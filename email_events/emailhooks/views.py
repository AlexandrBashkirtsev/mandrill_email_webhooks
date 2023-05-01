from django.shortcuts import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from emailhooks.tasks.dispatch import event_dispatch


def index(request):
    template = loader.get_template('emailhooks/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


@csrf_exempt
def hooks(request):
    '''Mandrill webhook entrypoint.
    
    on :HEAD: provides HTTP status 200 for Mandrill webhook add and update
    on :POST: calls Celery payload dispatch task and return HTTP status 200
    '''
    if request.method == 'POST':
        # Celery task call
        print('Celery entrypoint is triggered')
        event_dispatch.delay(request.POST,
                             request.META['HTTP_X_MANDRILL_SIGNATURE'])
        return HttpResponse(status=200)
    
    elif request.method == 'HEAD':
        return HttpResponse(status=200)