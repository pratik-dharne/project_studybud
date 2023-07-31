from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from . models import Room,Topic,Message,User
from . forms import RoomForm,UserForm,MyUserCreationForm


# Create your views here.


# rooms=[
# 	{'id':1,'room':'python'},
# 	{'id':2,'room':'java'},
# 	{'id':3,'room':'C#'},
# ]
def login_page(request):

    page='login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email=request.POST.get('email').lower()  #getting user credentials
        password=request.POST.get('password')
    
        try:
            user=User.objects.get(email=email)  #getting to know if the user exsit or not if exist user object is store inside
        #user if not then error is thrown that is why we are using try block
        except:
            messages.error(request,'User does not exist') #display user not exsit flash message
        else:
            user = authenticate(request,email=email,password=password)#user is checked returns none or AbstractBaseUser(pratik-username) object if
        #username and password is matched
            if user is not None:
                login(request,user) #login and session by using AbstractBaseUser 
                return redirect('home')
            else:
                messages.error(request,'Incorrect Username or Password')

    return render(request,'base\login_register.html',{'page':page})

def logout_page(request):
    
    logout(request)
    return redirect('home')

def register_page(request):

    form = MyUserCreationForm()
   
    if request.method =='POST': 
       
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An Error Occurred during registration') 

    return render(request,'base/login_register.html',{'form':form})


def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
                                Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(description__icontains=q)|
                                Q(host__username__icontains=q)
                                )
    
    topics=Topic.objects.all()[0:5]

    room_count = rooms.count()

    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )

    context={'rooms':rooms,'topics':topics,'room_count':room_count,"room_messages":room_messages}
    
    return render(request,'base/home.html',context=context)

def room(request,pk):

    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all()
    participants=room.participants.all()

    if request.method=='POST':
        Message.objects.create(
            owner=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context={'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context=context)


def userprofile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages=user.message_set.all()
    topics = Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}

    return render(request,'base/profile.html',context)

@login_required(login_url='login')
def createroom(request):

    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )

        # form = RoomForm(request.POST) #save the data inside the form variable
        # if form.is_valid():# check all the inbuilt validations
        #     room=form.save(commit=False)
        #     room.host=request.user
        #     room.save()
        return redirect('home')
        
  
    context={'form':form,'topics':topics,'room':room}
    

    return render(request, "base/room_form.html",context)

@login_required(login_url='login')
def updateroom(request,pk):

    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room) #getting the required record and saving it inside the form varaiable
    topics=Topic.objects.all()

    if request.user != Room.host:
        HttpResponse("you are not allowed to do that!")

    if request.method == 'POST':
        
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic= topic
        room.description=request.POST.get('description')
        room.save()


        # form = RoomForm(request.POST,instance=room) #which specific record to update is decided by instance=room and the updated data is saved inside the form variable
        # if form.is_valid():
        #     form.save()
        return redirect('home')

    context={'form':form,'topics':topics,'room':room}

    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteroom(request,pk):

    room = Room.objects.get(id=pk)
    
    if request.user != Room.host:
         HttpResponse("you are not allowed to do that!")
 
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context={'obj':room}

    return render(request,'base/delete.html',context)


@login_required(login_url='login')
def deletemessage(request,pk):

    message = Message.objects.get(id=pk)
    roomid= message.room.id
    
    if request.user != message.owner:
         HttpResponse("you are not allowed to do that!")
 
    if request.method == 'POST':
        message.delete()
        return redirect('room',pk=roomid)

    context={'obj':message}

    return render(request,'base/delete.html',context)

@login_required(login_url='login')
def updateuser(request):

    user=request.user
    form = UserForm(instance=user)

    if request.method == 'POST':

        form = UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile' ,pk=user.id)

    return render(request,'base/update-user.html',{'form':form})


def topicspage(request):

    q=request.GET['q'] if request.GET.get('q') != None else '' 
    topics=Topic.objects.filter(
        Q(name__icontains=q)
    )
    return render(request,'base/topics.html',{'topics':topics})


def activitypage(request):

    room_messages = Message.objects.all


    return render(request,'base/activity.html',{'room_messages':room_messages})



