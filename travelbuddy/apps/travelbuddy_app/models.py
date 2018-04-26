from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')

class TravelManager(models.Manager):
    def addTravel(self, destination, plan, start, end, users_id):
        errors = []
        if len(destination) <1:
            errors.append("You must be going somewhere")
        if len(start) <1:
            errors.append("You must start somewhere!")
        else:
            x = datetime.strptime(start, "%Y-%m-%d")
            if x < datetime.now():
                errors.append("You must start in the future!!")
        if len(end) <1:
            errors.append("You must end the trip!")
        elif end < start:
            errors.append("You can't time travel yet")
        if len(plan) <1:
            errors.append("You have to have a plan in life")
        response = {
            "trip": None,
            "errors": errors,
            "valid": False
        }

        print start

        if len(errors) == 0:
            response['valid'] = True
            response['trip'] = Travel.objects.create(
                destination=destination,
                start_date=start,
                end_date=end,
                plan=plan,
                users_id=users_id
            )
        return response

class UserManager(models.Manager):
    def register(self, name, username, email, password, confirm):
        errors = []
        if len(name) < 2:
            errors.append("Name must be 2 characters or more")

        if len(username) <2:
            errors.append("Username must be 2 characters or more")

        if len(email) <2:
            errors.append("Email must be 2 characters or more")
        elif not EMAIL_REGEX.match(email):
            errors.append("Invalid email")
        else:
            usersMatchingEmail = User.objects.filter(email=email)
            if len(usersMatchingEmail) > 0:
                errors.append("Email already in use")

        if len(password)<1:
            errors.append("Password is required")
        elif len(password)<8:
            errors.append("Password must be 8 characters or more")
        if len(confirm) <1:
            errors.append("Confirm Password is required")
        elif password != confirm:
            errors.append("Confirm Password must match Password")

        response = {
            "errors": errors,
            "valid": True,
            "user": None
        }

        if len(errors) >0:
            response["valid"] = False
            # response["errors"] = errors
            return response

        else:
            response["user"] = User.objects.create(
            name= name,
            username=username,
            email=email,
            password=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        )



        return response

    def login(self, email, password):
        errors = []

        if len(email) <1:
            errors.append("Email must be 2 characters or more")
        elif not EMAIL_REGEX.match(email):
            errors.append("Invalid email")
        else:
            usersMatchingEmail = User.objects.filter(email=email)
            if len(usersMatchingEmail) == 0:
                errors.append("Unknown email")

        if len(password)<1:
            errors.append("Password is required")
        elif len(password)<6:
            errors.append("Password must be 6 characters or more")

        # print errors

        response = {
            "errors": errors,
            "valid": True,
            "user": None,
        }

        if len(errors) == 0:
            if bcrypt.checkpw(password.encode(), usersMatchingEmail[0].password.encode()):
                response["user"] = usersMatchingEmail[0]
            else:
                errors.append("Incorrect Password")

        if len(errors) > 0:
            response["errors"] = errors
            response["valid"] = False

        return response


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email =models.CharField(max_length=255)
    password =models.CharField(max_length=255)
    confirm =models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

class Travel(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    manyusers = models.ManyToManyField(User, related_name="manyusers")
    users = models.ForeignKey(User, related_name="users")

    objects = TravelManager()

# class Trip(models.Model):
#     name = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
