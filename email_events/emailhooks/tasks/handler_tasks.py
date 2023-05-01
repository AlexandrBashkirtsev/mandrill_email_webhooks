from email_events.celery import app
from emailhooks.handlers.handlers import OpenEventHandler, DefaultEventHadler


@app.task
def handle_default_event(event):
    '''Default event handlig Celery task.

    :event: serialized event payload dictionary.
    '''
    handler = DefaultEventHadler(event)
    handler.handle()
    return True


@app.task
def handle_open_event(event):
    '''Open event handlig Celery task.
    
    :event: serialized event payload dictionary.
    '''
    handler = OpenEventHandler(event)
    handler.handle()
    return True