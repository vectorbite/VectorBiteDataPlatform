# Configuring PostgreSQL & PostGis for VectorBiTE Data Platform Databases

## Setting up on Ubuntu and other Debian-based Linux distributions. 

`Installation` 

```

https://www.postgresql.org/download/linux/ubuntu/

wget deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main

sudo apt-get install postgresql postgresql-contrib libpq-dev pgadmin4
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
matt@matt-HP-ZBook-15-G3:~$ wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add -


sudo apt-get -y install postgresql
sudo apt-get -y install python-psycopg2
```

`Start the database server with:`

```
sudo /etc/init.d/postgresql restart
```

`The PostgreSQL configuration file is:`

```
 /etc/postgresql/x.x/main/postgresql.conf  (x.x is the version number)
```

`The PostgreSQL logs are in:` 

```
/var/log/postgresql/
```

`Create the users and a database so that web2py applications can use it:`

```
sudo -u postgres createuser -P -s admin_db
sudo -u postgres createuser -P -s vecdyn_db
sudo -u postgres createuser -P -s taxon_db
sudo -u postgres createuser -P -s geo_db
createdb vectorbite
```

enter password for each user

`To confirm the database has been created type`

```
psql vectorbite
```

if you make a mistake , to drop a user

sudo su - postgres -c "dropuser admin"

to drop a database

sudo -u postgres dropdb vectorbite

```
CREATE DATABASE vectorbite
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;
```



```
CREATE USER admin WITH
	LOGIN
	SUPERUSER
	CREATEDB
	CREATEROLE
	INHERIT
	REPLICATION
	CONNECTION LIMIT -1
	PASSWORD 'xxxxxx';
GRANT pg_signal_backend, postgres TO admin WITH ADMIN OPTION;
```

The web2py application can now connect to this database with the command:

```
db = DAL( "postgres://"username here":"mypasswordhere"@localhost:5432/vectorbite")
```

`Where mypassword is the password you entered when prompted, and 5432 is the port where the database server is running.`

`For database backup details, read the PostgreSQL documentation; specifically the commands pg.dump and pg.restore.`