# start with a fresh ubuntu image
FROM ubuntu:18.04

# select non interactive mode
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# some installs
RUN apt-get update && apt-get -y install \
    vim \
    bash-completion \
    wget \
    lsb-release \
    sudo \
    gnupg2 \
    dialog \
    apt-utils

# add postgres
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" | tee  /etc/apt/sources.list.d/pgdg.list

# install postgres
RUN apt-get update && apt-get -y install \
    postgresql \
    postgresql-client

# 

# run db conf as postgres
USER root
# init db
COPY init_db.sh .
RUN chmod 777 init_db.sh

USER postgres
RUN /init_db.sh
# update pg_hba.conf
RUN echo "host all  all    0.0.0.0/0  trust" >> /etc/postgresql/13/main/pg_hba.conf
# update postgresql.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/13/main/postgresql.conf

# set the default command
CMD ["/usr/lib/postgresql/13/bin/postgres", "-D", "/var/lib/postgresql/13/main", "-c", "config_file=/etc/postgresql/13/main/postgresql.conf"]