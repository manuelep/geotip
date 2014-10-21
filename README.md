web2py-new-app
==============

Installation steps
============================

## 1. Clone the repository

```sh
$ git clone <url> <app>
```

## 2. Init the required submodules (**if needed**)

### 2.1. Pull and checkout into the branch containing all submodules

```sh
$ cd <app>/
$ git fetch origin submodules
$ git checkout submodules
```

### 2.2. Init and update submodules

```sh
$ git submodule init
$ git submodule update
```

### 2.3. Go back to the branch master

```sh
$ git checkout master
```

## 3. Database configuration

### 3.1. Create the database

Help yourself with the [PostgreSQL doc][] or some easier [how to][].
For SQLite DB usage this step is not necessary because the DB file
is automatically created.

### 3.2. Rename and modify the configuration file

```sh
$ cp models/confdb.py.example models/confdb.py
$ vim models/confdb.py
```

* Set the DEVELOPMENT variable value to **False** if in production;
* Adapt the dsn in dbconf->db->args list to your system configuration according
to the [web2py dsn specificaton][]
* Set migrate_anabled and migrate values to **False** if at the moment of the
installation the dedicated database is **not** empty and the tables
described in the model are already defined in the DB engine.

## How to run tests

```sh
$ ./web2py.py -S web2py_new_app -M -R applications/web2py_new_app/tests/*.py
```

[web2py dsn specificaton]: http://www.web2py.com/books/default/chapter/29/06/the-database-abstraction-layer#Connection-strings
[PostgreSQL doc]: http://www.postgresql.org/docs/9.3/static/
[how to]: http://www.cyberciti.biz/faq/howto-add-postgresql-user-account/
