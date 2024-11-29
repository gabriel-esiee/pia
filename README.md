# TODO

- Document data upload
- Responsive layout
- Change langage button
- Communication between users via websockets
- Unit testing on damage management
- Use logger system (with log levels)
- Documentation for API
- Commentaries in source code

# Configuration

## Lancement de l'application

source venv/Scripts/activate
flask run --debug

## Extraction des dictionnaires de traduction

source venv/Scripts/activate
pybabel extract -F babel.cfg -o messages.pot .
pybabel init -i messages.pot -d translations -l fr

## Compilation des dictionnaires de traduction

source venv/Scripts/activate
pybabel compile -d translations
