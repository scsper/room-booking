install:
	sudo apt-get install python-pip
	sudo pip install django

run:
	python retreat/manage.py runserver [::]:8000

clean:
	rm *.pyc
