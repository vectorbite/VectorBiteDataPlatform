# Database deployment procedure
This document describes the release procedure for the VBDP postgres database

## 0. Kill the previous database if required
Firstly you may wish to kill the previous database. To do this you will probably need to stop the apache server using `sudo service apache2 stop` on the server (ssh in as usual).

Next run `sudo su postgres` to switch to the postgres ubuntu user and run `psql` to connect to the main server as the superuser.

Now run `DROP DATABASE vectorbitedb;` to kill the db, and run the following to drop all users.

``` sql
DROP ROLE IF EXISTS geo;
DROP ROLE IF EXISTS tax;
DROP ROLE IF EXISTS vbdp;
DROP ROLE IF EXISTS vectraits;
DROP ROLE IF EXISTS vecdyn;
DROP ROLE IF EXISTS vbadmin;
```

This should leave you in a position to run the setup scripts as usual.

---

## 1. Create the DB, superuser, schemas & users
A lot of this has now been scripted, so simply put you just need to connect to the main aws server as postgres and run the `create_vbdp_db_pt1.sh` script (location tbc).

This will set up the db structure ready for data import

## 2. Data import
Importing data for the first time will seem to generate a few errors, as the pgdump file contains sql to try to drop the tables of the schema if they exist. As they do not exist, it'll throw some errors though this should be nothing to worry about.

To import the data, use the following command **from the main ubuntu user**:

`/usr/bin/pg_restore --dbname=vectorbitedb --schema=<SCHEMA> --clean --username=<USER> --host=127.0.0.1 --port=5432 /path/to/dump.pgdump`

So if I was importing `vectraits_270219.pgdump` from the pgdumps folder on LIVE into the `vectraits` schema, I would use the following command:

`/usr/bin/pg_restore --dbname=vectorbitedb --schema=vectraits --clean --username=vectraits --host=127.0.0.1 --port=5432 /home/ubuntu/pgdumps/vectraits_270219.pgdump`

This pgdump file should also create any constraints and views applied to the original db it was taken from. Thus once this is complete we just need to get VBDP to pick up the data.

## 3. Fake migration
In order to get Web2Py to work out that the data has change, we need to force a fake migration. Firstly restart apache2 if necessary using `sudo service apache2 start`.

Next navigate to the `/home/www-data/web2py/applications/VectorBiteDataPlatform/models` directory and open the `db.py` file. Find the line that defines the connection to the relevant schema e.g.

``` python
db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             lazy_tables=True,
             # fake_migrate_all=True,        # Allow fake migration to rebuild table metadata
             check_reserved=['sqlite'])
```

Uncomment the `fake_migrate_all` line and then try to open a view which depends on the db you just restored.

If that all works correctly, uncomment the `fake_migrate_all` line and you should be done.

In future this last step will be spun out to the appconfig.ini file, so no changes to the code will be required. 

