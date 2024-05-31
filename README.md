# Open Selected Api

## Overview

This project is a Flask web application using SQLite as the database. The following instructions will guide you through setting up the development environment, running the application, testing, linting, formatting the code, and managing database migrations.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:
- Python 3.10
- Flask
- pip (Python package installer)
- npm (for serverless.yml deploy)

## Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/davidmm07/open_selected_api.git
    cd open_selected_api
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up your environment variables:**

    Create a `.env` file in the root directory and add the necessary environment variables:

    ```env
    FLASK_APP=./app/app.py
    FLASK_ENV=development
    ```

## Makefile Commands

### Development

To run the Flask development server:

```sh
make dev
```
### Testing

To run the test suite using pytest:

```sh
make test
```
This command sets the PYTHONPATH to the current directory and runs pytest with output displayed.


### Database Migrations

To prepare the database for migrations:

```sh
make db_prepare
```
This command stamps the current state of the database and generates a new migration.

To apply the latest migrations:
```sh
make migrate_up
```
To roll back the latest migration:
```sh
make migrate_down
```
To generate a new migration:
```sh
make migrate
```
### Code Coverage

To measure code coverage:

1. **Install coverage:**
```sh
pip install coverage
```

2. **Run tests with coverage:**
```sh
coverage run -m pytest
```
3. **Generate coverage report:**
```sh
coverage report
```
4. **Generate HTML coverage report:**
```sh
coverage html
```
The HTML report will be generated in the htmlcov directory.

### Deploy

1. **Install serverless:**
```bash
  npm install -g serverless
```
2. **Create app:**

```bash
  sls
```
3. **Deploy command :**
```bash
  sls deploy --verbose
```

4. **Check request in real time :**
```bash
  sls logs -f app -t
```

5. **Remove deploy and reverse all the infraestructure:**
```bash
  sls remove
```



### Additional Notes
Ensure your database engine is properly configured in the app.py file.
For more details on Flask configuration, visit the Flask documentation.

### License
This project is licensed under the MIT License.