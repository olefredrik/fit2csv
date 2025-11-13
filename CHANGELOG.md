# Changelog

All notable changes to this project will be documented in this file.

This project follows [Semantic Versioning](https://semver.org).

---

## [Unreleased]

### Ideas / Exploration

- Explore improvements to the macOS GUI wrapper (more detailed UI, optional settings, better affordances).
- Potential future work will be added here as it becomes more concrete.

---

## [0.2.0] – 2025-11-13

### Added

- New **duotone runner app icon** with cleaner silhouette and improved motion dynamics.
- Full macOS `.iconset` and `.icns` generation workflow.
- Updated `mac-app/README_APP.md` with:
  - Clearer instructions for configuring custom icons in macOS bundles.
  - Details about `CFBundleIconFile` and `CFBundleIconName`.
  - Steps for removing “Get Info” icon overrides.
  - Commands for refreshing macOS icon cache (`killall Finder`, `killall Dock`).

### Improved

- Build instructions for the Automator app wrapper.
- Developer documentation for a more reproducible build process.

### Diff

[`0.1.0...0.2.0`](https://github.com/olefredrik/fit2csv/compare/v0.1.0...v0.2.0)

---

## [0.1.0] – 2025-11-12

### Added

- Initial project release.
- Python batch converter script: `fit2csv_batch.py`.
- macOS Automator application wrapper with:
  - Folder selection dialogs
  - Automatic output folder creation (`csv_out`)
  - macOS notifications
  - Automatic opening of output folder after conversion
- Project documentation and license.

### Diff

_Initial release — no previous version._
