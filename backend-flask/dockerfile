FROM python:3.10-slim-buster

# Inside Container
# Make new folder inside container
WORKDIR /backend-flask

# Outside container -> Inside container
# This contains libraries to install
COPY requirements.txt requirements.txt

# Inside container
# Install python libraries used for the app
RUN pip3 install -r requirements.txt

# Outside container -> Inside container
# . means everything in the current directory
# First period - (?backend-flask) (outside container)
# second period - (/backend-flask) (Inside container)
COPY . .

# Set environment variables
# Inside container and remain when container is running
ENV FLASK_ENV=development

EXPOSE ${PORT}
# This command runs flask
# python3 -m flask run --host=0.0.0.0 --port=4567
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]