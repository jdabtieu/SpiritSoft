#!/bin/bash

# Dump the database into demo.json

mv demo.json demo-$(date | sed -e 's/[ :]/_/g').json
python manage.py dumpdata main.eventCategory main.event main.attendance main.prizeCategory main.prize main.student actions.quarterlyWinner auth.user --exclude=auth.permission --exclude=contenttypes --indent 2 > demo.json
