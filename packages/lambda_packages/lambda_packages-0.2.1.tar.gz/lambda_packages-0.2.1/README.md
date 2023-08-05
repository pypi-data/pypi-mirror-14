# lambda-packages [![Build Status](https://travis-ci.org/Miserlou/lambda-packages.svg)](https://travis-ci.org/Miserlou/lambda-packages) [![Slack](https://img.shields.io/badge/chat-slack-ff69b4.svg)](https://slackautoinviter.herokuapp.com/)
Various popular libraries, pre-compiled to be compatible with AWS Lambda.

Currently includes support for:

* MySQL-Python
* psycopg2

## Installation

    pip install lambda-packages

## Usage

**lambda-packages** also includes a manifest with information about the included packages and the paths to their binaries.

```python
from lambda_packages import lambda_packages

print lambda_packages['psycopg2']['version'] 
# 2.6.1
print lambda_packages['psycopg2']['path'] 
# /home/YourUsername/.venvs/lambda_packages/psycopg2/psycopg2-2.6.1.tar.gz
```

## Contributing

To add support for more packages, send a pull request containing a gzipped tarball of the package (build on Amazon Linux and tested on AWS Lambda) in the appropriate directory and an updated manifest.

Useful targets include:

* MongoEngine
* pandas
* PIL
* scipy
