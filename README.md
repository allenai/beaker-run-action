# beaker-run-action

A GitHub Action for submitting experiments to Beaker.

By default the action will wait for the experiment to complete, then print the logs
from the experiment and exit with the same exit code as the experiment.
In this way you can essentially use this action to run a step of your workflow on Beaker.
This is useful when you need special hardware, such as GPUs, for a step.

## Inputs

### `spec` (required)

A YAML or JSON experiment spec. This can also be a path to a YAML or JSON file.

### `token` (required)

Your Beaker [token](https://beaker.org/user).

### `workspace` (required)

The Beaker workspace to use.

### `clusters` (optional)

A comma-separated list of clusters that can be used to override the cluster
in the spec for a task, if any of them have enough resources avaiable.

For example, you may want to set the cluster in your spec to a scalable cloud cluster,
and then set the `clusters` input to a list of on-premise clusters.
That way if any of those on-premise clusters have enough resources available,
they will be used instead of the cloud cluster specified in the experiment spec.

### `timeout` (optional)

Time to wait (in seconds) for the experiment to finish.

A timeout of -1 (the default) means wait indefinitely, a timeout of 0 means don't wait at all,
and a positive timeout means the action will wait that many seconds for the experiment to complete. If the experiment doesn't complete within `timeout` seconds, it will be stopped and the action will exit as a failure.

*NOTE: When `timeout` is 0, the action will always succeed even if the Beaker experiment doesn't succeed.*

## Example

```yaml
uses: allenai/beaker-run-action@v1
with:
  spec: |  # <-- !! This bar "|" is important !!
    version: "v2"
    description: "Hello, World!"
    tasks:
      - name: "hello"
        image:
          docker: "hello-world"
        context:
          cluster: "ai2/petew-cpu"
        result:
          path: "/unused"
  token: ${{ secrets.BEAKER_TOKEN }}
  workspace: ai2/petew-testing
  clusters: ai2/general-cirrascale,ai2/allennlp-cirrascale
```
