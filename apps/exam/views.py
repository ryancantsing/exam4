from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from .models import Users, Items
from django.contrib import messages
from django.db.models import Count

def index(request):
    return render(request, "exam/index.html")
def dashboard(request):
    user = Users.objects.get(id=request.session['user_id'])
    wished_items = user.wished_items.all()
    other_wishs = Items.objects.exclude(wished_at=user)
    context = {
    'user' : user,
    'wished_items' : wished_items,
    'other_wishs' : other_wishs
    'users' : Users.objects.get('')
    }
    return render (request, "exam/dashboard.html", context)
def wish_items(request, item_id):
    item = Items.objects.get(id=item_id)
    people_who_wants= item.wished_at.annotate(people_want = Count('id'))
    context = {
        'item' : item,
        'people_who_wants' : people_who_wants,
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
    else:
        request.session['user_id'] = result.id
        messages.success(request, "Successfully registered!")
        return redirect('/dashboard')

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
    user= Users.objects.get(id=request.session['user_id'])
    result = Items.objects.validate_item(request.POST, user)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/create')
    else:
        user.wished_items.add(result.id)        
        return redirect('/dashboard')
        
def add_to_list(request, item_id):
    user=Users.objects.get(id=request.session['user_id'])
    user.wished_items.add(item_id)
    
    
    return redirect('/dashboard')
def remove_from_list(request, item_id):
    user=Users.objects.get(id=request.session['user_id'])
    user.wished_items.remove(item_id)

    return redirect('/dashboard')
