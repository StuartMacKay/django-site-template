# How this project is organised

From Django's point of view this project is organised into the following
directories:

```
django-site-template (you are here)
└───locale
└───project
│   └───apps
│   └───conf
│   │   └───celery
│   │   │   app.py
│   │   │   logging.py
│   │   │   schedule.py
│   │   │   settings.py
│   │   asgi.py
│   │   settings.py    
│   │   urls.py
│   │   wsgi.py 
│   └───locale
│   └───static
│   └───templates
│   └───tests
└───static
└───templates
│   manage.py
```

The first thing to note is that, with python, it's modules all the way down.
That means, for the three entry points used to run Django, `manag.pye`, `asgi.py`
and `wsgi.py` it really does not matter where anything is located. As long as 
it can be found on `sys.path`, you can import it.

The first place this template is different from most is the `project` module.
Normally when you setup a Django project the convention is to call it something
"unique":

```shell
django-admin startproject mysite
```

Here, we simply give it the bland name `project` for the simple reason that the 
only place it will ever be referenced is from within the code you are going to 
write. Reusable Django apps need unique names to avoid conflicts or confusion 
is two with the same name end up in the same project. That simply does not apply
to root module of a site - unless some genius names the root module in their 
reusable app,`project`, in which case you are going to need to rename this one. 
There is also the added advantage that when referenced in `import` statements 
it is abundantly clear what code is being used. For example:

```python
from project.views import ...
```

## Configuration

The second departure from convention is that the settings, urls and configuration
files for ASGI and WSGI are placed in a `conf` module. There are two reasons 
for doing this. The first is rather trivial. Stashing away these four files 
unclutters the `project` module and puts everything related to configuring 
the project in one place. The second reason is more practical. We can do the
same to the configuration for celery. 

We can't just put everything in `celery.py` because it needs to contain the 
following code:
```python
from celery import Celery

app = Celery()
```
and python will complain that you are trying to import the file before you 
have finished defining it. Most projects get around this by calling the file, 
`celery_app.py`. Instead, we can break the configuration into separate files,
making things a little easier to find. Celery can still import the `app` object
from `conf/celery/__init__.py` and we keep everything neat and tidy. 

## Apps

Creating a separate directory for apps, /project/apps/, is nice as it keeps 
the project apps out of the root directory. That has two effects. It makes it 
clear that apps are just modules and can exist anywhere. More importantly, 
the way django generates the names for the database tables makes it easy to 
factor out apps as separate projects without having to go through the pain 
of migrating the underlying database tables just to change the app prefix.

It does make imports a little bit more verbose:
```python
from project.apps import contacts
```

but, again, you know exactly where something came from. If you ever end up 
with a large project then keeping the cognitive load as low as possible is 
always a good thing.

## Resources

The project directory is where we put the static assets, templates and 
translations files specific to the project:

```shell
django-site-template
└───project
│   └───locale
│   └───static
│   └───templates
│
└───locale
└───static
└───templates
```
The directories of the same names in the project root, /django-site-template,
allow you override files or translations either in the project or in any
third-party apps you use. The `STATICFILES_DIRS`, `TEMPLATES["DIRS"]` and
`LOCALE_PATHS` settings are configured to search these first.

If you run:
```shell
python manage.py makemessages --all
```
from the root directory, Django will put the messages in `/locale/` so you need
to change directory to `/project` first. The `Makefile` has a `messages` target
that does the directory change first:
```shell
make messages
```

## Tests

Using pytest, the convention is to keep the tests separate from the source 
tree. This is mainly done, so you do not end up shipping the tests if you are
developing a reusable app. Here we put the test inside the project directory
for the simple reason that, when looking for something code related, you need
only search one directory tree. Mundane, but when refactoring, the number of 
times code in a separate tests directory gets missed can be counted like grains 
of sand on a beach.

The other nice thing about mixing the tests with the code is that you are 
sort of forced to put them in the apps to keep things manageable. For large
codebases having everything close at hand has a quality all of its own.

## Docs

The docs are divided into two sections, how-tos and tech-notes. How-tos are,
as the name infers, recipes for carrying out various project tasks. Tech-notes
are exactly that, technical notes describing why things they way they are,
why design decisions were taken, etc. Anything that is too long to put in a 
comment in the code.

Always write any docs in Markdown. Restructured Text is much more expressive
but it's much harder to remember, and get right. You write everything in plain
text but all the major repository hosting sites render nice Markdown you can
get browsable, easy to follow documentation for a little extra effort.

Put any other types of documentation here. Stay way from the idea of writing 
a user manual or wiki for your project. You will never keep it up to date.

## Requirements

The `/requirements` are broken down into separate files, according to the 
type of environment in which the code will be run. That way you never need
to download and install packages you are not going to use. 
[pip-tools](https://github.com/jazzband/pip-tools) and 
[pip-upgrade](https://pypi.org/project/pip-upgrader/) make it easy to manage
the files.

## ToDo

Django and Celery have different entry points when starting. Currently, there
are separate blocks for configuring the logging for each. It would be nice if
most of the code was shared (the configuration dictionary already is) - it is
tiresome having to make changes in two places.
