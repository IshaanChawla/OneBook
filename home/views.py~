from booksdb.models import Books
from django.shortcuts import render,render_to_response,get_object_or_404
from django.http import HttpResponseRedirect
from .forms import LogInForm,SignUpForm
from .models import CustomUser,UserProfile
from django.contrib.auth import authenticate, login
from django.conf import settings
import hashlib, datetime, random
from django.utils import timezone
from django.core.urlresolvers import reverse
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
# Create your views here.
form1 = LogInForm()
form2 = SignUpForm()
wtg = 0

def register_confirm(request, activation_key):
    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
    #check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        return render_to_response('confirm_expired.html')
    #if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()
    if request.user.is_authenticated():
        HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    return render_to_response('confirm.html')

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

def sendActivationCode(request):
    email = request.user.email 
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
    activation_key = hashlib.sha1(salt+email).hexdigest()            
    key_expires = datetime.datetime.today() + datetime.timedelta(2)
    
    #Calling the newly created user
    user=CustomUser.objects.get(email=email)
    
    #Creating a New Profile
    new_profile = UserProfile(user=user, activation_key=activation_key, key_expires=key_expires)
    new_profile.save()
    
    #Sending Email for conformation
    email_subject = 'Account confirmation'
    email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
    48hours http://127.0.0.1:8000/confirm/%s" % (email, activation_key)
    mail_send(email,email_subject,email_body)
    
    request.user.is_active = False
    request.user.save()
    
    return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    
def authenticateUser(email,password):
    user = authenticate(email=email, password=password)
    if user is not None:
        return user
    return

def getEmailPassword(form):
    email = form.cleaned_data['email']
    password = form.cleaned_data['password']
    return email,password
    
def signin(request):
    if request.user.is_anonymous():
        state = ''
        form1 = LogInForm(request.POST or None)
        if form1.is_valid():
            email, password = getEmailPassword(form1)
            user = authenticateUser(email,password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
            state = 'Email and/or Password Do Not Match'
        book1,book2,book3,book4,book5,book6 = Books.objects.all().order_by('?')[:6]
        print book1.book_pic
        context = {
            'state' : state,
            'form1' : form1,
            'form2' : form2,
            'wtg' : wtg,
            'book1' : book1,
            'book2' : book2,
            'book3' : book3,
            'book4' : book4,
            'book5' : book5,
            'book6' : book6
        }
        return render(request,'home.html',context)
    else:
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

def signup(request):
    if request.user.is_anonymous():
        form2 = SignUpForm(request.POST or None)
        if form2.is_valid():
            email, password = getEmailPassword(form2)
            CustomUser.objects.create_user(
                email = email,
                password = password,
                full_name = form2.cleaned_data['full_name']
            )
            user = authenticateUser(email,password)
            if user is not None:    
                login(request, user)
                return HttpResponseRedirect(reverse('home.views.sendActivationCode'))
        else:
            wtg = 1
        book1,book2,book3,book4,book5,book6 = Books.objects.all().order_by('?')[:6]
        context = {
            'form1' : form1,
            'form2' : form2,
            'wtg' : wtg,
            'book1' : book1,
            'book2' : book2,
            'book3' : book3,
            'book4' : book4,
            'book5' : book5,
            'book6' : book6
        }
        return render(request,'home.html',context)
    else:
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
