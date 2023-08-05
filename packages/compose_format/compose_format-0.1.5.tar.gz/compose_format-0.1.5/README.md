[![Build Status](https://travis-ci.org/funkwerk/compose_format.svg)](https://travis-ci.org/funkwerk/compose_format)
[![](https://badge.imagelayers.io/funkwerk/compose_format.svg)](https://imagelayers.io/?images=funkwerk/compose_format:latest 'funkwerk/compose_format')
[![PyPi downloads](https://img.shields.io/pypi/dm/compose_format.svg)](https://pypi.python.org/pypi/compose_format/)
[![PyPi version](https://img.shields.io/pypi/v/compose_format.svg)](https://pypi.python.org/pypi/compose_format/)
[![Docker pulls](https://img.shields.io/docker/pulls/funkwerk/compose_format.svg)](https://hub.docker.com/r/funkwerk/compose_format/)
# compose_format

Format docker-compose files.

Note that this small utility is just valid until docker-compose has itself a format functionality.
Currently docker-compose just support the "config" switch. Which joins multiple compose files and print them in a machine readable form.

## Usage

### Via Python

Install it via:
`pip3 install compose_format`

After that use it like

`compose_format compose-format.yml`
this will print the formatted compose file to stdout.
To let it replace the compose file add `--replace`.

### Via Docker

Use it like:
`cat docker-compose.yml | docker run -i funkwerk/compose_format`

## Features
 - Support for Version 2 and Version 1.
 - Orders Services, Volumes, Networks
 - Orders Definitions
 - Orders Port and Volume Lists
