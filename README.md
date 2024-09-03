# Loan Schedule API

## Table of Contents

- [Introduction](#introduction)
- [Setup](#setup)
    - [Python 3.12](#python-312)
    - [Install Requirements](#install-requirements)
    - [Generate .env File](#generate-env-file)
    - [Install Pre-commit](#install-pre-commit)
    - [Install Tox](#install-tox)
- [Usage](#usage)
    - [Run Docker Compose for Database](#run-docker-compose-for-database)
    - [Start Server](#start-server)
    - [Run Tox](#run-tox)
    - [Run Pre-commit Manually](#run-pre-commit-manually)


## Introduction

Brief description of the project and its purpose.


## Setup

### Python 3.12

1. **Install Python 3.12**:
   Download and install Python 3.12 from the official [Python website](https://www.python.org/downloads/).

2. **Create Virtual Environment**:
   ```bash
   python3.12 -m venv venv
   ```

3. **Activate Virtual Environment**:
    - On Windows:
      ```bash
      .\\venv\\Scripts\\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

### Install Requirements

Install the required packages using \`requirements.txt\`:

```bash
pip install -r requirements.txt
```

### Generate `.env` file

Adjust values if needed:

```bash
cp .template-env .env
```

### Install Pre-commit

Set up pre-commit hooks:

1. **Install Pre-commit**:
   ```bash
   pip install pre-commit
   ```

2. **Install the Hooks**:
   ```bash
   pre-commit install
   ```

### Install Tox

Install Tox for testing in multiple environments:

```bash
pip install tox
```

## Usage

Provide usage instructions and examples here.

### Run Docker Compose for Database

Start the database using Docker Compose:

```bash
docker-compose -f docker-compose.local.yaml up -d database
```

### Start server

```bash
  python src/manage.py runserver
```

### Run Tox

Execute Tox to run tests:

```bash
tox
```

to run single environment use one of the following commands:

```bash
tox -e pytest
```

```bash
tox -e pylint
```

```bash
tox -e flake8
```

```bash
tox -e isort
```

```bash
tox -e django-checks
```

```bash
tox -e coverage
```

### Run Pre-commit Manually

Run pre-commit checks manually:

```bash
pre-commit run --all-files
```

to skip pre-commit checks use:

```bash
SKIP=django-check pre-commit run
```

## Local development with Docker/For other teams

To run backend server locally please follow the steps below:
* create `.env` file in root dir and copy `.template-env` to `.env` and adjust the values if needed:
```bash
cp .template-env .env
```
* run docker-compose:
```bash
docker-compose -f docker-compose.local.yaml up --build -d
```

* enjoy backend with url http://localhost:8000/.
* admin panel available at http://localhost:8000/admin/ with credentials in `.env` file.
Here you can put some static data to check the frontend or manualy fix something.

### APIs Documentation

To view APIs documentation go to [/api/docs/](http://localhost:8000/api/docs/)

To download APIs schema for testing tools go to [/api/schema/](http://localhost:8000/api/schema/)
