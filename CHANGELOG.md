# Changelog

All notable changes to the Media Knowledge Pipeline will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.6.0] - 2026-02-12

### Added
- Completely redesigned CLI wizard system with modular architecture
- Four core workflow plugins: media processing, batch processing, document processing, and Anki generation
- Shared utility modules for input validation and standardized user prompting
- Comprehensive test suite following Test-Driven Development principles
- Custom filename support for JSON output with organized directory structure
- Backward compatibility layer maintaining all existing CLI command functionality
- Detailed migration guide and architectural documentation

### Changed
- Enhanced output path handling to organize files in dedicated directories
- Improved input validation with URL, file path, and format checking
- Upgraded user experience with consistent prompting across all workflows

### Fixed
- Output files now properly organized in outputs/ directory structure
- Custom filename handling distinguishes between cancellation and auto-naming
- Workflow configuration sharing between components

## [2.5.3] - 2026-02-12

### Added
- Comprehensive CLI test coverage
- Enhanced documentation and user guides

## [2.5.2] - 2026-02-12

### Fixed
- Resolved interactive launcher import errors
- Fixed CLI command import issues

## [2.5.1] - 2026-02-10

### Added
- Enhanced CLI launcher with ASCII art display
- Improved system status checking

## [2.5.0] - 2026-02-10

### Added
- Initial enhanced CLI frontend implementation
- Interactive menu system with wizard workflows
- Media processing wizard with YouTube and local file support
- Batch processing wizard with parallel worker configuration
- Document processing wizard with PDF/EPUB/MOBI support
- Anki flashcard generation wizard
- System status and requirements checking
- Enhanced error handling and user guidance
