# GitHub Release Process

## Steps

1. Update the `VERSION` global constant in `beaker_run.py`.

2. Run the release script:

    ```bash
    ./scripts/release.sh
    ```

    This will commit the changes to the CHANGELOG and `version.py` files and then create a new tag in git
    which will trigger a workflow on GitHub Actions that handles the rest.

3. Lastly, in order to publish to the Actions marketplace, find the major and minor tags creating during the
   release (.e.g "v1" and "v1.0") and manually publish a new release from those via the GitHub dashboard:
   https://github.com/allenai/beaker-run-action/tags

## Fixing a failed release

If for some reason the GitHub Actions release workflow failed with an error that needs to be fixed, you'll have to delete both the tag and corresponding release from GitHub. After you've pushed a fix, delete the tag from your local clone with

```bash
git tag -l | xargs git tag -d && git fetch -t
```

Then repeat the steps above.
