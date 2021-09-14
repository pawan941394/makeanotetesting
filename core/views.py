from django import http
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db.models.fields import NullBooleanField
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_list_or_404, get_object_or_404
from django.utils import tree
from .models import *
from django.contrib.auth.models import User, update_last_login
from django.contrib import messages
from .decorators import unauthenticated_user
from django.contrib.auth import authenticate
from django.contrib.auth import login as user_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import  force_bytes,  force_text, repercent_broken_unicode
from django.template.loader import render_to_string
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import *

# Create your views here.
def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate Your Account !'
    email_body = render_to_string('account/emailTemplate.html', {
        'user':user,
        'domain':current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token':generate_token.make_token(user)
    })
    email = EmailMessage(
        subject=email_subject, 
        body=email_body, 
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email]
        )
    email.send()

def home(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            n = NewsLetters(email=email)
            n.save()
            messages.success(request, "Thanks for subscribing our news letters.")
            return redirect('core:home')
        except Exception as e:
            messages.error(request, "Something went wrong !")
            return redirect('core:home')

    faqs = ""
    testimonials = ""
    context = {
        'faqs':faqs,
        'testimonials':testimonials,
    }
    return render(request, 'core/index.html', context)


@unauthenticated_user
def register(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        name=request.POST['name']
        # phone=request.POST['phone']
        pass1=request.POST['password']
        pass2 = request.POST['password1']
        user = User.objects.filter(username=username)
        mail = User.objects.filter(email=email)
        if user.exists() or mail.exists():
            messages.error(request, "Username or email already exists !")
            return redirect('core:register')

        if not username.isalnum():
            messages.error(request, "User name should only contain letters and numbers !")
            return redirect('core:register')
        if (pass1!= pass2):
             messages.error(request, "Passwords do not match !")
             return redirect('core:register')
        
        try:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = name
            myuser.save()
            context = {
                'registerd': 'registerd'
            }
            return render(request, 'account/signup.html', context)
        except Exception as e:
            messages.success(request, "Something went wrong. Try Again !")
            # return HttpResponse(e)
            return redirect('core:register')
    context = {}
    return render(request, 'account/signup.html', context)


@unauthenticated_user
def login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        try:
            if user is not None:
                verifyEmail = UserProfile.objects.get(user=user)
                is_verify = verifyEmail.is_email_verified
                try:
                    if not is_verify:
                        send_activation_email(user, request)
                        messages.success(request, 'Kindely check your email & verify it.')
                        return redirect('core:login')
                    else:
                        user_login(request, user)
                        return redirect("core:dashboard")
                except Exception as e:
                    # return HttpResponse(e)
                    messages.error(request, 'Something went wrong please. Try again.')
                    return redirect('core:login')
            else:
                messages.error(request, "Invalid credentials! Please try again.")
                return redirect("core:login")
        except Exception as e:
            # return HttpResponse(e)
            messages.error(request, 'Invalid Credentials !')
            return redirect('core:login')
    context = {}
    return render(request, 'account/login.html', context)

# @unauthenticated_user
def userLogout(request):
    user = request.user
    logout(request)
    messages.success(request, "Successfully logged out !")
    return redirect('core:login')

def aboutUs(request):
    context = {}
    return render(request, 'core/aboutUs.html', context)

def feedbacks(request):
    context = {}
    return render(request, 'core/feedbackform.html', context)
    
def contact(request):
    if request.method=='POST':
        try:
            name = request.POST['name']
            email = request.POST['email']
            subjec = request.POST['subject']
            msg = request.POST['message']
            c = Contact(name=name, email=email, suggestion=subjec, message=msg)
            c.save()
            context = {
                'submitted':'submitted'
            }
            return render(request, 'core/contact.html', context)
        except Exception as e:
            messages.success(request, "Something went wrong !")
            return redirect('core:contact')
    context = {}
    return render(request, 'core/contact.html', context)
    
# After Login Views    
@login_required(login_url='core:login')
def dashboard(request):
    try:
        titles = Title.objects.filter(user=request.user)
        notes = Note.objects.filter(user=request.user,at_dashboard=True)
        context = {
            'notes':notes,
            'titles':titles,
        }
        return render(request, 'AfterLogin/dashbord.html', context)
    except Exception as e:
        messages.error(request, "Something went wrong !")
        return HttpResponse(e)
        return redirect('core:dashboard')

@login_required(login_url='core:login')
def notes(request):
    try:
        titles = Title.objects.filter(user=request.user)
        context = {
            'titles':titles,
        }
        return render(request, 'AfterLogin/yourNotes.html', context)
    except Exception as e:
        messages.error(request, "Something went wrong !")
        return redirect('core:dashboard')

      

@login_required(login_url='core:login')
def dashboardFolder(request, str):
    try:
        title = Title.objects.get(id=str)
        folders = CustomFolder.objects.filter(title=title)
        context = {
            'folders':folders,
            'title':title
        }
        return render(request, 'AfterLogin/dashboardfolder.html', context)
    except Exception as e:
        # return HttpResponse(e)
        messages.success(request, "Something went wrong !")
        return redirect('core:dashboard')
    

@login_required(login_url='core:login')
def dashboardNotesShow(request, str):
    try:
        folder = CustomFolder.objects.get(id=str)
        notes = Note.objects.filter(custom_folder=folder)
        context = {
            'notes':notes,
            'folder':folder
        }
        return render(request, 'AfterLogin/dashboardNotesShow.html', context)
    except Exception as e:
        # return HttpResponse(e)
        return redirect('core:dashboard')
    

@login_required(login_url='core:login')
def favourite(request):
    favnotes = Note.objects.filter(user=request.user, is_favorite=True)
    print(favnotes)
    context = {
        'favorites':favnotes
    }
    return render(request, 'AfterLogin/favourite.html', context)

@login_required(login_url='core:login')
def notesDelete(request, id):
    try:
        note = Note.objects.get(id=id)
        note.delete()
        messages.success(request, 'Note deleted successfully !')
        return redirect('core:favourite')    
    except Exception as e:
        messages.success(request, 'Something Went wrong !')
        return redirect('core:favourite')    
        
@login_required(login_url='core:login')
def noteView(request, id):
    try:
        note = Note.objects.get(id=id)
        context = {
            'note':note
        }
        return render(request, 'AfterLogin/noteView.html', context) 
    except Exception as e:
        messages.error(request, 'Something went wrong !')
        return redirect('core:dashboard')


@login_required(login_url='core:login')
def passwordChange(request):
    if request.method=='POST':
        try:
            oldPass = request.POST['oldPassword']
            newPass = request.POST['newPassword']
            confPass = request.POST['confirmPassword']
            user = authenticate(request, username=request.user, password=oldPass)
            if newPass==confPass and user is not None:
                u = User.objects.get(username__exact=request.user)
                u.set_password(confPass)
                u.save()
                user = authenticate(request, username=request.user, password=confPass)
                user_login(request, user)
                messages.success(request, "Password change successfully !")
                return redirect('core:passwordChange')
            else:
                messages.error(request, "Password didn't match !")
                return redirect('core:passwordChange')
        except Exception as e:
            messages.error(request, "Something went wrong !")
            return redirect('core:passwordChange')
    context = {}
    return render(request, 'AfterLogin/passwordChange.html', context)


@login_required(login_url='core:login')
def privacyPolicy(request):
    context = {}
    return render(request, 'AfterLogin/privacyPolicy.html', context)
    

@login_required(login_url='core:login')
def profile(request):

    form = EditProfileForm()
    profile_form = ProfileForm()
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES,  instance=request.user.userprofile)

        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
    context = {
        # 'profile':profile,
        'form':form,
        'profile_form':profile_form,
    }
    return render(request, 'AfterLogin/userProfile.html', context)


@login_required(login_url='core:login')
def deleteAccount(request):
    try:
        u = User.objects.get(username=request.user)
        u.delete()
        messages.success(request, "Account deleted successfully !")
        return redirect('core:home')
    except Exception as e:
        messages.error(request, "Something Went wrong !")    
        return redirect('core:dashboard')

def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None
    if user and generate_token.check_token(user, token):
        verifyEmail = UserProfile.objects.get(user=user)
        verifyEmail.is_email_verified = True
        verifyEmail.save()
        messages.success(request,'Email verified, You can now login ')
        return redirect('core:login')
    else:
        messages.error(request, 'Something went wrong !')
        return redirect('core:login')

@login_required(login_url='core:login')
def homeNotes(request):
    form = NoteForm()
    if request.method =='POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.at_dashboard = True
            form.save()
            messages.success(request, 'Note Created Successfully. ')
            return redirect('core:dashboard')
    context = {
        'form':form
        }
    return render(request, 'AfterLogin/homeNotes.html', context)

@login_required(login_url='core:login')
def directory_create(request):
    if request.method == 'POST':
        try:
            directory_name = request.POST['directory_name']
            directry = Title(user=request.user, name=directory_name)
            directry.save()
            messages.success(request, 'Directory created successfully.')
            return redirect('core:dashboard')
        except Exception as e:
            messages.error(request, 'Something went wrong.')
            return redirect('core:dashboard')
    return redirect('core:home')


@login_required(login_url='core:login')
def folder_create(request, id):
    path = str(id)
    if request.method == 'POST':
        try:
            folder = request.POST['folder_name']
            title = Title.objects.get(id=id)
            f = CustomFolder(user=request.user, title=title, name=folder)
            f.save()
            messages.success(request, 'Folder created successfully.')
            return redirect('core:dashboardFolder', str=path)
        except Exception as e:
            messages.error(request, 'Something went wrong.')
            return redirect('core:dashboardFolder', str=path)
    return redirect('core:home')


@login_required(login_url='core:login')
def noteAdd(request, id):
    path = str(id)
    form = NoteForm()
    if request.method=='POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.custom_folder = CustomFolder.objects.get(id=id)
            form.save()
            messages.success(request, "Note created successfully.")
            return redirect('core:dashboardNotesShow', str=path)

    context = {
        'form':form
    }
    return render(request, 'AfterLogin/noteAdd.html', context)

@login_required(login_url='core:login')
def addFavourite(request,nid, fid):
    path = str(fid)
    try:
        fav = Note.objects.get(id=nid)
        fav.is_favorite = True
        fav.save()
        messages.success(request, 'Note added successfully to favorite.')
        return redirect('core:dashboardNotesShow', str=path)

    except Exception as e:
        messages.success(request, 'Something went wrong.')
        return redirect('core:dashboardNotesShow', str=path)


@login_required(login_url='core:login')
def deleteNote(request,nid, fid):
    path = str(fid)
    try:
        fav = Note.objects.get(id=nid)
        fav.delete()
        messages.success(request, 'Note deleted successfully.')
        return redirect('core:dashboardNotesShow', str=path)
    except Exception as e:
        messages.success(request, 'Something went wrong.')
        return redirect('core:dashboardNotesShow', str=path)

@login_required(login_url='core:login')
def directoryDelete(request, id):
    try:
        title = Title.objects.get(id=id)
        title.delete()
        messages.success(request, 'Directory deleted Successfully.')
        return redirect('core:dashboard')
    except Exception as e:
        messages.success(request, 'Something went wrong.')
        return redirect('core:dashboard')

@login_required(login_url='core:login')
def folderDelete(request, id, did):
    path = str(did)
    try:
        folder = CustomFolder.objects.get(id=id)
        folder.delete()
        messages.success(request, 'Directory deleted Successfully.')
        return redirect('core:dashboardFolder', str=path)
    except Exception as e:
        messages.success(request, 'Something went wrong.')
        return redirect('core:dashboardFolder', str=path)


@unauthenticated_user
def demoNotes(request):
    return render(request, 'demo/demoNotes.html')

@unauthenticated_user
def demoChecklist(request):
    return render(request, 'demo/demoChecklist.html')
    

def quillform(request):
    # context = {
    # }
    # return render(request, 'core/qillPost.html', context)
    return redirect('core:home')

    
@login_required(login_url='core:login')
def checklist(request):
    tasks = Task.objects.filter(user=request.user)
    context = {
        'tasks':tasks
    }   
    return render(request, 'AfterLogin/checklist.html', context)
    

@login_required(login_url='core:login')
def checklistAdd(request):
    user = request.user
    title = request.POST['title']
    t= Task(user=user,title=title )
    t.save()


    return redirect('core:checklist')

@login_required(login_url='core:login')
def checklistDelete(request, todo_id):
    todo = get_object_or_404(Task, pk=todo_id)
    todo.delete()

    return redirect('core:checklist')

@login_required(login_url='core:login')
def checklistUpdate(request, todo_id):
    todo = get_object_or_404(Task, pk=todo_id)
    isCompleted = request.POST.get('isCompleted', False)
    if isCompleted == 'on':
        isCompleted = True
    
    todo.isCompleted = isCompleted

    todo.save()
    return redirect('core:checklist')


@login_required(login_url='core:login')
def notesShow(request):
    allNotes = Note.objects.filter(user=request.user)
    context = {
        'allNotes':allNotes
    }
    return render(request, 'AfterLogin/notesShow.html', context)


import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders




@login_required(login_url='core:login')
def render_pdf_view(request, id):
    template_path = 'AfterLogin/pdf.html'
    note = Note.objects.get(id=id)
    context = {
        'note':note
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # download
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # view
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def dashboardFavourite(request, id):
    try:
        fav = Note.objects.get(id=id)
        fav.is_favorite = True
        fav.save()
        messages.success(request, 'Note added successfully to favorite.')
        return redirect('core:dashboard')

    except Exception as e:
        messages.success(request, 'Something went wrong.')
        return redirect('core:dashboard')