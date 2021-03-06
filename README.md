Room Booking Web Scheduler
============
[![Build Status](https://travis-ci.org/scsper/room-booking.png?branch=master)](https://travis-ci.org/scsper/room-booking)

An application for churches to schedule and book rooms.

Configuring your dev environment
===============================

To create your dev environment, you need to download:
 * [Virtual Box](https://www.virtualbox.org/)
 * [Vagrant](http://www.vagrantup.com/)

After installing both, go inside room-booking/ and run:

```
$ make cookbooks
$ vagrant up
```

This command will ask Vagrant to download the Ubuntu image and install all the necessary packages for you.

To get into the environment, run:

```
$ vagrant ssh
$ cd /vagrant
```

To complete the setup, run:
```
$ make install
$ make db
```

After you're in the environment, you can:

```
$ make test // runs unit tests
$ make run // starts the server at http://127.0.0.1:8001/campus
$ make coverage // test coverage
```


