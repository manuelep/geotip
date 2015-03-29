Teleservice Node
============================

## Preamble

This application is a fork of [web2py-new-app](https://github.com/manuelep/web2py-new-app)
that is an empty web2py application as it comes from the wizard of the admin web
application augmented with some useful features such as:

* A predefined logger
* A UnitTest example
* A uniformed and coded way for submodules installation
* A uniformed and coded way for distinguish DB configuration between different installations

## Presentation

**Plugin GeoTip** is a [web2py plugin][] oriented to geographical data managing.
In this very first part of its development I've started implementing support for
geometries stored in a json field in order not to deal, at the moment, with 
geographical database extensions (such as PostGIS).


## DEMO

[GEOTIP](http://manuele.pythonanywhere.com/geotip)


Python dependencies:
============================

* psycopg2 ( >= **2.5.2** )
* geojson


Other dependencies:
============================

* PostgreSQL ( >= **9.3** )

**Important** 
Other dependencies (essentially javascript libraries) will be satisfied with
submodules initialization and update


Installation steps
============================

## 1. Clone the repository

```sh
$ git clone [application repo url][] geotip
```

## 2. Init the required submodules

### 2.1. Pull and checkout into the branch containing all submodules

```sh
$ cd <app dir>/
$ git submodule init
$ git submodule update
```


## 4. Database configuration

### 4.1. Create the database

Help yourself with the [PostgreSQL doc][] or some easier [how to][] to create
a user with uid **paytor** and password **paytor** and the 2 needed database:

```sql
CREATE USER <myuser> WITH PASSWORD '<mypassword>';
CREATE DATABASE <mydb>;
GRANT ALL PRIVILEGES ON DATABASE <mydb> to <myuser>;
```

### 4.2. Demo database

For demo porposes you can escape the database setup just explained using the
[postgression][] service. See how in the next configuiration section.


## 6. Configuration (**Optional**)

**No configuration is really needed for instalation**

For special needs you can add a json file called **config.json** under
the _private_ forlder of your application with a similar structure of the defaults
dictionary you can find in file _defaults.py_ under the path _modules->config_.
You can specify only key-value pairs you intend to modify.

```python
defaults = {
    # Set DEVELOPMENT to True if this installation is for development
    # or to false if it's for production. When you'll need to distinguish the two
	# situations in your code, for example for logging purposes you can refere to
	# this parameter.
    "DEVELOPMENT": True,
    # Set migrate_anabled and migrate values to False if at the moment of the
    # installation the dedicated database is not empty and the tables described
    # in the model are already defined in the DB engine.
    "migrate": True,
    "migrate_enabled": True,
    # The connection strings to the databases
    ## Just use it for DEMO
    "db": 'postgression'
    ## 
    # "db": "postgres:psycopg2://<myuser>:<mypassword>@localhost:5432/<mydb>",
    # Add here under other variable accordingly to your needs.
	# Values could be any simple type such as string, integer, float or boolean
	# or at leas a dictionary with simple values in it.
}
```

For example if you want to re-install the application maintaining the already
present database structure and their already collected data, you just need
something like

```json
{
	"migrate": False,
	"migrate_enabled": False
}
```

Development knowledge and suggestions
============================

## How to run tests

```sh
$ ./web2py.py -S web2py_new_app -M -R applications/web2py_new_app/tests/*.py
```

Credits
=======

Maintainer
-----------

* Manuele PESENTI

  * [GitHub](https://github.com/manuelep)
  * [manuele@inventati.it](mailto:manuele@inventati.it)

[web2py dsn specificaton]: http://www.web2py.com/books/default/chapter/29/06/the-database-abstraction-layer#Connection-strings
[PostgreSQL doc]: http://www.postgresql.org/docs/9.3/static/
[how to]: http://www.cyberciti.biz/faq/howto-add-postgresql-user-account/
[web2py plugin]: http://web2py.com/books/default/chapter/29/12/components-and-plugins#Plugins
[application repo url]: http://notyetspecified
[postgression]: http://www.postgression.com/
