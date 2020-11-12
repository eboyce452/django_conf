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

        filepath_proj = os.path.join(os.getcwd(),os.getcwd().split(os.sep)[-1])
        filepath_app = os.path.join(os.getcwd(), app_name)
        filepath_base = os.getcwd()

        template_path = os.path.join(filepath_base, 'templates', app_name)
        css_path = os.path.join(filepath_base, 'static', 'css', app_name)
        js_path = os.path.join(filepath_base, 'static', 'js', app_name)

        try:
            os.mkdir(template_path)
            os.mkdir(css_path)
            os.mkdir(js_path)
        except:
            raise

        css_template = '/* Blank CSS Sheet - Reset CSS with CTRL + F5 to Clear Browser Cache*/'

        with open(os.path.join(css_path, "{}.css".format(app_name)), 'w') as f:
            f.write(css_template)
            f.close()

        js_template = '// Blank Javascript File - Reset Javascript with CTRL + F5 to Clear Browser Cache'

        with open(os.path.join(js_path, '{}.js'.format(app_name)), 'w') as f:
            f.write(js_template)
            f.close()

        base_template = '''<!DOCTYPE html>

{{% load static %}}

<html>
<head>
    <title></title>
    <link rel='stylesheet' href='{{% static "sitepackages/bootstrap.min.css" %}}'>

    <link rel='stylesheet' href='{{% static "{}" %}}'>
    
    <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'>
</head>

<body>

    <!-- Insert repeated body code here -->

    <div>
        {{% block body_block %}}
        <!-- Anything outside of this will be inherited if you extend -->
        {{% endblock %}}
    </div>

    <script src='{{% static "sitepackages/jquery.min.js" %}}'></script>
    <script src='{{% static "sitepackages/popper.min.js" %}}'></script>
    <script src='{{% static "sitepackages/bootstrap.min.js" %}}'></script>

    <script src='{{% static "{}" %}}'></script>
</body>

</html>'''.format(os.path.join('css',app_name,'{}.css'.format(app_name)), os.path.join('js',app_name,'{}.js'.format(app_name)))

        extension_template = '''{{% extends "{}" %}}

{{% load {}_custom_tags %}}

{{% block body_block %}}
    <!-- Add in your body html for this page here -->
{{% endblock %}}'''.format(app_name, os.path.join(app_name,'{}_base.html'.format(app_name)))

        with open(os.path.join(template_path, '{}_base.html'.format(app_name)), 'w') as f:
            f.write(base_template)
            f.close()

        with open(os.path.join(template_path, '{}_extension.html'.format(app_name)), 'w') as f:
            f.write(extension_template)
            f.close()
        
        with open(os.path.join(filepath_proj,'settings.py'), 'r') as f:
          file_string = f.read()
          f.close()

        pattern = re.compile(r"INSTALLED_APPS\s=\s\[\n*\s*")
        matches = pattern.finditer(file_string)
        for match in matches: 
          stop = match.span()[-1]

        new_file_string = file_string[:stop] + "'" + app_name + "'" + ',' + '\n\t' + file_string[stop:]
        
        with open(os.path.join(filepath_proj,'settings.py'), 'w') as f:
          f.write(new_file_string)
          f.close()

        with open(os.path.join(filepath_app, 'forms.py'), 'w') as f:
            form_text = '''from django import forms
from django.core import validators
from django.contrib.auth.models import User
# from {}.models import model_name(s)

# In the HTML don't forget to add csrf_token!!

# class Form_Name(forms.Form):
#     name = forms.CharField()
#     email = forms.EmailField()
#     text = forms.CharField(widget = forms.Textarea)
#     botcatcher = forms.CharField(required = False, widget = forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])

# class Form_From_Model(forms.ModelForm):
#     class Meta:
#         model = model_name

#         ##Several options for how to specify fields:

#         #Option 1
#         fields = '__all__'

#         #Option 2
#         exclude = ['field_one', 'field_two'] ##include but all specified

#         #Option 3
#         fields = ('field_one', 'field_two') ##include only specified'''.format(app_name)
            f.write(form_text)
            f.close()

        with open(os.path.join(filepath_app, 'urls.py'), 'w') as f:
            urls_text = '''from django.conf.urls import url
from ''' + app_name + ' import views' + '\n\n' + '''app_name = '{}'

urlpatterns = [

]'''.format(app_name)
            f.write(urls_text)
            f.close()

        with open(os.path.join(filepath_proj, 'urls.py'), 'r') as f:
            main_urls_text = f.read()
            f.close()

        pattern = re.compile(r'from\s(.*|\s*)admin')
        matches = pattern.finditer(main_urls_text)
        for match in matches:
            stop = match.span()[-1]

        newstring = main_urls_text[:stop] + '\n' + 'from ' + app_name + ' import views' + main_urls_text[stop:]

        with open(os.path.join(filepath_proj, 'urls.py'), 'w') as f:
            f.write(newstring)
            f.close()

        try:
            os.mkdir(os.path.join(filepath_app, 'templatetags'))
        except:
            raise

        if os.path.exists(os.path.join(filepath_app, 'templatetags')) == True:
            with open(os.path.join(filepath_app, 'templatetags', '__init__.py'), 'w') as f:
                f.write('')
                f.close()

            with open(os.path.join(filepath_app, 'templatetags', '{}_custom_tags.py'.format(app_name)), 'w') as f:
                tag_template = '''from django import template

register = template.Library()

#@register.filter(name = 'filtername')
#def example(value,arg):
    #Do something to value based on arg here#
    ##Ex. return value.replace(arg,'')##
    #return value'''

                f.write(tag_template)
                f.close()

        with open(os.path.join(filepath_app, 'views.py'), 'r') as f:
            app_views_text = f.read()
            f.close()

        pattern = re.compile(r'from django.shortcuts import render')
        matches = pattern.finditer(app_views_text)
        for match in matches:
            stop = match.span()[-1]

        newstring = app_views_text[:stop] + '''from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout''' + '\n' + '#from {}.forms import Form_Name(s)\n'.format(app_name) + '#from {}.models import Model_Name(s)\n'.format(app_name) + app_views_text[stop:] + '''\n# def index(request):
#     return render(request, '{}')

# def formview(request):
#     form = Form_Name()
#     if request.method == 'POST':
#         form = Form_Name(request.POST)

#         if form.is_valid():
#             form.save(commit = True)
#             return index(request)
#         else:
#             print('Error')

#     return render(request, '{}', {{'form':form}})

# def modelview(request):
#     example_data = Model_Name.objects.all()
#     context_dict = {{'data_list':example_data}}
#     return render(request, '{}', context = context_dict)'''.format(os.path.join(app_name,'index.html'), os.path.join(app_name,'form_page.html'), os.path.join(app_name,'model_page.html'))

        with open(os.path.join(filepath_app, 'views.py'), 'w') as f:
            f.write(newstring)
            f.close()

        with open(os.path.join(filepath_app, 'models.py'), 'r') as f:
            app_models_text = f.read()
            f.close()

        newstring = app_models_text + '''\n# class Model_Name(models.Model):
        #     f_name = models.CharField(max_length = 256)
        #     l_name = models.CharField(max_length = 256)

        #     def __str__(self):
        #         return str(self.f_name + ' ' + self.l_name)'''

        with open(os.path.join(filepath_app, 'models.py'), 'w') as f:
            f.write(newstring)
            f.close()

        with open(os.path.join(filepath_base, 'auto_populate.py'), 'w') as f:
            generator_template = '''import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{}.settings')

import django
django.setup()

import faker
import random
from {}.models import #Model_Name(s)

f = faker.Faker()

def populate(N):

    for entry in range(N):

        # fake_fname = f.first_name()
        # fake_lname = f.last_name()
        # fake_email = f.free_email()

        # added_object = Model_Name.objects.get_or_create(f_name = fake_fname, l_name = fake_lname, email = fake_email)[0]

if __name__ == '__main__':

    print('populating data')
    populate(N = )
    print('data population complete')'''.format(os.getcwd().split(os.sep)[-1], app_name)
            f.write(generator_template)
            f.close()
