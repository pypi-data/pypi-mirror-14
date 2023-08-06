Messenger Hook
==============

Description
-----------

This is a basic implementation of a facebook messenger Hook.
It's working with falcon but should be easily modify to work with Flask or Django.

Install
-------

You can run `pip install messenger_hook` to install it.

Build a ping application
------------------------

```python
import falcon
from messenger_hook.falcon_messenger import FalconMessenger

app = falcon.API()
hook = FalconMessenger('verify_key', 'your_token')
app.add_route('/hook/', hook)
```

You need to install falcon to use it with falcon.
You can launch it with gunicorn or uwsgi


Transform message
-----------------

```python
import falcon
from messenger_hook.falcon_messenger import FalconMessenger

class MyMessenger(FalconMessenger):
    def transform_message(self, message):
        return 'You sent {}'.format(message)

app = falcon.API()
hook = FalconMessenger('verify_key', 'your_token')
app.add_route('/hook/', hook)
```
