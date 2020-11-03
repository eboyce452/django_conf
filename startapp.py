from importlib import import_module
import os
import re

from django.core.management.base import CommandError
from django.core.management.templates import TemplateCommand


class Command(TemplateCommand):
    help = (
        "Creates a Django app directory structure for the given app name in "
        "the current directory or optionally in the given directory."
    )
    missing_args_message = "You must provide an application name."

    def handle(self, **options):
        app_name, target = options.pop('name'), options.pop('directory')
        self.validate_name(app_name, "app")

        # Check that the app_name cannot be imported.
        try:
            import_module(app_name)
        except ImportError:
            pass
        else:
            raise CommandError(
                "%r conflicts with the name of an existing Python module and "
                "cannot be used as an app name. Please try another name." % app_name
            )

        super(Command, self).handle('app', app_name, target, **options)

        filepathalpha = str(os.getcwd()) + '/' + (str(os.getcwd()).split('/'))[-1] + '/' + 'settings.py'
        
        with open(filepathalpha, 'r') as f:
          file_string = f.read()
          f.close()

        pattern = re.compile(r"INSTALLED_APPS\s=\s\[\n*\s*")
        matches = pattern.finditer(file_string)
        for match in matches: 
          stop = match.span()[-1]

        new_file_string = file_string[:stop] + "'" + app_name + "'" + ',' + '\n\t' + file_string[stop:]
        
        with open(filepathalpha, 'w') as f:
          f.write(new_file_string)
          f.close()

        filepathbeta = os.getcwd() + '/' + app_name + '/' + 'forms.py'

        with open(filepathbeta, 'w') as f:
            form_text = '''from django import forms
from django.core import validators'''
            f.write(form_text)
            f.close()

        filepathgamma = os.getcwd() + '/' + app_name + '/' + 'urls.py'

        with open(filepathgamma, 'w') as f:
            urls_text = '''from django.conf.urls import url
from ''' + app_name + ' import views' + '\n\n' + '''app_name = '{}'

urlpatterns = [

]'''.format(app_name)
            f.write(urls_text)
            f.close()

        filepathdelta = str(os.getcwd()) + '/' + (str(os.getcwd()).split('/'))[-1] + '/' + 'urls.py'

        with open(filepathdelta, 'r') as f:
            main_urls_text = f.read()
            f.close()

        pattern = re.compile(r'from\s(.*|\s*)admin')
        matches = pattern.finditer(main_urls_text)
        for match in matches:
            stop = match.span()[-1]

        newstring = main_urls_text[:stop] + '\n' + 'from ' + app_name + ' import views' + main_urls_text[stop:]

        with open(filepathdelta, 'w') as f:
            f.write(newstring)
            f.close()

        
