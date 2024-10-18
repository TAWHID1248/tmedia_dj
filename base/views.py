from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate ,login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic, Message
from . forms import RoomForm
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

# rooms = [
#     {
#         'id': 1,
#         'name': 'Room 1',
#         'description': 'This is Room 1',
#         'price': 200
#     },
#     {
#         'id': 2,
#         'name': 'Room 2',
#         'description': 'This is Room 2',
#         'price': 300
#     },
#     {
#         'id': 3,
#         'name': 'Room 3',
#         'description': 'This is Room 3',
#         'price': 400
#     }
# ]


def loginPage(request):

    page = 'login'
    
    if request.user.is_authenticated: # eta ken dise jani na
        return redirect('home') # eta ken dise jani na
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
            
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User Doesn't exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "username or password isn't correct")



    context = {'page' : page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    
    return render(request, 'base/login_register.html', {'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) |
        Q(description__icontains=q) 
        )
    
    room_count = rooms.count()

    topics = Topic.objects.all()

    room_messages = Message.objects.filter(room__topic__name__icontains=q)

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    
    room_messages = room.message_set.all().order_by

    participants = room.participants.all()

    if request.method == 'POST':
        messages = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)





@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topic = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topic': topic}
    return render(request, 'base/profile.html', context)


def updateRoom(request, pk):
    room = Room.objects.get(pk=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, pk):
    room = Room.objects.get(pk=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='/login')
def deleteMessage(request, pk):
    message = Message.objects.get(pk=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed to delete')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': message})