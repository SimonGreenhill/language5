Language 5
==========

Features:
---------

* fully scalable. 
* fast.
* automated tests for most of the code to check everything works as expected.
* everything is tracked with a version history (i.e. who edited this lexical item and when and how).
* everything is linked to a source. 
* maps of each language.
* Full data entry system: 
** allows easy adding of data (scanned images/PDF)
** pdf/images are zoomable, so you can zoom in to identify things.
* Real-time statistics:
** http://transnewguinea.org/statistics/



Needed Cronjobs:
----------------

1. Update Search Index
    ./manage.py buildwatson

2. Update website statistics
    ./manage.py update_statistics

3. Backup:
    ./manage.py dbbackup --compress
    
4. Backup Media:
    ./manage.py backup_media

5. Update Sitemap
    ./manage.py refresh_sitemap