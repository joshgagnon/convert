# Convert
Convert odts to docx and pdf



Local Service
soffice  -env:UserInstallation=file:///tmp/xofficeuser "--accept=socket,port=2002;urp;" --invisible --headless

### curl to test conversion
curl -X POST -F "file=@fixtures/letter.odt" -F "fileType=pdf" localhost:5668/convert --verbose -o fixtures/letter.pdf



Production Service
soffice  "--accept=socket,port=2002;urp;" --invisible --headless

# convert.service
/etc/systemd/system/convert.service
[Unit]
Description=Convert uwsgi
After=network.target

[Service]
User=convert
ExecStart=/var/www/sign/bin/uwsgi  /var/www/convert/convert.ini
Restart=always

[Install]
WantedBy=multi-user.target


# soffice.service
# /etc/systemd/system/soffice.service
[UNIT]
Description=Libre Office Headless
After=network.target

[Service]
ExecStart=/usr/bin/soffice "--accept=socket,port=2002;urp;" --invisible --headless

[Install]
WantedBy=multi-user.target



# production deployment
sudo adduser --disabled-password convert
sudo apt-get install python3-dev python3-pip libreoffice
sudo pip3 install --upgrade pip
sudo pip3 install virtualenv

sudo touch /var/log/convert.log
sudo chown convert:convert /var/log/convert.log

cd /var/www
sudo git clone https://github.com/joshgagnon/convert.git
cd convert
sudo chown -R convert:convert .
sudo su convert
virtualenv -p /usr/bin/python3.5 .
source bin/activate
pip install uwsgi
python setup.py install


# nginx conf
server {
    listen 80 http2;
    server_name conversion.catalex.nz;


    client_body_in_file_only clean;
    client_body_buffer_size 32K;

    client_max_body_size 300M;

    sendfile on;
    send_timeout 300s;

    location / {
            include uwsgi_params;
            uwsgi_pass 127.0.0.1:5668;
    }


     gzip on;
     gzip_disable "msie6";
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 9;
    gzip_buffers 16 8k;
    gzip_http_version 1.1;
    gzip_types text/plain text/css application/json application/x-font-woff application/x-javascript text/xml application/xml application/xml+rss text/javascript application/javascript;

}