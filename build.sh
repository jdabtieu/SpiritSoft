#!/bin/bash

# Builds the web app and embedded chromium browser into a desktop app

OLD_WD="$(pwd)"
rm -rf /tmp/SpiritSoftBuild
git clone $(pwd) /tmp/SpiritSoftBuild
cd /tmp/SpiritSoftBuild
pyinstaller --name=core.exe manage.py
mv dist/core.exe dist/core
sed -i 's/python manage.py/core\\core.exe/g' run.py
sed -i "s/django-insecure-.*'/$(head -c 30 /dev/urandom | xxd -ps)'/g" SpiritSoft/settings.py
cp -r actions main SpiritSoft demo.json dist/core
dist/core/core.exe migrate
dist/core/core.exe loaddata demo
pyinstaller --onefile --noconsole --icon favicon.png run.py
mv dist/run.exe dist/SpiritSoft.exe
cp favicon.png dist
cd dist
7z a SpiritSoft.zip core SpiritSoft.exe
cd "$OLD_WD"
mv /tmp/SpiritSoftBuild/dist/SpiritSoft.zip .
rm -rf /tmp/SpiritSoftBuild
