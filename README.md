# TODO

- Unit testing on damage management
- Change langage button
- Document data upload
- Responsive layout
- Communication between users via websockets
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
