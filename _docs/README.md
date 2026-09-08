# 📚 data-pipeline Documentation

Welcome to the complete documentation for this repository. This documentation is automatically generated and maintained by Woden Docbot.

![Files Documented: 24](https://img.shields.io/badge/Files_Documented-24-blue) ![Coverage: 96%](https://img.shields.io/badge/Coverage-96%-green) ![Last Updated: 2026-09-08](https://img.shields.io/badge/Last_Updated-2026--09--08-gray)

## 🔗 Quick Links

[📂 .github](./github/README.md) | [📂 Root files](./ROOT.md) | [📂 airflow](./airflow/README.md)
[📂 dbt](./dbt/README.md) | [📂 profiles](./profiles/README.md) | [📂 src](./src/README.md)
[📋 Dependencies](./DEPENDENCIES.md)


---

## 📑 Documentation Sections

### [.github](./github/README.md)
Its single configuration file controls how documentation is emitted (per-directory, per-file, or both), where generated docs are stored, which target branches trigger processing, and a set of preferences that shape the content.

The configuration also declares an architecture guide project, per-directory override hooks, a whitelist of file extensions to include in documentation, and a comprehensive set of glob patterns and related settings that define which files are included in or excluded from generated docs. This file is the central place to change documentation behavior for the repository.

The configuration file encapsulates the directory's purpose and is the only component to consult when modifying documentation generation settings.

![Files: 1](https://img.shields.io/badge/Files-1-blue)

### [Root files](./ROOT.md)
This directory contains infrastructure configuration for running a multi-service Docker Compose application that brings up Apache Airflow components together with a PostgreSQL database and an auxiliary dbt docs service. It centralizes common build and environment settings and defines the set of services required to run the Airflow stack and its supporting components.

The directory is organized around a single docker-compose.yml that declares the entire multi-service application.

![Files: 1](https://img.shields.io/badge/Files-1-blue)

### [airflow](./airflow/README.md)
This directory groups the documented sections listed below. It contains no directly documented files of its own — either its files are excluded by this repository's DocBot configuration, or it only holds subdirectories.

### [dbt](./dbt/README.md)
This directory groups the documented sections listed below. It contains no directly documented files of its own — either its files are excluded by this repository's DocBot configuration, or it only holds subdirectories.

### [profiles](./profiles/README.md)
This directory holds the dbt profile configuration used to define how dbt connects to local DuckDB databases for the project. It centralizes connection outputs and the active target so that dbt runs can select the appropriate environment (development or production-like) when invoked.

The single file in this directory configures a profile named "ecommerce_dbt" with two outputs (dev and live), each using the DuckDB adapter and pointing at local DuckDB files; it also defines an attached secondary DuckDB file aliased as "warehouse" and sets the active target to "dev" to make the local development settings the default for dbt runs.

The directory is organized around a single YAML file that consolidates all dbt connection configuration for the project. profiles.yml contains the profile name, multiple outputs for different environments, and the active target selection; together these elements let dbt choose which DuckDB connection (and which attached secondary file alias) to use at runtime.

![Files: 1](https://img.shields.io/badge/Files-1-blue)

### [src](./src/README.md)
The src directory contains modules related to initializing and exercising a local development database environment using DuckDB. It groups a project-level script for creating or initializing a development database and a test-oriented module that references DuckDB for validation purposes.

This directory is organized around direct DuckDB usage: one file performs project-level preparation of a development database environment, and the other is part of the test suite that imports and exercises DuckDB interactions.

The directory is organized as a small collection of top-level Python modules that directly import DuckDB at module scope. create_dev_db.py is a script-style module whose contents are intended to prepare or initialize a development database environment; its code is arranged at the module level rather than inside classes or named functions. test_duckdb.py is a test-oriented module that imports the DuckDB package and is intended to be part of the test suite that exercises DuckDB interactions.

![Files: 2](https://img.shields.io/badge/Files-2-blue)

---

## 📊 Documentation Statistics

- **Files Documented**: 24
- **Directories**: 15
- **Coverage**: 96%
- **Eligible Source Files**: 25
- **Last Updated**: 2026-09-08

---

## 🧭 How to Navigate

> ℹ️ **INFO**
> Each directory has its own README.md with detailed information about that section. Use the breadcrumb navigation at the top of each page to navigate back to parent directories.

### Navigation Features

- **Breadcrumbs** - At the top of each page, showing your current location
- **Directory READMEs** - Each folder has a comprehensive overview
- **File Documentation** - Click through to individual file documentation
- **Search** - Use GitHub's search or your IDE's search functionality

---

## 🤖 About Woden DocBot

This documentation is automatically generated and kept up-to-date by Woden DocBot, an AI-powered documentation assistant. DocBot analyzes code on every pull request and updates documentation to reflect changes.

### Features

- **Automatic Updates** - Documentation updates on every PR
- **Comprehensive Coverage** - Files, functions, classes, and directories
- **Smart Navigation** - Breadcrumbs, related files, and parent links
- **AI-Powered** - Uses Azure GPT models for intelligent documentation generation

---

*Generated by Woden DocBot for data-pipeline*