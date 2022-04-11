#!/bin/bash

set -e

export PYTHONPATH='./'

TAG=$(python -c 'from beaker_run import VERSION; print("v" + VERSION)')
MAJOR_TAG=$(python -c 'from beaker_run import VERSION; print("v" + VERSION.split(".")[0])')

read -p "Creating new release for $TAG. Do you want to continue? [Y/n] " prompt

if [[ $prompt == "y" || $prompt == "Y" || $prompt == "yes" || $prompt == "Yes" ]]; then
    python scripts/prepare_changelog.py
    git add -A
    git commit -m "Bump version to $TAG for release" || true && git push
    echo "Creating new git tag $TAG"
    git tag "$TAG" -m "$TAG"
    git tag "$MAJOR_TAG" -m "$MAJOR_TAG"
    git push --tags
else
    echo "Cancelled"
    exit 1
fi
