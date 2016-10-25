# django-less

In this project used pure LESS stylesheets with server-side compiling.

Django static precompiler provides template tags to compile LESS,SASS style-sheets.

Installation

1. $ pip install django-static-precompiler

2. Add 'static-precompiler' to INSTALLED_APPS in settings.py

3. Run manage.py migrate command to initialize database

4. Set STATIC_ROOT path in your app

5. In templates load compile_static template tag and less files

	{% load compile_static %}

	link rel="stylesheet" href="{% static "path/to/style.less"|compile %}"

	Which will be parsed to

	link rel="stylesheet" href="/static/COMPILED/path/to/style.css"

To use this project on my win cmd I have done following steps

	pip install Django==1.10.2
	pip install django-static-precompiler

	install node.js
	npm install -g less (if -g is not set then we should pass path to lessc explicitly)

	pull sources from repo
	cd django-less

	python manage.py migrate
	python manage.py runserver