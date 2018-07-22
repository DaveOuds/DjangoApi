from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from soda.models import Soda
from soda.serializers import SodaSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from soda.models import Soda
from soda.serializers import SodaSerializer

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
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def soda_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        soda = Soda.objects.get(pk=pk)
    except Soda.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SodaSerializer(soda)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SodaSerializer(soda, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        soda.delete()
        return HttpResponse(status=204)