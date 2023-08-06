from .messageBox import messageBox

def messages(request):
    return {'messageBox':messageBox}
