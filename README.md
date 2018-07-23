# General:
This README.md file explains how to set up a Django api using restframework and djongo to use a MongoDB database.

# Setting up Django Restframework 
1.  'virtualenv X'
2.  'source X/bin/activate'
3.  'pip install django'
4.  'pip install djangorestframework'
5.  'django-admin.py startproject project'
6.  'cd project/project'
7.  Start the MongoDB daemon 'Run: mongod'
8.  Open new terminal session and open the Mongo shell 'Run: mongo'
9.  Create a database 'Run: use DATABASE_NAME'
10. Add data to DATABASE_NAME and close the terminal session:
```
from soda.models import Soda<br/>
from soda.serializers import SodaSerializer<br/>
s = Soda(_id=1, name="Cola", price= 0.99)<br/>
s2 = Soda(_id=2, name="Sprite", price= 0.89)<br/>
s3 = Soda(_id=3, name="Fanta", price= 0.95)<br/>
s.save()<br/>
s2.save()<br/>
s3.save()<br/>
```
11. Edit project/settings.py:
```
INSTALLED_APPS += ['rest_framework']
```
# Djongo:
1. 'pip install djongo'
2. Edit settings.py :
```
    DATABASES = {
    'default': {
    	'ENGINE': 'djongo',
      'NAME':  DATABASE_NAME,
    }
	}
```
# Create an endpoint
1.  'cd project/project'
2.  'python manage.py startapp ENDPOINT'
3.  'cd ENDPOINT'
4.  'touch serializers.py urls.py'
5.  Define your model in models.py:
from django.db import models
```
    class Soda (models.Model):
        _id = models.IntegerField(primary_key=True)
        name = models.CharField(max_length=50)
        price = models.DecimalField(max_digits=2, decimal_places=2)

        class Meta:
            ordering = ('_id',)
```
6.  Create your (Model)serializer in serialize.py
```
from rest_framework import serializers
from soda.models import Soda

class SodaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soda
        fields = ('_id', 'name', 'price')
```
7.  Create Views (API-methods)
```
from rest_framework.parsers import JSONParser
from soda.models import Soda
from soda.serializers import SodaSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def soda_list(request):
    if request.method == 'GET':
        soda = Soda.objects.all()
        serializer = SodaSerializer(soda, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SodaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def soda_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        soda = Soda.objects.get(pk=pk)
    except Soda.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = SodaSerializer(soda)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SodaSerializer(soda, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        soda.delete()
        return Response(status=204)
```
8.  Add the urls
```
from django.conf.urls import url
from soda import views

urlpatterns = [
    url(r'^sodas/$', views.soda_list),
    url(r'^soda/(?P<pk>[0-24]+)/$', views.soda_detail),
]
```
9.  Hook the endpoint/app  up in the project/urls.py
```
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('soda.urls')),
]
```
10. Add the endpoint to INSTALLED_APPS in project/settings.py
```
INSTALLED_APPS += ['soda']
```
## Helpful links:
https://nesdis.github.io/djongo/different-ways-to-integrate-django-with-mongodb/
