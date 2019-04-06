FROM jupyter/pyspark-notebook:latest
LABEL email=zschoenb@gmail.com

USER root
RUN apt-get install -y git

