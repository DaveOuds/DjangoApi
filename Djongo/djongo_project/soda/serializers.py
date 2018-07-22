from rest_framework import serializers
from soda.models import Soda

class SodaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soda
        fields = ('_id', 'name', 'price')