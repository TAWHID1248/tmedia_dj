from django.shortcuts import render
from django.http import HttpResponse




# Create your views here.

rooms = [
    {
        'id': 1,
        'name': 'Room 1',
        'description': 'This is Room 1',
        'price': 200
    },
    {
        'id': 2,
        'name': 'Room 2',
        'description': 'This is Room 2',
        'price': 300
    },
    {
        'id': 3,
        'name': 'Room 3',
        'description': 'This is Room 3',
        'price': 400
    }
]

def home(request):
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
    context = {'room': room}
    return render(request, 'base/room.html', context)