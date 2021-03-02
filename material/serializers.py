from rest_framework import serializers
from material.models import *


class SuperclassSerializer(serializers.ModelSerializer):

    class Meta:
        model = Superclass
        fields = '__all__'


class SubclassSerializer(serializers.ModelSerializer):
    superclass = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Subclass
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    record_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = MaterialInfo
        fields = '__all__'
