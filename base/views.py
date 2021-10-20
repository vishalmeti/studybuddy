from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from .models import Room,Message,Topic
from .forms import RoomForm,MessageForm,TopicForm

# Create your views here.


def loginpage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, 'User doesnot exists')
        
        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            messages.success(request, 'Login Successfull')
            return redirect('home')
        else:
            messages.error(request, 'Error occured during Login')
    context={'page':page}
    return render(request,'base/loginpage.html',context)

def registerPage(request):
    form=UserCreationForm()
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration')

    context={'form':form}
    return render(request,'base/loginpage.html',context)

def userLogout(request):
    
    logout(request)
    messages.success(request, 'Logout Successfull')
    return redirect('home')

def home(request):
    if request.GET.get('q'):
        q=request.GET.get('q')
        query=Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(desc__icontains=q) )
    else:
        query=Room.objects.all()[0:10]
    roomCount=Room.objects.all().count()
    topics=Topic.objects.all().order_by('id')
    if request.GET.get('q'):
        recentMsg=Message.objects.filter(Q(room__topic__name__icontains=q)).order_by('-created')[0:7]
    else:
        recentMsg=Message.objects.all().order_by('-created')[0:15]

    temp={'contexts':query,'topics':topics,'roomCount':roomCount,'recentMsg':recentMsg}
    return render(request,'base/home.html',temp)

def about(request):
    return render(request,'base/about.html')

def room(request,pk ):
    room=Room.objects.get(id=pk)
    roomId=room.id
    room.participants.add(room.host)
    # message=Message.objects.filter(room=roomId)

    if request.method=='POST':
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('msg')
        )  
        room.participants.add(request.user) 
        return redirect('room',pk=room.id)


    participants=room.participants.all()
    message=Message.objects.filter(room=roomId).order_by('-created')[0:13]
    # chats=Room.objects.get()
    context={'room':room,'message':message,'participants':participants}
    return render(request, 'base/room.html',context)

@login_required(login_url='login')      
def createRoom(request):
    # form=RoomForm()
    
    # if request.method== 'POST':
    #     form=RoomForm(request.POST)
    #     print(request.user.id)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('home')
    form = RoomForm()
    topics = Topic.objects.all()
    print(topics)
    if request.method == 'POST':
        topic_id = request.POST.get('topic')
        topic = Topic.objects.get(id=topic_id)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            desc=request.POST.get('desc'),
        )
        messages.success(request, 'Room Created')
        return redirect('home')
    
    contest={'form':form}
    return render(request,'base/Form.html',contest)


@login_required(login_url='login')  
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.user.username != room.host.username:
        return HttpResponse('You are not allowed here!!')
    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room Updated')
            return redirect('home')
    context={'form':form}
    return render(request,'base/updateRoom.html',context)

@login_required(login_url='login')  
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user.username != room.host.username:
        return HttpResponse('You are not allowed here!!')
    if request.method=='POST':
        room.delete()
        messages.success(request, 'Room Deleted')
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

@login_required(login_url='login')  
def deleteMessage(request,pk):
    msg=Message.objects.get(id=pk)
    room=msg.room
    if request.user.username != msg.user.username:
        return HttpResponse('You are not allowed here!!')
    if request.method=='POST':
        # msg.delete()
        curr=request.user
        msg.body='*** This message was deleted ***'
        msg.save()
        messages.success(request, 'Message Deleted')
        return redirect('room',pk=room.id)
    return render(request,'base/delete.html',{'obj':msg})


    
@login_required(login_url='login')  
def createTopic(request):
    form=TopicForm()
    if request.method=='POST':
        form=TopicForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New topic created')
            return redirect('home')
    return render(request,'base/newtopic.html',{'form':form})


