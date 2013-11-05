Please don't use in prod
pip install Django south
Fill in the settings_example.py (database at minimum) and move to settings.py
python manage.py syncdb
python manage.py migrate task
python manage.py collectstatic
