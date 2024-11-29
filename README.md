# TODO

- Document upload
- Correct logging system
- Communication between investigator and user via websockets
- Unit testing

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
