
# start with a fresh ubuntu image
FROM ubuntu:18.04

# select non interactive mode
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# some installs
RUN apt-get update && apt-get -y install \
    vim \
    bash-completion \
    wget \
    openssh-server \
    lsb-release \
    git \
    curl \
    sudo \
    gnupg2 \
    dialog \
    apt-utils \
    default-jdk

# Add latest postgres
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" | tee  /etc/apt/sources.list.d/pgdg.list

# postgresql-client only needed
RUN apt-get update && apt-get -y install \
    postgresql-client \
    python3.7 \
    python3.7-dev \
    python3-distutils \
    python3-apt


# update pip
RUN curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3.7 get-pip.py --force-reinstall && \
    rm get-pip.py

# create user
RUN \
useradd -ms /bin/bash -p grasshopper grasshopper \
&& \
usermod -a -G sudo grasshopper

USER grasshopper
# create workdir
WORKDIR /home/grasshopper
# install required packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# add postgresql JDBC
USER root
ADD https://jdbc.postgresql.org/download/postgresql-42.2.23.jar ./postgresql-42.2.23.jar
RUN chown grasshopper ./postgresql-42.2.23.jar

# SET the default command
ADD start.sh .
RUN chmod 777 start.sh
USER grasshopper
CMD ["sh", "start.sh"]