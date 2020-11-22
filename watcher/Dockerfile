
FROM python:3.8-slim

COPY . /app
WORKDIR /app
# set timezon from watcher-variables.env
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN pip3 install --no-cache-dir  -r requirements.txt
RUN pytest -s

CMD ["python3", "watcher.py"]