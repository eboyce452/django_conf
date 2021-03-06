# django_conf
Changes to Django Conf files that make full stack development a lot easier. I created this for my own use, and it is heavily customized to my preferences and my machine. You may find incompatibility issues if your directories, files, and versions are different from mine. I'm making this public use just for the heck of it, and will eventually work to making it more universal, just please don't hate me if this doesn't work perfectly for you.

--These changes were made on a machine running Ubuntu 20.04 in a virtual environment running Django 1.11.17 and Python 3.8.5, I am working on updating them to the other Django versions, but it's all straightforward enough to work out on your own if you needed to--

--It's also worth noting that as I build experience I'll be seeing if there is more I can automate using the same series of config files. If I end up building the same index page, models, forms, etc. I may end up adding commented out versions to the templates so that I can either use them and uncomment or just ignore them if they're not relevant. It would also be possible to pass in another argument when I'm running django-admin startproject/python manage.py startapp such as 'default site' that would build to those specs. I'll play around with it more in the future--

# Changes to templates.py (django --> core --> management --> templates.py):

*Automatically creates templates and static directories

*Within static directory, automatically creates directories for css and js and auto-populates blank files for each

*Also within static directory, it will create a directory called site packages; search your machine from your home directory for bootstrap.min.css, bootstrap.min.js, popper.min.js, and jquery.min.js; and then copy those files to the site package directory (ALL of these files -need- to be installed to your computer somewhere in your home directory. Eventually I will add conditionals in case you don't have them all or don't want them all.)

# Changes to manage.py startapp (django --> core --> management --> commands --> startapp.py):

*Will automatically add the app to your settings.py under INSTALLED_APPS

*Will automatically create forms.py in your app directory with 'from django import forms'

*Will automatically create urls.py in your app directory with 'from django.conf.urls import url' as well as 'from *app_name* import views' and a blank urlpatterns = [ ]

*Will update urls.py in main directory to import views.py from your app

*will automatically make a templatetags directory and an init.py file

# Changes to settings.py-tpl (django --> conf --> project_template --> project_name --> settings.py-tpl):

*Automatically creates variables for TEMPLATES_DIR and STATIC_DIR

*Adds TEMPLATES_DIR to TEMPLATES = [...'DIRS':[ ],...]

*Creates STATICFILES_DIRS = [ ] and adds STATIC_DIR to it

# Changes to models.py-tpl (django --> conf --> app_template --> models.py-tpl

*Added User model import from django.contrib.auth

# TO START A PROJECT:

*django-admin startproject projname

*cd projname

*python manage.py startapp appname

*python generate_html.py

And from there, the only things on your plate are building models, forms, views, mapping urls, and editing your html/css/js. (AKA the actual site building)
All of the setup should basically be taken care of.

## Change Log

11/10/2020 : Updated the startapp.py so that the code was much cleaner and is no longer OS dependent. It should work across all operating systems though I have not tested on Windows or Mac yet. It will also automatically create a templatetags directory and an __init__.py file in case you want custom tagging.

11/10/2020 : I also changed the shell templates. Now there is one for your base html template (django_base_html.sh) and another script for your templates that are extensions (django_extend_html.sh). You can easily use the django_base_html.sh as a normal html template since the {% block %} code shouldn't actually affect anything, though feel free to comment it out if it is causing problems. In the future, I will probably just make these templates through the django-admin startproject process by altering templates.py. For now though, I kind of like the control, and it is much easier to make multiple extension templates with the shell script.

11/11/2020 : Quick change, I ended up getting rid of the shell templates and folding them into the startapp.py file. Now a base.html and extend.html are created and named specifically for each app. To compensate for the loss of convenience provided by the shell applications, the startapp file now creates a .py file called generate_html.py. When you run it, it will ask what .html files you want to create and for which app, then it will make the html files from the extend.html template. So it is roughly as convenient, but is much better integrated as it now auto-formats the django loads with the appropriate files. Furthermore, I added an auto-generating population script called auto_populate.py if you want to fill a model with random data for testing, I added in commented out example code for basically every .py file so that you can follow a template for building models/forms, and I formatted almost all of the code (including the django templates themselves) to use os.path generic filepaths so that it is less OS specific. This is all working so smoothly that I may eventually end up creating an entirely separate application and UI to make django way more user friendly. Kind of like squarespace but including the whole stack. But that is way way down the road and my code so far has been kinda rushed and sloppy just so I can get something useable working for myself. Still, something to consider.
