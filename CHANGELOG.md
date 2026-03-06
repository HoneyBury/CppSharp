# Changelog

This project follows Semantic Versioning and Keep a Changelog.

---

## [5.0.0] - 2026-03-07

### Added
- Added cross-platform CI pipeline for Linux, macOS, and Windows.
- Added automated formatting workflow with automatic commit support.
- Added Taskfile-based local developer workflows.
- Added static analysis checks with cppcheck and clang-tidy.
- Added text normalization tooling for encoding and line endings.

### Changed
- Updated project version to 5.0.0.
- Unified project engineering standards for build, lint, test, and packaging.
- Refined Conan and CMake integration for preset-based local/CI usage.

### Removed
- Removed in-file code comments from project source and CMake scripts.

---

## [4.1.2] - 2025-06-28

### Added
- Added NSIS package support for Windows installer generation.
- Added CPack cross-platform packaging for DEB, NSIS, and DragNDrop.
- Added metadata extraction from CMakeLists.txt in conanfile.py.
- Added CPACK_CREATE_DESKTOP_SHORTCUT option.
- Added GNUInstallDirs, CMakePackageConfigHelpers, and CPack integration.
- Added exports and exports_sources in conanfile.py.

### Changed
- Updated project version to 4.1.2.
- Improved output directories, installation layout, package naming, and architecture handling.
- Refined conanfile.py structure and dependency flow.
- Expanded README build and package documentation.

### Fixed
- Fixed inconsistent output directories on some platforms.
- Fixed missing source/path issues during Conan builds.
- Fixed missing LICENSE and README in CPack output.

---

## [4.0.0] - 2025-06-28

### Added
- Added LICENSE file.
- Added more install options.

### Changed
- Updated conanfile.
- Updated CMakeLists.txt.
- Updated required C++ standard.

### Fixed
- Fixed install issues.

---
