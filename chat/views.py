from django.shortcuts import render
from booksdb.models import UserBooks
from .models import ChatLine,TextMessage
from pusher import Pusher
from django.conf import settings
from home.models import CustomUser, FollowUser
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import DownloadLinkForm
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib


def mail_send(reciever,subject,body):
    fromaddr = settings.EMAIL_HOST_USER
    toaddr = reciever
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, settings.EMIAL_HOST_PASSWORD)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def pushNotification(request,email,data,time,img,event):
    channel = u"customuser_{pk}".format(
        pk=email
    )
    pusher = Pusher(app_id=settings.PUSHER_APP_ID,
                    key=settings.PUSHER_KEY,
                    secret=settings.PUSHER_SECRET)
    event_data = {
        'object' : data,
        'user': request.user.email
    }
    if time != None:
        event_data.update({'time' : time,'img' : img})
    pusher.trigger(
        [channel,],
        event,
        event_data
    )
    
def sendChatMessage(request,email):
    other = CustomUser.objects.get(email = email)
    try:
        chatLine = ChatLine.objects.get(Q(user_one = request.user,user_two = other) | Q(user_one = other,user_two = request.user))
    except ObjectDoesNotExist:
        chatLine = ChatLine.objects.create(user_one = request.user,user_two = other)
    finally:
        data = request.GET['text']
        textMessage = TextMessage.objects.create(chat = chatLine,text = data,sender = request.user,send = True)
        if textMessage.timestamp.strftime("%p") == "PM":
            ext = ' p.m.'
        else:
            ext = ' a.m.'
        timestamp = u"%s" % textMessage.timestamp.strftime("%b. %d, %Y, %l:%M") + ext
        img = u"%s" % request.user.profile_pic
        pushNotification(request,email,data,timestamp,img,u"update")
        
def recieved(request):
    other_email = request.GET['email']
    text = request.GET['text']
    sender = CustomUser.objects.get(email = other_email)
    chatLine = ChatLine.objects.get(Q(user_one = request.user,user_two = sender) | Q(user_one = sender,user_two = request.user))
    textMessages = TextMessage.objects.all().filter(sender = sender,chat = chatLine,text = text,read = False)
    for message in textMessages:
        message.read = True
        message.save()
    
def chat(request,email):
    history = ''
    obj = CustomUser.objects.get(email = email)
    try:
        chatLine = ChatLine.objects.get(Q(user_one = request.user,user_two = obj) | Q(user_one = obj,user_two = request.user))
    except ObjectDoesNotExist:
        chatLine = ChatLine.objects.create(user_one = request.user,user_two = obj)
    else:
        history = TextMessage.objects.all().filter(chat = chatLine)
        
    form = DownloadLinkForm(request.user,
        request.POST or None
    )
    if form.is_valid():
        userbook = UserBooks.objects.get(id = form.cleaned_data['ebookOption'])
        body = "Hey %s,\nBook : %s by %s\nSender : %s\nDownload Link : http://127.0.0.1:8000/media/%s" % (
            email,
            userbook.book.title,
            userbook.book.author,
            request.user,
            userbook.ebook
        )
        subject = "Download Link"
        mail_send(email,subject,body)
    context = {
        'obj' : obj,
        'history' : history,
        'form' : form
    }
    return render(request,'chats.html',context)
    
def chat_list(request):
    followed_by = FollowUser.objects.all().filter(user_followed = request.user)
    following = FollowUser.objects.all().filter(user_follower = request.user)
    chat_user = []
    
    for followedTuple in followed_by:
        for followingTuple in following:
            if followingTuple.user_followed == followedTuple.user_follower:
                chat_user.append(followingTuple.user_followed)
                break
    context = {
        'chat_user' : chat_user
    }
    return render(request,'chat_list.html',context)
    
def follow(request,email):
    other_user = CustomUser.objects.get(email = email) 
    FollowUser.objects.create(user_followed = other_user, user_follower = request.user)
    pushNotification(request,email,'is following you.',None,None,u'notify')
    return HttpResponseRedirect(reverse('library.views.seelibrary',kwargs={'email' : email}))
    
def unfollow(request,email):
    other_user = CustomUser.objects.get(email = email) 
    FollowUser.objects.get(user_followed = other_user, user_follower = request.user).delete()
    return HttpResponseRedirect(reverse('library.views.seelibrary',kwargs={'email' : email}))