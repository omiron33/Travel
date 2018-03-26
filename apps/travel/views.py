from django.shortcuts import render, redirect
from .models import User, Destination
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    if 'id' in request.session.keys():
        return redirect ('/travels')
    return render(request, "travel/home.html")

def reg(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        userpass = request.POST['pw']
        hashpass = bcrypt.hashpw(userpass.encode(), bcrypt.gensalt())
        User.objects.create(name=request.POST['name'], username=request.POST['username'],  password=hashpass)
        temp = User.objects.last()
        request.session['id'] = temp.id
        request.session['name'] = temp.name
        request.session['username'] = temp.username
    return redirect ('/travels')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        temp = User.objects.filter(username = request.POST['loguser'])
        request.session['name'] = temp[0].name
        request.session['username'] = temp[0].username
        request.session['id'] = temp[0].id
        return redirect("/travels")

def travels(request):
    context = {
        'destinations' : Destination.objects.filter(creator_id = request.session['id']),
        'joineddestinations' : Destination.objects.filter(joiners = request.session['id']),
        'others' : Destination.objects.exclude(creator_id = request.session['id']).exclude(joiners = request.session['id'])
    }

    return render(request, "travel/dashboard.html", context)

def logout(request):

    request.session.flush()

    return redirect ('/')

def add(request):

    return render(request, "travel/add.html")

def addproc(request):
    errors = User.objects.trip_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/travels/add')
    else:
        Destination.objects.create(location=request.POST['destination'], desc=request.POST['description'],start_date=request.POST['start'], end_date=request.POST['end'], creator_id=request.session['id'])
        return redirect ('/travels')

def destinationshow(request, id):
    data = Destination.objects.get(id = id)
    context = {
        'destination' : data,
        'joiners' : data.joiners.all()
    }
    return render (request, "travel/destination.html", context)

def join(request, id):
    place = Destination.objects.get(id = id)
    person = User.objects.get(id = request.session['id'])
    person.joined_destinations.add(place)
    return redirect ('/travels')