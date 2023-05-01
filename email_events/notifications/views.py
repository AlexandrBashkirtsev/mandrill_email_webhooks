from django.shortcuts import render


def index(request):
    '''Open events index.
    Renders simple template with websockets client, recieveing new
    open events.
    '''
    return render(request, "notifications/index.html")