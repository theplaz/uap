UAP: Panopticlick Migrations
===

For project description, theory, and results:
http://wiki.theplaz.com/UAP:_Panopticlick_Migrations

Please note the code has been specifically designed around loading a data set from the EFF database,
converting it to my needs, and then running test cases over it.

**Author**: Michael Plasmeier http://theplaz.com  
**Date**: April 2013  
**License**: CC-BY-SA-NC 2.5

Requirements
=============
* **Python** (tested with 2.7.3)
* **MySQL**
* **Python-mysqldb** (a library to connect Python to MySQL)

Usage
=============
(again assuming have EFF database)

Note for all migrators, you can paginate results with ```migrator.py <start> <#records>```
For example, ```migrator.py 10 5``` processes rows 11, 12, 13, 14, and 15.
Both params are optional.  You can use:  
```migrator.py``` - to process all records  
```migrator.py <start>``` - to process records starting at a certain offset  
```migrator.py <start> <#records>``` - to process a given number of records from an offset  
This is handy if the process gets interrupted and you don't want to start from scratch.

Note that in many cases **it is not safe to rerun migrators over a given record set more than once**!
See the description in each file for important info if you can rerun or if you need to clear tables before hand.

##Set Up DB
1. Set up a new MySQL database for the new migration-tuned database and run schema.sql to set up the schema  
1. Set the database constants in ```config.py``` for both the old and new database

##Load DB
1. Run migrator.py to copy ```fingerprint``` and ```visit``` tables to the new db ```visit``` and ```software``` tables