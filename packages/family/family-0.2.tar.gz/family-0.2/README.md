# We are family, we are microservices

## Get Started

    mkvirtualenv family

    pip install git+git://github.com/daixm/family.git@master

    family-createapp helloworld

    # then step by step create your project

    cd helloworld; tree .
      ├── development.ini
      ├── helloworld
      │   ├── app.py
      │   ├── __init__.py
      │   ├── settings.py
      │   └── wsgi.py
      ├── helloworld.egg-info
      │   ├── dependency_links.txt
      │   ├── entry_points.txt
      │   ├── PKG-INFO
      │   ├── SOURCES.txt
      │   └── top_level.txt
      ├── __init__.py
      ├── production.ini
      ├── requirements.txt
      └── setup.py

    pip install -r requirements.txt; gunicorn --paste development.ini
