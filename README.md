web2py-new-app
==============

This a simple (e.g. empty) web2py application as it comes from the wizard
of the admin web application augmented with some useful features such as:

* A predefined logger
* A UnitTest example
* A uniformed and coded way for submodules installation
* A uniformed and coded way for distinguish DB configuration between different installations

Prerequisites
============================

## Dependencies:

They depend on the specific developed application. They could be something like:

* python-psycopg2 (>=2.5.2)
* ...

## Other prerequisites:

They depend on the specific developed application. They could be something like:

* Running and accessible PostgreSQL server (>=9.3)
  with a dedicated database
* ...

Deploiment
============================

[TODO]

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

## 4. Create a local branch for configuration versioning (*optional*)

### 4.1. Create your local branch

```sh
$ git checkout -b local
```

### 4.2. Let your branch recognize your configuration file

For this purpose you have to comment out the line in your .gitignore
that exclude your configuration file from versioning.
Change the line

```
models/confdb.py
```

to 

```
# models/confdb.py
```

### 4.3. Add the configuration file to your branch

```sh
$ git add .gitignore models/confdb.py
$ git commit -m "Introduced confdb in local branch"
```

From now on you have to use your local branch and merge the master branch
to it in order to let your app to be kept up to date.

Development knowledge and suggestions
============================

## How to run tests

```sh
$ ./web2py.py -S web2py_new_app -M -R applications/web2py_new_app/tests/*.py
```

## How to log

TODO

## Add submodules letting git ignore them

### Switch to *submodules* branch

```sh
$ git checkout submodules
```

### Add the desidered submodule

```sh
$ git add submodule <url> <path>
```

in case of javascript and css dependencies use a path like: ```static/submodules/<mylib>```

### Fix the submodule version

First go to the submodule root

```sh
$ cd <path>
```

* in case you want to use tgs
```sh
$ git checkout tags/<tagname>
```
* in case you want to use commt id
```sh
$ git checkout <commit id>
```

now go back to your project root

```sh
$ cd -
```
than you have to add to your submodules branch:
* the .gitmodules file (just the first time you add a submodule to your project)
* the <path> to your submodule

and **go back branch master**

```sh
$ git add .gitmodules <path>
$ git commit -m "Just added a submodule!"
$ git checkout master
```

## Usage of the global variale "DEVELOPMENT"

TODO

## Change the remote "origin" repository

### 1. Rename the *origin* to *root*

```sh
$ git remote rename origin root
```

### 2. Remove the pushing option for the remote *root* repository

This step is usefull for avoiding to push to the wrong repository

```sh
$ git remote set-url --push root no-pushing
```

### 3. Add a new project remote *origin* repository

```sh
$ git remote add origin <url>
```

[web2py dsn specificaton]: http://www.web2py.com/books/default/chapter/29/06/the-database-abstraction-layer#Connection-strings
[PostgreSQL doc]: http://www.postgresql.org/docs/9.3/static/
[how to]: http://www.cyberciti.biz/faq/howto-add-postgresql-user-account/


Credits
=======

Maintainer
-----------

* Manuele PESENTI <manuele@inventati.org>
