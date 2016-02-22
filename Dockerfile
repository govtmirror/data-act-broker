FROM ubuntu

RUN apt-get update && apt-get install -y \
    git \
    curl \
    python-pip \
    ca-certificates \
    python-dev \
    libpq-dev \
    postgresql

#needed for testing, perhaps belongs in pip dep??
RUN pip install unittest-xml-reporting

ADD . /data-act

WORKDIR /data-act

RUN pip install --process-dependency-links .

ADD s3bucket.json /usr/local/lib/python2.7/dist-packages/dataactcore/aws/s3bucket.json
ADD dbCred.json /usr/local/lib/python2.7/dist-packages/dataactcore/credentials/dbCred.json
ADD web_api_configuration.json /usr/local/lib/python2.7/dist-packages/dataactbroker/web_api_configuration.json
ADD credentials.json /usr/local/lib/python2.7/dist-packages/dataactbroker/credentials.json
ADD manager.json /usr/local/lib/python2.7/dist-packages/dataactbroker/manager.json

CMD webbroker -s
    
