# Molly

`molly` is simple application that injects a signal after the WSGIHandler
is instatiated. What this means for you is that you can definitively know when
your application is live and can receive requests.


## Installation:

`pip install django-molly`


## Usage:


```python
# settings.py file

INSTALLED_APPS = (
    ...,
    'molly',
    ...
)

```

```python
# in some apps.py file
...
from molly.signals import application_started


def hello_world():
    print "hello world!!!"

class MyAppConfig(AppConfig):
    def ready(self):
        application_started.connect(
            hello_world, dispatch_uid='my-silly-message'
        )
```

So now when you run `python manage.py runserver` or *any* service that utilizes
the `django.core.handlers.wsgi.WSGIHandler` you should see you message.

Enjoy the *ecstacy* of it all...
