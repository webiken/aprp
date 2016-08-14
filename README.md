# aprp - Asynchronous Python Range Proxy.  

A python based HTTP 1.1 Reverse Proxy supporting Range requests.

APRP is a `Tornado <http://www.tornadoweb.org>` based reverse
proxy for media requests supporting range style requests
as per the HTTP 1.1 RFC.

## Request Types

There are two types of range requests supported:
	1 Range in request headers (HTTP 1.1)
    2 Range as URL param, as in : 
      1 /myfilename/<start>/<end>
      2 /myfilename.mp4/1234/789

## Unit Testing

1. Tornado offers a testing library based on python's UnitTest.
2. `Nose <http://nose.readthedocs.io/en/latest/>` is used as a TestRunner.
3. Requests to upstream server are mocked using `unittest.mock <https://docs.python.org/3/library/unittest.mock.html>`

After installing libraries in requirements.txt, unit testing can run as:
```$ nosetests```
The config file ```nose.cfg``` has a basic configuration but can be updated
to create coverage reports, etc.

## Docker 
```Dockerfile``` in repo downloads the ```python 3.5``` image, installs
requirements, and runs the ```runserver.py``` script as entry point.

## runserver.py

```runserver.py``` servers as an entry point and helps set paths correctly since it is
run outside of the main package.  It uses two functions defined in ```aprp.py``` module.

## Logging

Logging uses the ```RotatingFileHandler``` and is configurable in the
```settings``` module.

## Settings
Settings are configurable via the ```settings.py``` module.  Basic settings include:
1. DEBUG    : development vs production.
2. PORT     : 80 in production else 8000
3. UPSTREAM : Upstream server URL



