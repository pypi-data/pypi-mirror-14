===========
CSVtoSQLiteDB
===========

    This class accepts a csv file and puts the contents into an SQLite database table.
    This pre--population is important in cases where you have to convert a csv file into an SQLite database and also
    when there is the need to have a prepopulated SQLite DB to use as a resource in mobile development.


    how to install
    -------
    $ pip install CSVtoSQLiteDB



    usage
    -----
    #!/usr/bin/env python
    from CSVtoSQLite import converter
    loader = converter.csvSQLiteConvert('example-sqlite-database-name.db')
    loader.loadCSVtoTable('path-to-csv', 'tableName')
    loader.loadCSVtoTable('path-to-another-csv', 'tableName2')
    loader.close()


license
-------
MIT