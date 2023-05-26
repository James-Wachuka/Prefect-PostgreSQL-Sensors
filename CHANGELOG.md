# Changelog
All notable changes to the "prefect_postgres_sensors" package will be documented in this file.

## [0.6.0] - 26-05-2023

### Added
- added the following features to the package:
- **TableUpdatedSensor**: Monitors the last update timestamp of a table in a PostgreSQL database.
- **RowCountSensor**: Retrieves the row count of a table in a PostgreSQL database.
- **ColumnChangeSensor**: Detects changes in specific columns of a table in a PostgreSQL 
database.
- **QueryPerformance**: Monitors the performance of queries executed against the table.
- **TableFragmentationSensor**: Monitors the level of fragmentation within the table itself. 
- **DiskSpaceUsage**: Tracks the disk space used by the table and its associated indexes. 


### Changed

- Updated the package metadata in `setup.py` with correct information.
- updated `__init__.py`

### Deprecated

- None.

### Removed

- None.

### Fixed

- None.

---


## [0.2.0] - 26-05-2023

### Added
- Initial release of the "prefect_postgres_sensors" package.
- Detailed usage instructions in the README file.
- License information and contributing guidelines in the README file.
- Support section in the README file with a link to open issues.
- Acknowledgments section in the README file.
- Related Projects section in the README file.
- Release Notes section in the README file.

### Changed

- Updated the package metadata in `setup.py` with correct information.
- updated `__init__.py`

### Deprecated

- None.

### Removed

- None.

### Fixed

- None.

---
