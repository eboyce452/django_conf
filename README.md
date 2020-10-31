# django_conf
Changes to Django Conf files that make full stack development a lot easier. I created this for my own use, and it is heavily customized to my preferences and my machine. You may find incompatibility issues if your directories, files, and versions are different from mine. I'm making this public use just for the heck of it, and will eventually work to making it more universal, just please don't hate me if this doesn't work perfectly for you.

--These changes were made in a virtual environment running Django 1.11.17, I am working on updating them to the other Django versions, but it's all straightforward enough to work out on your own if you needed to--

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

# Changes to settings.py-tpl (django --> conf --> project_template --> project_name --> settings.py-tpl):

*Automatically creates variables for TEMPLATES_DIR and STATIC_DIR

*Adds TEMPLATES_DIR to TEMPLATES = [...'DIRS':[ ],...]

*Creates STATICFILES_DIRS = [ ] and adds STATIC_DIR to it

# django_html.sh:

*Shell script that will create an html template formatted for django

*Includes filepaths to sitepackages and static loads them in

*Includes commented out tags for adding the css and js files created by the templates.py file

# TO START A PROJECT:

*django-admin startproject projname

*cd projname

*python manage.py startapp appname

*cd ../django_html.sh > ./templates/filename.html

And from there, the only things on your plate are building models, forms, views, mapping urls, and editing your html/css/js. (AKA the actual site building)
All of the setup should basically be taken care of.
