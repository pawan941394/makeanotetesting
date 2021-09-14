from .models import *

def contactDetails(request):
    try:
        contactDetails = ContactLink.objects.latest('-id')
        return {'contactDetails':contactDetails}
    except Exception as e:
        context = {}
        return context

def profileDetails(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        return {'profile':profile}
    except Exception as e:
        context = {}
        return context

def noCounter(request):
    try:
        folderNo = CustomFolder.objects.filter(user=request.user).count()
        filesNo = Note.objects.filter(user=request.user).count()
        favNo = Note.objects.filter(user=request.user, is_favorite=True).count()
        directoryNo = Title.objects.filter(user=request.user).count()
        context = {
            'folderNo':folderNo,
            'filesNo':filesNo,
            'favNo':favNo,
            'directoryNo':directoryNo,
        }
        return context
    except Exception as e:
        context = {}
        return context
