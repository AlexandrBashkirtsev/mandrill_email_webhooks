from django.db import models


class EmailMessage(models.Model):
    '''Abstract template for message models.
    '''
    _id = models.CharField(max_length=100)
    ts = models.IntegerField(blank=True)
    email = models.EmailField(blank=True)
    sender = models.EmailField(blank=True)
    subject = models.CharField(max_length=1000)

    class Meta:
        abstract = True


class OpenMessage(EmailMessage):
    ''''msg' model implementation for 'open' event'''
    clicks = models.TextField(blank=True)
    opens = models.TextField(blank=True)


class EmailEvent(models.Model):
    '''Abstract template for event models'''
    _id = models.CharField(max_length=100)
    ts = models.IntegerField()
    event = models.CharField(max_length=30)
    msg = models.TextField(blank=True)

    class Meta:
        abstract = True


class DefaultEvent(EmailEvent):
    '''Default implementation of EmailEvent model'''
    pass


class OpenEvent(EmailEvent):
    '''Event model implementation for 'open' event'''
    ip = models.CharField(blank=True,
                          max_length=46)
    user_agent = models.TextField(blank=True)
    location = models.TextField(blank=True)
    msg = models.OneToOneField(OpenMessage,
                               on_delete=models.CASCADE)