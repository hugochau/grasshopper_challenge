: '
File = init_db.sh
Version = 1.0
Author = Hugo Chauvary
Email = chauvary.hugo@gmail.com 
'

# create user & db
/etc/init.d/postgresql start &&\
    psql --command "CREATE USER grasshopper WITH SUPERUSER PASSWORD 'docker';" &&\
    psql --command "ALTER USER postgres WITH PASSWORD 'postgres';" &&\
    createdb -O grasshopper grasshopper