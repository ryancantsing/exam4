from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from .models import Users, Items
from django.contrib import messages


def index(request):
    return render(request, "exam/index.html")
def dashboard(request):
    user = Users.objects.get(id=request.session['user_id'])
    wished_items = user.wished_for.values('name', 'added_by', 'created_at')
    other_wishs = wished_items.values('name', 'added_by', 'created_at')
    context = {
    'user' : user,
    'wished_items' : wished_items,
    'other_wishs' : other_wishs
    }
    return render (request, "exam/dashboard.html", context)
def wish_items(request):
    items = Items.objects.values('id','name', 'wished_for')
    context = {
    'items' : items,
    }
    return render(request, 'exam/wish_items.html', context)
def create(request):
    return render(request, "exam/create.html")
def success(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    context = {
        'user': Users.objects.get(id=request.session['user_id'])
    }
    return render(request, 'exam/success.html', context)


def register(request):
    result = Users.objects.validate_registration(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully registered!")
    return redirect('/success')

def login(request):
    result = Users.objects.validate_login(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    request.session['username'] = result.username
    return redirect('/dashboard')

def logout(request):
    del request.session['user_id']
    return redirect('/')
def create_item(request):
    result = Items.objects.validate_item(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/create')
    else:
        name = Items.objects.get(name=request.POST['name'])
        added_by = Users.objects.get(id=request.session['user_id'])
        wished_for = Users.objects.get(id=request.session['user_id'])
        Items.objects.create(name=name, added_by=added_by, wished_for=wished_for)
        return redirect('/dashboard')
def add_to_list(request):
    wished_for = Users.objects.get(id=request.session['user_id'])
    Items.objects.create(wished_for=wished_for)
    return redirect('/dashboard')
def remove_from_list(request, item_id):
    Users.objects.get(id=request.session['user_id']).wished_for.delete(item_id)
    return redirect('/dashboard')
