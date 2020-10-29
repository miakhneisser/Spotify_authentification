FROM python:3.7
COPY requirements.txt /
RUN pip install -r requirements.txt
WORKDIR /Spotify_FlaskApp
COPY . /Spotify_FlaskApp
CMD ["python", "app.py"]
