# Mandrill emails tracking application

This code provides application structure for Mandrill transactional email events handling.
Web-framework is Django, events are handled with Celery and Redis. Notifications are handled with Channels and Redis.

## Application architecture

This application webhook entrypoint is `hooks/` view, that recieves webhook, dispatches it with Celery task and gives Mandrill response that webhook recieved.
Celery dispathing task creates `PayloadDispatcher` object, that checks webhook authenticity and dispatches appropriate handler for recieved events with Celery handling tasks. If no custom handling provided - triggers default handling procedure (basically, save payload to permanent storage)
Each task serializes payload in custom handler class instance, then calls its `handle()` method.

For `open` event `OpenEventHandler` class is provided. `OpenEventHandler` is linked with Django model `OpenEvent` for permanent storage. `OpenEventHandler` class provides additional steps to handle() procedure with more serialization (email message) and connection to Channels/Redis layer for notifications. Each new `open` event goes through Channels/Redis layer and is being sent to websocket client.

Django application structure:

- `emailhooks` app handles Mandrill webhooks.
- `notifications` app handles notifications (`open` event websocket notification is implemented).

`emailhooks.handlers` module contains `PayloadDispatcher` class and handler classes.
`emailhooks.tasks` module contains Celery tasks.

`notifications.consumers` module contains `Channels` websocket consumer for `open` event.