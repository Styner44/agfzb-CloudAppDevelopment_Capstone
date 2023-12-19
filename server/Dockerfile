FROM python:3.8.2
ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1
RUN apt-get update \
    && apt-get install -y netcat
ENV APP=/app
WORKDIR $APP
COPY requirements.txt $APP
RUN pip3 install -r requirements.txt
COPY . $APP
EXPOSE 8000
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/bin/bash","/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangobackend.wsgi"]