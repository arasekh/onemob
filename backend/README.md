# onemob-django

installation
--------------------
- requirements:
 - Python 3.8.1
 - The `requirements.txt` file should list all Python libraries that your django project
 depends on, and they will be installed using:

 ```
 pip install -r requirements.txt
 ```
- create database using `python manage.py migrate` and you will see db.sqlite3 file created
- run your server using `python manage.py runserver`

> **Note:**

> - You need to create an admin user to manage your blog site by this command: `python manage.py createsuperuser`

api urls:
- http://localhost:8000/api/
- http://localhost:8000/api/get/<username>
- http://localhost:8000/api/create

Create url: open teminal and type this url. Note that httpie must be installed.

`$ http -a <USERNAME>:<PASSWORD> http://127.0.0.1:8000/api/create/ username='<YOUR_USERNAME>' password='<YOUR_PASSWORD>' first_name='<YOUR_FIRSTNAME>' last_name='<YOUR_LASTNAME>' email='<YOUR_VALID_EMAIL>'`
