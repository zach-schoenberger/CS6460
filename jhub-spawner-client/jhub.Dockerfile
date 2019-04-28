FROM jupyter/pyspark-notebook:latest
LABEL email=zschoenb@gmail.com

USER root
RUN apt-get update -y
RUN apt-get install -y git vim curl

RUN echo 'export HOSTIP=$(hostname -i)' >> /etc/bash.bashrc


COPY ./*.py /opt/client/
COPY ./examples /home/jovyan/examples
COPY ./examples /opt/client/
ENV PYTHONPATH=$PYTHONPATH:/opt/client