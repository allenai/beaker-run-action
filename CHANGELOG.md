# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## [v1.0.6](https://github.com/allenai/beaker-run-action/releases/tag/v1.0.6) - 2022-04-12

### Changed

- Improved release process.

## [v1.0.5](https://github.com/allenai/beaker-run-action/releases/tag/v1.0.5) - 2022-04-12

### Changed

- The `spec` input can now be YAML or JSON, or a path to a YAML or JSON file.
- Bumped `beaker-py` to version 0.7.

## [v1.0.4](https://github.com/allenai/beaker-run-action/releases/tag/v1.0.4) - 2022-04-11

### Changed

- Updated Docker image to use the official `beaker-py` image as a base. This speeds up build time.

## [v1.0.3](https://github.com/allenai/beaker-run-action/releases/tag/v1.0.3) - 2022-04-11

### Fixed

- Fixed Docker image when ran with a different working directory.

## [v1.0.2](https://github.com/allenai/beaker-run-action/releases/tag/v1.0.2) - 2022-04-10

### Changed

- Minor upgrade to `beaker-py`, remove progress bars that don't render well in GH Actions.

## [v1.0.1](https://github.com/allenai/beaker-run-action/releases/tag/v1.0.1) - 2022-04-10

### Added

- Added `timeout` input.

## [v1.0.0](https://github.com/allenai/beaker-run-action/releases/tag/v1.0.0) - 2022-04-10

### Added

- Added `@v1` of action.

## [v0.0.1](https://github.com/allenai/beaker-run-action/releases/tag/v0.0.1) - 2022-04-10

### Added

- Added initial version of Action.
