# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User, Travel
from django.contrib import messages

def index(request):
    return render(request, "travelbuddy_app/index.html")

def register(request):

    check = User.objects.register(
        request.POST['name'],
        request.POST['username'],
        request.POST['email'],
        request.POST['password'],
        request.POST['confirmpassword']
    )

    if not check["valid"]:
        for error in check["errors"]:
            messages.add_message(request, messages.ERROR, error)
        return redirect("/")
    else:
        request.session["user_id"] = check["user"].id
        messages.add_message(request, messages.SUCCESS, "Registration Successful!!, {}".format(request.POST["username"]))
        return redirect('/')

def login(request):
    check = User.objects.login(
        request.POST['email'],
        request.POST['password']
    )

    if not check["valid"]:
        for error in check["errors"]:
            messages.add_message(request, messages.ERROR, error)
        return redirect("/")
    else:
        request.session["users_id"] = check["user"].id
        request.session["user_name"] = check["user"].username
        messages.add_message(request, messages.SUCCESS, "Login Successful!! Welcome, " "{}".format(check["user"].username))
        return redirect('/dashboard')

def dashboard(request):

    current = request.session["user_name"]
    current_id = request.session["users_id"]

    trips3 = Travel.objects.all()
    trips = Travel.objects.all()
    trips2 = Travel.objects.exclude(users=current_id)
    user = User.objects.get(id=request.session["users_id"])
    usertrips = user.manyusers.all()

    print usertrips
    

    # current = {
    #     "currentuser": check["user"].id
    # }

    data = {
        "trips": trips,
        "current": current,
        "current_id": current_id,
        "trips2": trips2,
        "trips3": trips3,
        "usertrips": usertrips,
    }

    return render(request, "travelbuddy_app/dashboard.html", data)

def logout(request):
    request.session.clear()
    messages.add_message(request, messages.SUCCESS, "Until Next Time!!")
    return redirect("/")

def travel(request):
    return render(request, "travelbuddy_app/travel.html")

def add_travel(request):

    check = Travel.objects.addTravel(
        request.POST['destination'],
        request.POST['plan'],
        request.POST['start'],
        request.POST['end'],
        request.session["users_id"]
    )

    if not check['valid']:
        for error in check['errors']:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/travel')

    else:
        messages.add_message(request, messages.SUCCESS, "Added successfully!")

    # request.session['user_id'] = check['user'].id
    return redirect("/dashboard")


def details(request, id):
    # current_id = request.session["users_id"]
    test = Travel.objects.get(id=id).users_id
    usersjoining = User.objects.get(id=test)

    jeez = Travel.objects.get(id=id)
    # jeez2 = jeez.manyusers.all()
    # jeez3 = jeez2[0].name

    jeez2 = jeez.manyusers.all()

    print jeez2

    # print test
    # jesus = test.manyusers.filter(usersjoining)
    # print jesus

    

    data = {
        "test": test,
        "usersjoining": usersjoining,
        "jeez2": jeez2
    }
    return render(request, "travelbuddy_app/details.html", data)

def home(request):
    return redirect("/dashboard")

def letsgo(request, id):
    # print id
    request.session['id'] = id
    test = Travel.objects.get(id=id)
    user = User.objects.get(id=request.session["users_id"])

    test.manyusers.add(user)
    # print request.session['id']
    return redirect("/dashboard")
    # return render(request, "travelbuddy_app/dashboard.html", data2)

