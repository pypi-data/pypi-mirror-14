pushnote
========

`pushnote`_ is a simple django plugin for sending push messages from
django server to sockjs clients. It internally uses `zeromq`_ and
`sockjs-tornado`_. pushnote can send push notifications to all sockjs
clients and to subset of this clients.

Requirements:
-------------

1. `pyzmq`_>=2.0
2. `sockjs-tornado`_>=0.0.5
3. `django`_>=1.4

GitHub:
-------------
https://github.com/dadasoz/pushnote

Installation:
-------------

Install ``pushnote`` with your favorite Python package manager:

::

   pip install pushnote

Add ``pushnote`` to your ``INSTALLED_APPS`` in ``settings.py``

::

   INSTALLED_APPS = (
       'django.contrib.auth',
       'pushnote',
       ...
   )

Define ``PUSHNOTE_MQ_SOCKET`` in ``settings.py``

::

   PUSHNOTE_MQ_SOCKET = 'tcp://127.0.0.1:8002'

Usage:
------

Run pushnote forwarder device

::

   pushnote-mq --sub=tcp://127.0.0.1:8002 --pub=tcp://127.0.0.1:8001

Run sockjs-tornado server

::

   pushnote-server --port=8080 --mq_socket=tcp://127.0.0.1:8001 --route=/sockjs --address=''


Alternatively, if you don't need multiple tornado instances support, you can entirely omit pushnote-mq and should pass -S/--single argument to pushnote-server

::

   pushnote-server --single --port=8080 --mq_socket=tcp://127.0.0.1:8002 --route=/sockjs --address=''

Append sockjs client library to your page

::

   <head>
       <script src="http://cdn.sockjs.org/sockjs-0.3.min.js">
       ...

Open page in browser and connect to sockjs-tornado server

::

   conn = new SockJS('http://localhost:8080/sockjs')

Define a callback for incoming messages

::

   conn.onmessage = function (e){ console.log(e.data); };

Send a message from django

::

   from pushnote.pub import notify_all
   notify_all({'msg': u'Hi all!'})

and you will see it in js console

::

       Object {msg: "Hi all!"}

Advanced notifications:
-----------------------

You can send notifications to subset of users.

::

    from pushnote.pub import notify
    from pushnote.utils import tokenize
    from django.contrib.auth.models import User
    user = User.objects.get(email='pushnote@mail.com')
    notify({'msg': u'Hi, %s!' % user.username}, users=[user])
    token = tokenize(user)
    notify({'msg': u'Hi user with token %s !' % token}, users=[user])

To get this messages you need to subscribe by token

::

    var token = {% pushnote_token %};
    SockJS.prototype.emit = function (name, data) { // wrapper around SockJS.send for pushnote's protocol support
        var meta_dict = {
            name:name,
            data:data
        };
        this.send(JSON.stringify(meta_dict))
    };
    conn = new SockJS('http://localhost:8080/sockjs')
    conn.emit('subscribe', {'token': token});
    conn.onmessage = function (e){ console.log(e.data); };

``{% pushnote_token %}`` is nothing more than a wrapper around
``pushnote.utils.tokenize`` that returns user.id signed with
standart django singing mechanism. You can configure you own salt by setting
``PUSHNOTE_SALT`` in ``settings.py``. If you need more security,
you can provide your own tokenization function. It should accept django User
 object and return token. Add path to this function in settings.py .

::

    PUSHNOTE_TOKENIZER = 'pushnote.utils.tokenize'

Conclusions:
------------

1. pushnote serializes datetime objects with ISO 8601 format. You can parse it on client with `moment.js`_ .
2. pushnote server can handle client's messages constructed only in some specific way and can't be used for client to client communications.

