mv demo.json demo-$(date | sed -e 's/[ :]/_/g').json
python manage.py dumpdata main.attendance main.eventCategory main.event main.prizeCategory main.prize main.student auth.user --indent 2 > demo.json
