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