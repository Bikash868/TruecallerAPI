
Installation:
Install the required packages using pip:
pip install django rest_framework django-filter faker

Start the server from the root directory of your project:
python manage.py runserver

Data Population:
To populate your database, follow these steps:

Populate auth.user Database:
Load initial user data using the following command:
python manage.py loaddata auth_user_data.json

Populate Contact and UserProfile Databases:
Use the script populate_db.py to populate the necessary data.