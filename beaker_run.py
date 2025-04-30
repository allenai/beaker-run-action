import os
import signal
import sys
import time
import uuid
from typing import cast

import click
import petname
import rich
import yaml
from beaker import (
    Beaker,
    BeakerCancelationCode,
    BeakerExperimentSpec,
    BeakerJob,
    BeakerWorkloadStatus,
)
from rich import pretty, print, traceback

VERSION = "2.0.0"


class TermInterrupt(Exception):
    pass


def handle_sigterm(sig, frame):
    del sig, frame
    raise TermInterrupt


def generate_name() -> str:
    return cast(str, petname.generate()) + "-" + str(uuid.uuid4())[:8]


def format_job_status(job: BeakerJob) -> str:
    if job.status.canceled_code in {
        BeakerCancelationCode.system_preemption,
        BeakerCancelationCode.user_preemption,
        BeakerCancelationCode.sibling_task_preemption,
    }:
        return ":warning: preempted"

    status = job.status.status

    if status == BeakerWorkloadStatus.succeeded:
        return ":white_check_mark: succeeded"
    elif job.status.created:
        return ":thumbsup: created..."
    elif status == BeakerWorkloadStatus.submitted:
        return ":stopwatch: submitted..."
    elif status == BeakerWorkloadStatus.queued:
        return ":stopwatch: queued..."
    elif status == BeakerWorkloadStatus.ready_to_start:
        return ":stopwatch: ready_to_start..."
    elif status == BeakerWorkloadStatus.initializing:
        return ":stopwatch: initializing..."
    elif status == BeakerWorkloadStatus.running:
        return ":runner: running..."
    elif status == BeakerWorkloadStatus.uploading_results:
        return ":stopwatch: uploading results..."
    elif status == BeakerWorkloadStatus.canceled:
        return ":no_entry_sign: canceled..."
    elif status == BeakerWorkloadStatus.stopping:
        return ":no_entry_sign: stopping..."
    elif status == BeakerWorkloadStatus.succeeded:
        return ":white_check_mark: succeeded"
    elif status == BeakerWorkloadStatus.failed:
        return ":no_entry_sign: failed..."
    else:
        return ""


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
@click.option("--org", default="ai2", help="The Beaker organization")
@click.option("-n", "--name", default=None, help="A name to assign to the experiment")
@click.option(
    "--timeout",
    type=int,
    default=-1,
    help="""Time to wait (in seconds) for the experiment to finish.
    A timeout of -1 means wait indefinitely. A timeout of 0 means don't wait at all.""",
)
@click.option(
    "--poll-interval",
    type=int,
    default=5,
    help="""Time to wait (in seconds) between polling for status changes of the experiment's jobs.""",
)
def main(
    spec: str,
    token: str,
    workspace: str,
    org: str = "ai2",
    name: str | None = None,  # type: ignore
    timeout: int = -1,
    poll_interval: int = 5,
) -> int:
    """
    Submit and await a Beaker experiment defined by the SPEC.

    SPEC can be a JSON or Yaml string or file.
    """
    console = rich.get_console()

    with Beaker.from_env(user_token=token, default_workspace=workspace, default_org=org) as beaker:
        print(f"❯ Authenticated as [b]'{beaker.user_name}'[/]")

        name = name if name is not None else generate_name()
        print(f"❯ Experiment name: [b]'{name}'[/]")

        # Load experiment spec.
        serialized_spec: str
        if os.path.exists(spec):
            with open(spec, "rt") as spec_file:
                serialized_spec = spec_file.read()
        else:
            serialized_spec = spec

        spec_dict = yaml.load(serialized_spec, Loader=yaml.SafeLoader)
        exp_spec = BeakerExperimentSpec.from_json(spec_dict)

        # Submit experiment.
        print("❯ Submitting experiment...")
        workload = beaker.experiment.create(name=name, spec=exp_spec)
        tasks = list(workload.experiment.tasks)
        print(f"  :eyes: See progress at {beaker.workload.url(workload)}")

        # Can return right away if timeout is 0.
        if timeout == 0:
            return 0

        # Otherwise we wait for all tasks to complete and then display the logs.
        try:
            print("❯ Waiting for tasks to complete...")
            task_to_status: dict[str, str] = {task.id: "pending..." for task in tasks}
            task_finalized: dict[str, bool] = {task.id: False for task in tasks}
            start_time = time.time()
            time.sleep(poll_interval)
            while timeout < 0 or time.time() - start_time <= timeout:
                # Check for status changes.
                for task in tasks:
                    job = beaker.workload.get_latest_job(workload, task=task)
                    if job is not None:
                        status = format_job_status(job)
                        if status != task_to_status[task.id]:
                            print(f"  Task [i]'{task.name}'[/] ❯ {status}")
                            task_to_status[task.id] = status

                        if job.status.HasField("finalized"):
                            task_finalized[task.id] = True

                # Check if all tasks have been completed.
                if all(task_finalized.values()):
                    break
                else:
                    time.sleep(poll_interval)
            else:
                print("[red]Timeout exceeded![/]")
                raise TimeoutError()

            # Get logs and exit codes.
            for task in tasks:
                job = beaker.workload.get_latest_job(workload, task=task)
                assert job is not None
                print()
                console.rule(f"Logs from task [i]'{task.name}'[/] :point_down:")
                for job_log in beaker.job.logs(job, follow=True):
                    console.print(job_log.message.decode(), highlight=False, markup=False)
                print()
                console.rule(f"End of logs from task [i]'{task.name}'[/]")

            print("❯ Summary:")
            exit_code = 0
            for task in tasks:
                job = beaker.workload.get_latest_job(workload, task=task)
                assert job is not None
                if job.status.HasField("exit_code") and job.status.exit_code > 0:
                    exit_code = job.status.exit_code
                    print(f"  :x: Task '{task.name}' failed with exit code {exit_code}")
                elif job.status.HasField("failed"):
                    exit_code = 1
                    print(f"  :x: Task '{task.name}' failed")
                    if job.status.HasField("message") and job.status.message:
                        print(job.status.message)
                else:
                    print(f"  :white_check_mark: Task '{task.name}' succeeded")
            print(f"❯ {beaker.workload.url(workload)}")

        except (KeyboardInterrupt, TermInterrupt, TimeoutError):
            print("[yellow]Canceling jobs...[/]")
            beaker.workload.cancel(workload)
            return 1

        return exit_code


if __name__ == "__main__":
    rich.reconfigure(
        width=max(rich.get_console().width, 180), force_terminal=True, force_interactive=False
    )
    pretty.install()
    traceback.install(width=180, show_locals=True, suppress=[click])
    signal.signal(signal.SIGTERM, handle_sigterm)

    sys.exit(main())
