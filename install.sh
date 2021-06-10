#!/bin/bash
/var/www/venv/bin/uwsgi --stop /var/www/supplies/uwsgi.pid
rm -rf /var/www/supplies/collect_static /var/www/supplies/material /var/www/supplies/supplies
tar -xf supplies.tar -C /var/www/supplies
/var/www/venv/bin/python /var/www/supplies/manage.py collectstatic
/var/www/venv/bin/uwsgi --ini /var/www/supplies/uwsgi.ini
sudo /etc/init.d/nginx restart

# path=/home/zaba/mysqlbackup
# mysqldump -hlocalhost -uroot -p123456 supplies > $path/$today.sql
# rm -f $path/$deleday.sql