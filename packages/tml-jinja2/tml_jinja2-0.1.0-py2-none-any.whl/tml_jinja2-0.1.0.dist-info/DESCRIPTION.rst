[![Build Status](https://travis-ci.org/translationexchange/tml-jinja2.png?branch=master)](https://travis-ci.org/translationexchange/tml-jinja2)
[![Coverage Status](https://coveralls.io/repos/translationexchange/tml-jinja2/badge.png?branch=master)](https://coveralls.io/r/translationexchange/tml-jinja2?branch=master)


The idea of this extension is to integrate web frameworks, that uses Jinja2 as template engine, with TML in easy and extendable fashion.


The best way to start using this extension is to run a "toy" demo on Bottle that comes bundled with this extension.


### Before Running the Sample Application
Make sure you have a Translation Exchange account, and have created a project in your dashboard.

https://github.com/translationexchange/tml-jinja2

```bash
$ git clone https://github.com/translationexchange/tml-jinja2.git
$ cd tml-jinja2/demo
$ virtualenv --no-site-packages tml_env
$ . ./tml_env/bin/activate
$ pip install -r requires.txt
```

Now you can start the application by running:

```bash
$ python app.py
```

This will start the Toy demo port 8000. Open your browser and point to: [http://localhost:8000](http://localhost:8000)

