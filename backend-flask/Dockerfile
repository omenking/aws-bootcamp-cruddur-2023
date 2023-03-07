FROM  python:3.12.0a5-slim

WORKDIR /backend-flask

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy from outside the container to inside the container
COPY . .

ENV FLASK_ENV=development

EXPOSE ${PORT}
# python3 -m flask run --host=0.0.0.0 --port=4567
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]
