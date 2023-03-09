FROM python:3.11.2-slim-buster
WORKDIR /backend-flask

COPY requirements.txt requirements.txt
RUN apt update && apt install -y curl
RUN pip3 install -r requirements.txt

# Copy from outside the container to inside the container
COPY . .

ENV FLASK_ENV=development

EXPOSE ${PORT}
# python3 -m flask run --host=0.0.0.0 --port=4567
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]
