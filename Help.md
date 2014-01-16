### Performing a South migration

###### For a new app:
* Look at the South docs to figure this out before you add anything to the model

###### Converting an existing app:
```
make conversion myapp
```

###### Performing the migration:
```
make migrate myapp
```


### Using the Django superuser model in shell

###### To create a superuser from scratch:
* make shell
```
	# import the model
	from django.contrib.auth.models import User

	# create the object
	u = User.objects.create("Admin")

	# set a password
	u.set_password("password")

	# assign all permissions
	# this might be optional, but to be safe
	u.is_superuser = True

	# allow it to explicitly log into the admin
	u.is_staff = True

	# save it into the database so you can use it
	u.save()
```
* this should create a superuser able to log into the django admin with username "Admin" and password "password"



###### to check if there are any superusers
* make shell
```
	# import model
	from django.contrib.auth.models import User

	# list all superusers
	User.objects.all()
```

###### to access a superuser object for editing
* make shell
```
	# import model
	from django.contrib.auth.models import User

	# access and store object
	u = User.objects.get(username)

	# where username is the string of the username
	# of the object you wish to access and edit
```