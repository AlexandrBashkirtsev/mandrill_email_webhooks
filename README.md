# Mandrill emails tracking application

## Challenge

Emails are sent out through Mandrill ( https://mandrillapp.com ). Once they are out,
Mandrill sends various events back (open, clicked, etc). We want to listen to those
events and capture them for later usage. We also want to notify some user interface
in real time about those events from Mandrill.

## What is expected

- Mandrill sends event [open] to backend app webhook
- Backend stores message payload into storage of some kind (cache/sql/nosql
or any other, no schema definition required). Mandrill’s message ID can be
used as a key
- Backend publishes notification that user opened email via websocket to very
simple index.html frontend with websocket client
( https://developer.mozilla.org/en-US/docs/Web/API/WebSocket )

## Approach

To achieve required flow we can make application with fairly simple architecture - `Django` for handling webhooks with HTTP and `Channels` for handling websockets connections and direct delivery of `open` event notifications.
But to aquire quality we need to address some problems:

- Mandrill webhooks may scale in future (both with webhook queue and number of tracked emails).
- Some business intelligence may be needed in future - we may want to save all types of events to permanent storage and analyze later.
- Application usage may scale by number of handled events, different from `open` event and by new event handling procedures.

Meaning, we may want to include more complex flow of webhook handling, leaving space for different types of events, acceptable time of DB communication and fast webhook handling (without standard sync handling).

My proposal is to provide fast handling of webhook with Celery/Redis dispatching task (send `HTTP STATUS 200` right away). With dispatch we can handle events:

- with custom handler procedures (e.g. websockets notifications for `open` events)
- with custom DB models linked to to handlers

## Application architecture

This application webhook entrypoint is `hooks/` view, that recieves webhook, dispatches it with Celery task and gives Mandrill response that webhook recieved.
Celery dispathing task creates `PayloadDispatcher` object, that checks webhook authenticity and dispatches appropriate handler for recieved events with Celery handling tasks. If no custom handling provided - triggers default handling procedure (basically, save payload to permanent storage)
Each task serializes payload in custom handler class instance, then calls its `handle()` method.

For `open` event `OpenEventHandler` class is provided. `OpenEventHandler` is linked with Django model `OpenEvent` for permanent storage. `OpenEventHandler` provided additional steps to handle() procedure with more serialization (email message) and connection to Channels/Redis layer for notifications. Each new `open` event goes through Channels/Redis layer and is being sent to websocket client.

## Current state of application and thoughts on quality

Application is in development quality for the challenge. You can check docker-compose.yml for testing deployment.
Mandrill webhooks can be tested with test webhooks (https://mandrillapp.com/settings/webhooks/ send_test) and ngrok for exposed web connection.

Next steps that should be taken or should be considered for production:

- Ensuring safe connections (`wss://` vs `ws://` , SSL encryption, proxy)
- Production settings (.env with secrets) and database
- Automated tests covering websockets connection and different Mandrill webhooks handling
- Webhooks coverage (new events, actions)
- Deeper payload serialization (depending on planned business processes)
- Additional event handling (depending on planned business processes)