FROM python:3.5
COPY src /src
COPY requirements.txt /src/requirements.txt
CMD ["pip", "install", "-r", "/src/requirements.txt"]
CMD ["python", "/src/runserver.py"]
