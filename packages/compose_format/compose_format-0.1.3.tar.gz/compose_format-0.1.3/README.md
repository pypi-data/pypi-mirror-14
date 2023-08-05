# compose_format
Format docker compose files.

Note that this small utility is just valid until docker-compose has itself a format functionality.
Currently docker-compose just support the "config" switch. Which joins multiple compose files and print them in a machine readable form.

## Usage

### Via Python

Install it via:
`pip3 install compose_format`

### Via Docker

After that use it like:
`echo "docker-compose.yml" > docker run -t compose_format`

## Features
 - Support for Version 2 and Version 1.
 - Orders Services, Volumes, Networks
 - Orders Definitions
 - Orders Port and Volume Lists
