import json
import os
import signal
import sys
import uuid
from typing import List, Optional

import click
import petname
import rich
from beaker import Beaker, ExperimentSpec, TaskResources
from rich import pretty, print, traceback

VERSION = "1.0.0"


class TermInterrupt(Exception):
    pass


def handle_sigterm(sig, frame):
    raise TermInterrupt


def generate_name() -> str:
    return petname.generate() + "-" + str(uuid.uuid4())[:8]


@click.command()
@click.argument("spec-json", type=str)
@click.option(
    "--token",
    required=True,
    help="Your Beaker user token",
    default=lambda: os.environ.get("BEAKER_TOKEN"),
)
@click.option("--workspace", required=True, help="The Beaker workspace to use")
@click.option(
    "--clusters",
    help="""A comma-separated list of clusters that can be used to override the
    cluster for a task if any of them have enough resources available.""",
)
@click.option("--org", default="ai2", help="The Beaker organization")
@click.option("-n", "--name", default=None, help="A name to assign to the experiment")
def main(
    spec_json: str,
    token: str,
    workspace: str,
    clusters: str,
    org: str = "ai2",
    name: Optional[str] = None,
):
    beaker = Beaker.from_env(user_token=token, default_workspace=workspace)

    print(f"- Authenticated as {beaker.account.name}")

    name: str = name if name is not None else generate_name()

    # Load spec and determine the cluster(s) to use.
    spec = ExperimentSpec.from_json(json.loads(spec_json))
    clusters: List[str] = [] if not clusters else clusters.split(",")
    if clusters:
        for i, task in enumerate(spec.tasks):
            available_clusters = beaker.cluster.filter_available(
                task.resources or TaskResources(), *clusters
            )
            if available_clusters:
                cluster_to_use = available_clusters[0].full_name
                print(
                    f"\n- Found cluster with enough free resources for task {i}: '{cluster_to_use}'"
                )
                task.context.cluster = cluster_to_use

    print("\n- Experiment spec:", spec.to_json())

    print("\n- Submitting experiment...")
    experiment = beaker.experiment.create(name, spec)
    print(
        f"Experiment {experiment.id} submitted.\nSee progress at https://beaker.org/ex/{experiment.id}",
    )

    try:
        print("\n- Waiting for job to finish...")
        experiment = beaker.experiment.await_all(experiment, timeout=20 * 60)

        print("\n- Pulling logs...")
        logs = "".join([line.decode() for line in beaker.experiment.logs(experiment)])
        rich.get_console().rule("Logs")
        rich.get_console().print(logs, highlight=False)

        sys.exit(experiment.jobs[0].status.exit_code)
    except (KeyboardInterrupt, TermInterrupt):
        print("- Canceling job...", end="\n\n")
        beaker.experiment.stop(experiment)


if __name__ == "__main__":
    rich.get_console().width = max(rich.get_console().width, 180)
    pretty.install()
    traceback.install()
    signal.signal(signal.SIGTERM, handle_sigterm)

    main()
