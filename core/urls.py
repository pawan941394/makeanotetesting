from django.urls import path
from .views import *
app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('aboutUs', aboutUs, name='aboutUs'),
    path('feedbacks', feedbacks, name='feedbacks'),
    path('contact', contact, name='contact'),
    # user paths
    path('register', register, name='register'),
    path('logout', userLogout, name='logout'),
    path('login', login, name='login'),
    # path('notes', notes, name='notes'),
    # Dashboard related urls
    path('homeNotes', homeNotes, name='homeNotes'),
    path('notesShow', notesShow, name='notesShow'),
    path('dashboard', dashboard, name='dashboard'),
    path('dashboardFolder/<str:str>', dashboardFolder, name='dashboardFolder'),
    path('dashboardNotesShow/<str:str>', dashboardNotesShow, name='dashboardNotesShow'),

    #Note related urls
    path('noteAdd/<int:id>', noteAdd, name='noteAdd'),
    path('noteView/<int:id>', noteView, name='noteView'),
    path('notesDelete/<int:id>', notesDelete, name='notesDelete'),
    path('directoryDelete/<int:id>', directoryDelete, name='directoryDelete'),
    path('folderDelete/<int:id>/<int:did>', folderDelete, name='folderDelete'),
    path('deleteNote/<int:nid>/<int:fid>', deleteNote, name='deleteNote'),
    path('favourite', favourite, name='favourite'),
    path('addFavourite/<int:nid>/<int:fid>', addFavourite, name='addFavourite'),
    path('dashboardFavourite/<int:id>', dashboardFavourite, name='dashboardFavourite'),
    
    # check list related urls
    path('checklist', checklist, name='checklist'),
    path('check_list<int:todo_id>/delete', checklistDelete, name='delete'),
    path('check_list<int:todo_id>/update', checklistUpdate, name='update'),
    path('check_list/add', checklistAdd, name='add'),

    # user relatedurls
    path('passwordChange', passwordChange, name='passwordChange'),
    path('privacyPolicy', privacyPolicy, name='privacyPolicy'),
    path('profile', profile, name='profile'),
    path('deleteAccount', deleteAccount, name='deleteAccount'),
    path('activate_user/<uidb64>/<token>', activate_user, name='activate'),
    path('directory_create', directory_create, name='directory_create'),
    path('folder_create/<int:id>', folder_create, name='folder_create'),
    path('demoChecklist', demoChecklist, name='demoChecklist'),
    path('demoNotes', demoNotes, name='demoNotes'),
    path('downloadPdf/<int:id>', render_pdf_view, name='downloadPdf'),
]
