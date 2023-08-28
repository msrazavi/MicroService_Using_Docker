FROM postgres:latest

ENV POSTGRES_USER myuser
ENV POSTGRES_PASSWORD digipass
ENV POSTGRES_DB digi_database

COPY init.sql /docker-entrypoint-initdb.d/