FROM postgres:15

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=restaurantes

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
