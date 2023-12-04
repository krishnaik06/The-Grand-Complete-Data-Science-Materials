# FROM  - the base image to use to start the build process.
FROM python:3.8-slim-buster

# WORKDIR - sets the working directory for any RUN, CMD, ENTRYPOINT, COPY and ADD instructions that follow it in the Dockerfile.
WORKDIR /app

#COPY - copies files or directories and adds them to the filesystem of the container.
COPY . ./

# RUN - executes any commands in a new layer on top of the current image and commits the results.
RUN pip install -r requirements.txt

# CMD - provides defaults for an executing container.
CMD python app.py