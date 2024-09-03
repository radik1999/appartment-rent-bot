FROM python:3.12-slim-bullseye
WORKDIR /home
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev build-essential


COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY src/. src/
WORKDIR /home

COPY ./entrypoint.sh ./
RUN chmod 777 ./entrypoint.sh


# Specify the entrypoint script
ENTRYPOINT ["./entrypoint.sh"]
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 5432
