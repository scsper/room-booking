cookbooks:
	cd cookbooks
	git clone git://github.com/opscode-cookbooks/apache2.git
	git clone git://github.com/opscode-cookbooks/apt.git
	git clone git://github.com/opscode-cookbooks/build-essential.git
	git clone git://github.com/opscode-cookbooks/git.git
	git clone git://github.com/opscode-cookbooks/vim.git
	cd ..

install:
	sudo apt-get install python-pip
	sudo pip install django

run:
	python room_scheduler/manage.py runserver [::]:8000 --settings=room_scheduler.settings.local

db: 
	python room_scheduler/manage.py syncdb --settings=room_scheduler.settings.local

test:
	python room_scheduler/manage.py test room_scheduler --settings=room_scheduler.settings.test

clean:
	rm *.pyc
