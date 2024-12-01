# Semestral project for KIV/PIA-E course

Author : Gabriel ROULEAU \
Academic year : 2024/2025

## Getting started

Follow these instructions to get a copy of the project running on your local machine.

### Prerequisites

Ensure you have the following installed:

* Python 3.7 or higher
* pip (Python package manager)
* virtualenv (recommended)

### Installation 

1. Clone the repository and navigate to its root

2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
source venv/Scripts/activate # on Linux: venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Paste the .env file provided by the author inside the project's root folder.

5. Run the application:

```bash
flask run --debug
```

## Running tests

To run test simply call pytest command from the project's root folder.

```bash
pytest
```

## Project structure

...

## Technologies

* Python: Core programming language.
* Flask: Micro web framework for developing web applications.
* SQLAlchemy: ORM for database integration.
* Jinja2: Template engine for rendering HTML.
* Bulma CSS: Frontend framework for responsive design.
* Authlib: Package for easy OAuth2 integration.
