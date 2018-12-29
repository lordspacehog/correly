FROM python:3.7.2-stretch
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install correly
CMD ["/usr/bin/env","correly"]
