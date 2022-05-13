#Ref: https://medium.com/backticks-tildes/how-to-dockerize-a-django-application-a42df0cb0a99
# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.10.3

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /images_api

# Set the working directory to /images_api
WORKDIR /images_api

# Copy the current directory contents into the container at /images_api
ADD . /images_api/

# Install all needed packages specified in requirements.txt
RUN pip install -r requirements.txt