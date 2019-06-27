# Stellar SMS client
==================

This is a python implementation of sending digital assets via SMS on the stellar network. A simple http server API listens for incoming transactions and verifies (more on this below) it before submitting it to the network. If the transaction has already been submitted, horizon will simply return the saved result and not attempt to submit the transaction again, as stated in the [docs](https://www.stellar.org/developers/horizon/reference/endpoints/transactions-create.html). Further protection against multiple submissions is provided by a Redis lock on the transaction key to ensure only one worker process is working on the task.  
**This is an experimental project. Not intended for use in production.**

## Features and functionality

* Inspired by the [js version ](https://github.com/stellar/stellar-sms-client) of stellar-sms-client
* Flask, Postgres, Celery for task management, Redis as a message broker and for task locking. Each running as a service using docker-compose
* Configured for test net. 
* After creating an account on the test net  and [deploying the app](#testing-and-deployment) you can send a transaction by sending a text to your Twilio phone number: `send [address] [amount]` (or `send [name] [amount]` if there exists an Address mapping for `[name]` in the database.) For example: `send tunde 10` will send 10 XLM to tunde.
* The app will then send a reply text with a summary of the transaction and prompts a response from the user with 'Y' or 'Yes', or a one-time password (not fully implemented) if the user has one set up.  
* The simplest way to demo this app is by running a mock transaction as described in the section below 

## Testing and deployment

To test the app:
* Build the docker image and start services:
```
$ python manage.py up
```
* Start a shell in the container by running :
```
$ python manage.py shell
```
* To run all tests: run ``$ pytest`` from inside the container shell 

* To see a mock transaction: import and run the `tests.client.live_test.live` method in a flask shell within a container shell and verify the transaction using the logs from the docker-compose terminal. (This is actually a real transaction on the test net, a 'mock' only because it's not initiated by an actual SMS)

To deploy:
* Build the docker image and start services:
```
$ python manage.py up
```
* install and run [ngrok](https://ngrok.com/) in a separate terminal to expose your local server using the public url

After deploying your app:

1. Create your accounts on the test net and populate the DB accordingly
2. Create a phone number that is capable of sending/receiving SMS on  [Twilio](https://www.twilio.com/):
3. In your phone number details set Request URL to:
```
https://[your ngrok public URL]/api/messages/sms
```
Request method can be set to `HTTP GET or POST`.

## DISCLAIMER
* This app was in no way intended to be a secure method of sending or receiving digital assets. It was built for demo purposes only. 
There are no warranties or guarantees expressed or implied.
You assume all responsibility and liability. 

## License 
* Code released under the [MIT License](https://opensource.org/licenses/MIT).
