#nginx conf
sudo rm -r /etc/nginx/sites-enabled/default
sudo ln -s /home/box/web/etc/nginx.conf  /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart

#gunicorn conf
sudo rm -r /etc/gunicorn.d/test
sudo ln -s /home/box/web/etc/gunicorn.conf /etc/gunicorn.d/test
sudo /etc/init.d/gunicorn restart