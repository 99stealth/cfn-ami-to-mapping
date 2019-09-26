# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.0] - 2019-09-26
### Added
- `setup.py` in order to create packages
- Module `helper` with method `timeit` which allows measuring methods' execution time 
### Changed
- Package structure. Instead of one `main.py` was created structure based on best python practices. Now there are several python classes and one `run.py` file which calls them
- Makefile which now allows to build the package and install it on the system
- `.gitignore` which now ignores everything in `dist` directory and all `egg-info` directories
- Smoke tests in order to correspond to the new directory structure
### Removed
- `main.py` since it was changed by the new structured code design
- `test_cases.sh` and `timeit.py` from `.gitignore` as now 1-st is a part of CI and 2-nd is a part of the new structure
- `install`, `install-dependencies` from `Makefile` since this is not needed for the installation process



## [0.5.4] - 2019-09-20
### Added
- Key interruption exception

## [0.5.3] - 2019-09-19
### Added 
- Parameters which allow specifying aws-access-key-id and aws-secret-access-key inline

## [0.5.2] - 2019-09-10
### Added
- Information about utility's version

## [0.5.1] - 2019-09-06
### Added
- Informative outputs about current tasks
- Quiet mode for CI/CD perspectives

## [0.5.0] - 2019-09-04
### Added
- Regex which allows checking that AMI ID has been correctly passed

## [ 0.0.0 - 0.5.0] - 2019-08-29 - 2019-09-02
### Added
There was active development here. All the basic functionality had been developed here.
I think the utility is ready to use but there should be added a lot of improvements. So, I swear I'll do. 
### Changed
When I thought it's ready I decided to double-check and test it, and you know what? I found one critical bug so I decided to rewrite the main logic. Now it works nicely
### Fixed
Also, fixed a bunch
### Removed
There was some shitty stuff, but I don't really remember what and where :)