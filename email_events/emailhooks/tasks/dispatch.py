from email_events.celery import app
from emailhooks.handlers.dispatcher import PayloadDispatcher


@app.task
def event_dispatch(payload, signature):
    '''Celery task providing event dispatcher.
    
    :signature: Mandrill webhook recieved signature
    '''
    payload = PayloadDispatcher(payload, signature)
    return True