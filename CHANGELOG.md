# Changelog

All notable changes to this project will be documented in this file.

This project follows [Semantic Versioning](https://semver.org).

---

## [Unreleased]

### Ideas / Exploration

- Exploring improvements to the macOS GUI wrapper (more detailed UI, optional settings, enhanced affordances).
- Additional internal cleanup or refactoring to improve maintainability.

---

## [0.3.1] – 2025-11-13

### Improved

- Bundled `fitdecode` and related Python dependencies inside the macOS app bundle.
- The macOS app is now self-contained and no longer requires users to run `pip install fitdecode`.

### Diff

[0.3.0...0.3.1](https://github.com/olefredrik/fit2csv/compare/v0.3.0...v0.3.1))

---

## [0.3.0] – 2025-11-13

### Improved

- Translated the entire Python batch converter script (`fit2csv_batch.py`) from Norwegian to English for consistency across the repository.
- Cleaned up comments, improved naming consistency, and added clarifying documentation inside the script.
- No functional changes were introduced; conversion behavior remains identical.

### Diff

[`0.2.0...0.3.0`](https://github.com/olefredrik/fit2csv/compare/v0.2.0...v0.3.0)

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
