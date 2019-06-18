FROM ubuntu:18.04
ARG auth_token
ARG mac_address

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       apt-utils \
       python-setuptools \
       python-pip \
       software-properties-common \
       rsyslog systemd systemd-cron sudo curl

RUN pip install requests

ADD mac_utils.py /
CMD ["python", "./mac_utils.py", "-t", "$auth_token", "-m", "$mac_address"]
