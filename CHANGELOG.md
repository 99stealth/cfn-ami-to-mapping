# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.8.3](https://github.com/99stealth/cfn-ami-to-mapping/tree/v0.8.3) - 2020-03-12
### Removed
- Tests from python package

## [0.8.2](https://github.com/99stealth/cfn-ami-to-mapping/tree/v0.8.2) - 2020-01-10
### Fixed
- Nothing special just fixed comments for some functions :)
### Removed
- Option `quiet` from several functions since it is not needed anymore

## [0.8.1](https://github.com/99stealth/cfn-ami-to-mapping/tree/v0.8.1) - 2019-12-30
### Fixed
- Nothing special just fixed comments for some functions :)

## [0.8.0](https://github.com/99stealth/cfn-ami-to-mapping/tree/v0.8.0) - 2019-12-07
### Added
- Verbose mode
- Check which allows verifying if `--region` is exist
### Changed
- Removed prints and changed them to logging
- A mechanism which checks AWS keys moved from parsing to separate definition
### Fixed
- Exit mechanism after exceptions appear

## [0.7.2](https://github.com/99stealth/cfn-ami-to-mapping/tree/v0.7.2) - 2019-11-09
### Fixed
- Import order
- Linter

## [0.7.1](https://github.com/99stealth/cfn-ami-to-mapping/tree/v0.7.1) - 2019-11-03
### Added
- Support of Python 3.8

## [0.7.0](https://github.com/99stealth/cfn-ami-to-mapping/tree/v0.7.0) - 2019-10-29
### Added
- Color for a version :)
### Fixed
- Application's speed! Just check it out

![Speed fix demo](.media/070vs065.gif)
### Removed
- Notifications about processing since now users are not waiting for a while.

## [0.6.5](https://github.com/99stealth/cfn-ami-to-mapping/tree/v0.6.5) - 2019-10-07
### Added
- Added new option which allows set only needed AWS Regions
- Added new option which allows excluding regions from the full scope

## [0.6.4](https://github.com/99stealth/cfn-ami-to-mapping/tree/v0.6.4) - 2019-10-01
### Added
- Validation for AWS Access Key ID and AWS Secret Access Key

## [0.6.3] - 2019-10-01
### Fixed
- Help message

## [0.6.2] - 2019-09-30
### Fixed
- Linter
- Unittests

## [0.6.1] - 2019-09-27
### Added
Unit tests for methods:
- Enrich.images_info_with_id
- Enrich.images_info_with_name
- Get.images_names_from_init_name_map
- Get.images_ids_from_init_id_map
- Transform.dictionary_to_json
- Transform.dictionary_to_yaml
- Validate.images_ids
### Removed
Methods `images_ids_from_info` and `images_names_from_info` since they were not in use

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
