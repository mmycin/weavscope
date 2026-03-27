# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of the `WeavScope` class for high-level Weaviate interaction.
- Support for config-driven lifecycle management (`WeaviateConfig`).
- Automatic multi-tenant creation and deletion via context manager.
- Helper classes for batch ingestion (`scope.batch.add_objects`) and querying (`scope.query.hybrid`).
- Idempotent and deterministic UUID generation for document insertions.
- Basic support for various vectorization providers including Gemini, OpenAI, Cohere, etc.

### Fixed
- Resolved `500 Internal Server Error` and header pollution issues when using the `gemini` embedding model provider natively via Google.
