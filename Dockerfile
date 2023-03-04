FROM python:3.11.1-slim-bullseye as base
LABEL Home Notes App
# set work directory
WORKDIR /code

# set environment variables
# Python path IMPORTANT
ENV PYTHONPATH "${PYTHONPATH}:/code/app"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update -y && \
    apt-get install procps curl net-tools iproute2 postgresql-client gcc libpq-dev -y


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --upgrade
# Create non-root user to run as
# on your host machine, make sure that you have the right permissions and a user added to the GID 1001
ARG UNAME=docker-runner
ARG UID=1001
ARG GID=1001
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME

# copy project
COPY . .
RUN chown -R docker-runner:docker-runner /code/app
USER $UNAME

#Expose port
EXPOSE 8000
EXPOSE 5678

# If debug is enable start debug steps.
FROM base as debug
RUN pip install debugpy
CMD  python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m flask run --host 0.0.0.0 --port 8000

FROM base as prod
# run entrypoint.sh
CMD  gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app