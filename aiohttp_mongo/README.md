## Requirements

- Python +3.5.3
- Aiohttp 3.1.0 (Asynchronous http server with asyncio)
- PyYAML 3.12 (To parse configuration file in yaml format)
- motor 1.2.1 (MongoDB driver for asyncio)
- locustio (a tool for load testing)

## Installation
To install python dependencies simply run:
```
python setup.py install
```

## Testing
To run all tests simply run:
```
python setup.py test
```
To see coverage report, run:
```
python test.py
```

## Load Testing
To run load testing simply run:
```
./load_test.sh
```
and open localhost:8089 and use locust.

## Usage
To run on default config, run:
```
twylacfg run
```

To run on custom config, run:
```
twylacfg run --config=path/to/config.yaml
```

To create a config sample:
```
twylacfg generate_config_file --path=path/to/config.yaml (default = ./config.yaml)
```

## Features:

- [x] Should run under Python 3.6, but is not required to run on Python 2.7.
- [x] Correct input conditions should be checked for, and proper error responses must be returned. The required keys in the POSTed JSON document are tenant,integration_typeand non-empty configuration.
- [x] All IO operations should be asynchronous, and there should be no locking operations when the service is running in single threaded mode.
- [x] The standard Python toolchain for installing dependencies and creating entry points (especially for the command line) should be used.
- [x] Unit and integration test suites should be included. The test suites should also generate coverage reports.

###### Bonus:
- [x]  A feature that we haven’t implemented yet in our own service is load-testing. We would really like to know how you would approach this topic, be it in the form of a couple of lines of code, a link to a package that can be easily conﬁgured and used, or a web service