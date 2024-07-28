import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phonebook.settings')

import django
django.setup()

from django.contrib.auth.models import User
from faker import Faker
from CallerInsight.models import Contact, UserProfile, MatchUserContact


fake = Faker()

def populate():
    # Creating 1,000 dummy records for the Contact model
    for _ in range(5000):
        name = fake.name()
        phone_number = fake.random_int(min=1000000000, max=9999999999)
        email = fake.email()
        spam = fake.boolean(chance_of_getting_true=10)  # 10% chance of being spam

        contact = Contact.objects.create(
            name=name,
            phone_number=phone_number,
            email=email,
            spam=spam
        )

    # Adding random data to the UserProfile model
    # populate auth.user table using auth_user_data fixture befor this
    
    users = User.objects.all()

    # print("all users:",len(users))
    # print("Adding data to UserProfile model")
    for user in users:
        phone_number = fake.random_int(min=1000000000, max=9999999999)
        email = fake.email()
        spam = fake.boolean(chance_of_getting_true=10)

        UserProfile.objects.create(
            user=user,
            phone_number=phone_number,
            email=email,
            spam=spam
        )

    print("Adding data to MatchUserContact model")
    # Creating some random matches between users and contacts
    for _ in range(3000):
        user = fake.random_element(users)
        contact = fake.random_element(Contact.objects.all())

        MatchUserContact.objects.create(user=user, contact=contact)

if __name__ == "__main__":
    populate()
