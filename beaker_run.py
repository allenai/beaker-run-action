import os
import random
import signal
import sys
import uuid
from typing import List, Optional

import click
import petname
import rich
import yaml
from beaker import Beaker, ExperimentSpec, TaskResources
from rich import pretty, print, traceback

VERSION = "1.0.8"


class TermInterrupt(Exception):
    pass


def handle_sigterm(sig, frame):
    raise TermInterrupt


def generate_name() -> str:
    return petname.generate() + "-" + str(uuid.uuid4())[:8]


@click.command()
@click.version_option(VERSION)
@click.argument("spec", type=str)
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
@click.option(
    "--timeout",
    type=int,
    default=-1,
    help="""Time to wait (in seconds) for the experiment to finish.
    A timeout of -1 means wait indefinitely. A timeout of 0 means don't wait at all.""",
)
def main(
    spec: str,
    token: str,
    workspace: str,
    clusters: str,
    org: str = "ai2",
    name: Optional[str] = None,
    timeout: int = -1,
):
    """
    Submit and await a Beaker experiment defined by the SPEC.

    SPEC can be a JSON or Yaml string or file.
    """
    beaker = Beaker.from_env(user_token=token, default_workspace=workspace)

    print(f"- Authenticated as [b]'{beaker.account.name}'[/]")

    name: str = name if name is not None else generate_name()

    print(f"- Experiment name: [b]'{name}'[/]")

    # Load experiment spec.
    serialized_spec: str
    if os.path.exists(spec):
        with open(spec, "rt") as spec_file:
            serialized_spec = spec_file.read()
    else:
        serialized_spec = spec
    spec_dict = yaml.load(serialized_spec, Loader=yaml.SafeLoader)
    exp_spec = ExperimentSpec.from_json(spec_dict)

    print("- Experiment spec:", exp_spec.to_json())

    cluster_to_use: Optional[str] = None
    clusters: List[str] = [] if not clusters else clusters.split(",")
    if clusters:
        for i, task_spec in enumerate(exp_spec.tasks):
            available_clusters = beaker.cluster.filter_available(
                task_spec.resources or TaskResources(), *clusters
            )
            random.shuffle(available_clusters)
            for cluster in available_clusters:
                cluster_utilization = beaker.cluster.utilization(cluster)
                if cluster_utilization.queued_jobs == 0:
                    cluster_to_use = cluster.full_name
                    task_spec.context.cluster = cluster_to_use
                    print(
                        f"- Found cluster with enough free resources for task {i}: [b]'{cluster_to_use}'[/b]"
                    )
                    break

    print("- Submitting experiment...")
    experiment = beaker.experiment.create(name, exp_spec)
    print(
        f"  See progress at {beaker.experiment.url(experiment)}",
    )

    if timeout == 0:
        return

    try:
        print("- Waiting for job to finish...")
        experiment = beaker.experiment.wait_for(
            experiment,
            timeout=None if timeout <= 0 else timeout,
            poll_interval=3.0,
        )[0]

        for task in beaker.experiment.tasks(experiment):
            logs = "".join(
                [line.decode() for line in beaker.experiment.logs(experiment, quiet=True)]
            )
            print("\n")
            rich.get_console().rule(f"Logs for task '{task.display_name}'")
            rich.get_console().print(logs, highlight=False)

        for job in experiment.jobs:
            if job.status.exit_code is not None and job.status.exit_code > 0:
                sys.exit(job.status.exit_code)
    except (KeyboardInterrupt, TermInterrupt, TimeoutError):
        print("- Canceling job...")
        beaker.experiment.stop(experiment)
        sys.exit(1)


if __name__ == "__main__":
    rich.get_console().width = max(rich.get_console().width, 180)
    rich.get_console().is_terminal = True
    pretty.install()
    traceback.install()
    signal.signal(signal.SIGTERM, handle_sigterm)

    main()
