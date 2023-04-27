from rest_framework import serializers
from .models import Tagghist

class TagghistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tagghist
        fields = '__all__'
    
    