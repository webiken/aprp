FROM python:3.5
COPY src /src
CMD ["python", "/src/test.py"]
