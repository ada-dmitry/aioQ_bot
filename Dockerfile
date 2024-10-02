FROM python
WORKDIR /app
COPY . /app/

RUN pip3 install -r requiments.txt

EXPOSE 5000

CMD [ "python3", "run.py" ]

