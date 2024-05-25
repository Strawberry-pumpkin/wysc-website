# wysc-website

To get started with local development
    `pip install -r requirements.txt`

You will need a copy of the settings_local.py file or you will have to create one yourself.
After that start with the existing database, please put the db.sqlite3 file in this folder
alternatively you can setup a fresh database as follows:

then `python manage.py makemigrations`
`python manage.py runserver`

Alternatively with daphne
daphne -b 0.0.0.0 -p 8000 wysc.asgi:application