# flask-orgainized

What Is This?
-------------

This is a simple Python/Flask application intended to help users better organize there time. It has been integrated with fullcalendar.js (minimal).  

## Features
* User registration 
* User profiles
* Database setup, including database migrations and CRUD examples
* Fast deployment on Heroku (including staging and production setup)
* Powerful stack: back-end based on Python with Flask, front-end is Bootstrap, fullchalendar
* Including basic testing coverage and framework and PEP8 check (flake8)


Development
-----------

If you want to work on this application I’d love your pull requests and tickets on GitHub!

1. If you open up a ticket, please make sure it describes the problem or feature request fully.
2. If you send a pull request, make sure you add a test for what you added.

## Development Environment

At the bare minimum you'll need the following for your development environment:

1. [Python](http://www.python.org/)

It is strongly recommended to also install and use the following tools:

1. [virtualenv](https://python-guide.readthedocs.org/en/latest/dev/virtualenvs/#virtualenv)
2. [virtualenvwrapper](https://python-guide.readthedocs.org/en/latest/dev/virtualenvs/#virtualenvwrapper)

### Local Setup

The following assumes you have all of the recommended tools listed above installed.

#### 1. Clone the project:

    $ git clone git@github.com/ThomasMcDonnell/flask-organized
    $ cd overholt

#### 2. Create and initialize virtualenv for the project:

    $ mkvirtualenv venv
    $ source bin/activate (mac and linux only)
    $ pip install -r requirements.txt

#### 3. Run the development server:

    $ export FLASK_APP=todo.py
    $ export FLASK_ENV=development
    $ flask run

#### 4. Open [http://localhost:5000](http://localhost:5000)


### Development

If all went well in the setup above you will be ready to start hacking away on
the application. The application has minimal integration with fullcalender.js feel free 
to hack around and try intergrating CRUD capabilities through ajax calls. 

#### Database Migrations

This application uses [flask-migrate](http://flask-migrate.readthedocs.org/) for database
migrations and schema management. Changes or additions to the application data
models will require the database be updated with the new tables and fields.


