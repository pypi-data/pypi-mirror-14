CanvasData Utilities
=======================

.. image:: https://travis-ci.org/kajigga/py_canvas_data.svg

Full documentation 

This python module is designed to make it easy to access Canvas Data files.

Currently, this module makes it possible to:

  - Convert downloaded Canvas Data files to CSV files with headers
  - export SQL table creation statements 
  - list files for a table
  - download all files or files for a specific table
  - view the Canvas Data schema (fields, field types, etc)
  - connect to a database (uses sqlalchemy) to create tables, import data, run SQL queries


----

Module Usage
------------

This module can be used programatically in other scripts and software. An
example of creating a canvas_data object is found below.::
  
  from canvas_data_utils.canvas_data_auth import CanvasData

  canvas_data_object = CanvasData(
      API_KEY=YOUR_API_KEY ,
      API_SECRET=YOUR_API_SECRET, 
      base_folder = YOUR_BASE_DIR,
      data_folder = YOUR_DATA_DIR)

  
Once you have that object created, you can...

generate mysql table creation statements

::

  mysql_table_creation_statement = canvas_data_object.table_creation_statement('mysql')

generate sqlite table creation statements

::

  sqlite_table_creation_statement = canvas_data_object.table_creation_statement('sqlite')

generate postgres table creation statements

::

  postgres_table_creation_statement = canvas_data_object.table_creation_statement('postgres')

create tables in a database given by a connection string

::

  canvas_data_object.create_tables('sqlite:///{}'.format(db_filename))

fetch the current schema (as json)

::

  schema = canvas_data_object.fetch_schema()

get a list of columns in a table

::

  user_dim_columns = canvas_data_object.get_schema_columns( 'user_dim')

convert an text file download from TSV (Tab Separated Values) to CSV

::

  canvas_data_object.convert_tsv_to_csv(tsv_filepath)

list all the tables in the schema

::

  table_list = canvas_data_object.table_list()

download and convert all files to CSV

::

  canvas_data_object.convert_all_to_csv()

list all downloadable files for a table

::

  file_list = canvas_data_object.list_all_files('user_dim')

----

Config File
------------
You need to create a config file somewhere. This config file is a typical .INI
file. It should look something like the following example.

::

  [config]
  API_SECRET = replace_with_api_secret_from_canvas_data
  API_KEY = replace_with_api_key_from_canvas_data

  base_folder = /path/to/base/folder/for/downloads/
  data_folder = %(base_folder)s/test2

  connection_string = sqlite:///%(base_folder)s/sample.db


Note: The connection_string configuration follows the connection pattern needed
by SQLAlchemy at http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html.

This library supports any database type than SQLAlchemy does.

----

Command-line Tool
-----------------

This library includes a command line utility called `canvasdata`.

Usage
-----

::

  canvasdata [-h] [--config CONFIG] [-t TABLE] [--offline OFFLINE]
                  {convert_to_csv,import,create_tables,reset,sql_create_statement,list_files,download,sample_queries,schema}

  optional arguments:
    -h, --help            show this help message and exit
    --config CONFIG       path to the configuration file
    -t TABLE              specify a specific table
    --offline OFFLINE     run in offline mode


