# Convert
Convert odts to docx and pdf



Local Service
soffice  -env:UserInstallation=file:///tmp/xofficeuser "--accept=socket,port=2002;urp;" --invisible --headless

### curl to test conversion
curl -X POST -F "file=@fixtures/letter.odt" -F "fileType=pdf" localhost:5668/convert --verbose -o fixtures/letter.pdf



Production Service
soffice  "--accept=socket,port=2002;urp;" --invisible --headless

