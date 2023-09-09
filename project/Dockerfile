FROM python:3.8
LABEL maintainer="Itumeleng Tshabalala"

COPY . /project
WORKDIR /project
RUN pip install -r techtrends/requirements.txt
RUN python techtrends/init_db.py

# command to run on container start
CMD [ "python", "techtrends/app.py" ]