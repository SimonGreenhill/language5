Language 5
==========


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