FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY requirements /app/requirements
RUN pip install --upgrade pip
RUN pip install -r /app/requirements/requirements.txt
EXPOSE 8000
COPY . /app/
CMD ["python","manage.py","runserver","0.0.0.0:8000"]
ENTRYPOINT ["sh", "docker-entrypoint.sh"]

