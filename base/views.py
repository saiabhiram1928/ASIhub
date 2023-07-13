from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.db.models import Q
from  .models import Room
from  .models import Topic
from  .models import Messages
from  .models import Profile
from  .forms import RoomForm
from  .forms import ProfileForm
from  .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate , login ,logout
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def home(request):
    query = request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms  = Room.objects.all().filter(
        Q(topic__name__contains = query) | Q(name__contains = query)| Q(description__contains = query) |Q(host__username = query)
        ).order_by('-id')
    count = Room.objects.all().count()
    topics = Topic.objects.all().order_by('-rooms_count')[0:5]
    msgs = Messages.objects.filter(Q(room__topic__name__icontains= query)).order_by('-created') [0:5]
    show_profile_link = True
    paginator = Paginator(rooms, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'base/home.html' , {'rooms' : rooms , 'topics':topics , 'count':count ,'msgs':msgs , 'show_profile_link':show_profile_link , 'page_obj': page_obj})
def room(request , pk):
    data = Room.objects.get(id= pk)
    room_messages = Messages.objects.filter(room = pk).order_by('created')
    participants = data.participants.all()
    user_is_participant = 0
    for participant in participants:
        if participant.username == request.user.username :
            user_is_participant = 1
    #another way of doing it is to get all the childrens of a parent in forigen key is
    #room_messages = Room.messages_set.all()
    if request.method == 'POST':
         room_message = Messages(user= request.user , room = data , text = request.POST.get('message'))
         room_message.save()
         return redirect('room',pk)
    return render(request, 'base/room.html' , {'room' : data, 'room_messages' : room_messages , 'participants':participants , 'user_is_participant' : user_is_participant})
@login_required(login_url = 'login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        form  = RoomForm(request.POST)
        if form.is_valid():
            form_topic = form.cleaned_data['topic']
            topic= Topic.objects.get(name = form_topic)
            topic.rooms_count =  topic.rooms_count+1
            topic.save()
            room = form.save(commit = False)
            room.host = request.user
            room.save()
            room = Room.objects.get(name = form.cleaned_data['name'])
            room.participants.add(request.user)
            return redirect('home')

    return render(request, 'base/room_form.html' , {'form' : form , 'topics' : topics})
@login_required(login_url = 'login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room)
    if request.user != room.host:
        return redirect('home')
    if request.method == 'POST':
        form = RoomForm(request.POST , instance = room)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'base/room_form.html', {'form' : form})
@login_required(login_url = 'login')
def deleteRoom(request, pk):
    room = Room.objects.get(id = pk)
    topic = Topic.objects.get(name = room.topic)
    topic.rooms_count =  topic.rooms_count-1
    if request.user != room.host:
        return redirect('home')
    room.delete()
    return redirect('home')
def loginUser(request):
    page = 'login'
    if request.user.is_authenticated :
        return redirect('home')
    if request.method == 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "username is invalid")
            return redirect('login')
        user = authenticate(request, username = username ,password= password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else : 
            messages.error(request, "please check password")
    return render(request, 'base/login_register.html' , {'page' : page} )
def logoutUser(request):
    logout(request)
    return redirect('home')
def register(request):
    page = 'register'
    form  = CustomUserCreationForm()
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            user= form.save(commit =False)
            user.username = user.username.lower()
            user.save()
            login(request , user)
            return redirect('home')
        else:
           messages.error(request, form.errors)
    return render(request, 'base/login_register.html', {
        'page': page,
        'form': form    
    })
@login_required(login_url = 'login')
def joinRoom(request , pk):
    room = Room.objects.get(id=pk)
    room.participants.add(request.user)
    return redirect('room',pk)
@login_required(login_url = 'login')
def delete_msg(request, pk):
    room_msg = Messages.objects.get(id =pk)
    print(room_msg.room.host.username)
    if request.user != room_msg.user and room_msg.room.host.username != request.user.username:
        return redirect('home')
    room_msg.delete()
    return redirect('room' , room_msg.room.id)
@login_required(login_url = 'login')
def profile(request , pk):
    query = request.GET.get('q') if request.GET.get('q')!=None else ''
    user  = User.objects.get(id=pk)
    rooms = user.room_set.all().filter(Q(topic__name__contains = query))
    count = user.room_set.all().count()
    show_profile_link =False
    topics = Topic.objects.all()
    profile = Profile.objects.get(user = request.user)
    topics_count={}
    for topic in topics:
        topics_count[topic] = Room.objects.filter(Q(host= request.user) & Q(topic =topic )).count()
    msgs = user.messages_set.all().order_by('-created')[0:5]
    return render(request, 'base/profile.html' , {'user':user , 'rooms' : rooms , 'show_profile_link' : show_profile_link , 'msgs' : msgs ,'count':count , 'topics_count' :topics_count , 'profile' : profile})
def go_back(request):
    previous_page = request.META.get('HTTP_REFERER')
    print(previous_page)
    return redirect(previous_page)
@login_required(login_url = 'login')
def updateUser(request) : 
    form = UserForm(instance = request.user)
    if request.method == 'POST':
        form = UserForm(request.POST , instance = request.user)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('profile' , pk = request.user.id )
        else :
            messages.error(request, form.errors)
    return render(request, 'base/update_user.html' , {'form': form})
def topicsPage(request):
    query = request.GET.get('q') if request.GET.get('q')!=None else ''
    topics = Topic.objects.all().filter(name__contains = query)
    count = Room.objects.all().count()
    return render(request , 'base/topics.html' , {'topics' : topics , 'count':count})
def activityPage(request):
    msgs = Messages.objects.all().order_by('-created')[0:10]
    return render(request , 'base/activity.html' ,{'msgs' : msgs})

@login_required(login_url = '/login')
def updateProfile(request):
    profile ,created = Profile.objects.get_or_create(user = request.user)
    if request.method == 'POST':
        profile.bio = request.POST.get('bio')
        profile.profile_pic = request.FILES.get('avatar')
        print(profile.profile_pic)
        profile.save()
        return redirect('profile',request.user.id)  
    return render(request , 'base/settings.html' , {'profile' : profile } )