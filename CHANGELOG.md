# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Fixed

- Always uses latest Beaker-py image now.

## [v1.1.8](https://github.com/allenai/beaker-run-action/releases/tag/v1.1.8) - 2022-09-23

### Fixed

- Upgraded `beaker-py` to fix a bug with `Node` data model.

## [v1.1.7](https://github.com/allenai/beaker-run-action/releases/tag/v1.1.7) - 2022-09-14

### Fixed

- Preempted jobs are handled gracefully now so the task won't be treated as a failure when its latest job is preempted.

## [v1.1.6](https://github.com/allenai/beaker-run-action/releases/tag/v1.1.6) - 2022-06-24

### Added

- Summary of task exit codes now printed at the end.

## [v1.1.5](https://github.com/allenai/beaker-run-action/releases/tag/v1.1.5) - 2022-05-31

### Changed

- Bumped `beaker-py` to version 1.3.

### Fixed

- '\r' now replaced with '\n' when displaying log lines.

## [v1.1.4](https://github.com/allenai/beaker-run-action/releases/tag/v1.1.4) - 2022-05-06

### Fixed

- Fixed `beaker-py` version requirement.

## [v1.1.3](https://github.com/allenai/beaker-run-action/releases/tag/v1.1.3) - 2022-05-06

### Changed

- Bumped `beaker-py` to version 0.15.

## [v1.1.2](https://github.com/allenai/beaker-run-action/releases/tag/v1.1.2) - 2022-05-05

### Changed

- Bumped `beaker-py` to version 0.14.1.

## [v1.1.1](https://github.com/allenai/beaker-run-action/releases/tag/v1.1.1) - 2022-05-04

### Changed

- Bumped `beaker-py` to version 0.14.0.

## [v1.1.0](https://github.com/allenai/beaker-run-action/releases/tag/v1.1.0) - 2022-04-21

### Added

- Added support for multi-task experiments.
- Added optional `name` and `poll_interval` input parameters.

### Changed

- Bumped `beaker-py` to version 0.11.0.
- Only clusters from the corresponding input variable that don't have any queued jobs
  will be considered, and out of those, one will be picked randomly.
- Timestamp from Beaker logs is now stripped out.

## [v1.0.8](https://github.com/allenai/beaker-run-action/releases/tag/v1.0.8) - 2022-04-13

### Changed

- Bumped `beaker-py` to version 0.8.2.

## [v1.0.7](https://github.com/allenai/beaker-run-action/releases/tag/v1.0.7) - 2022-04-12

### Changed

- Bumped `beaker-py` to version 0.8.

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
