from rest_framework import serializers
from material.models import *


class SuperclassSerializer(serializers.ModelSerializer):
    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     if not data['description']:
    #         data['description'] = ""

    class Meta:
        model = Superclass
        fields = '__all__'


class SubclassSerializer(serializers.ModelSerializer):
    superclass = serializers.SlugRelatedField(queryset=Superclass.objects.all(), slug_field='name')

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     if not data['example']:
    #         data['example'] = ""
    #     return data

    class Meta:
        model = Subclass
        fields = '__all__'


class MediaImgSerializer(serializers.ModelSerializer):

    class Meta:
        model = MediaImg
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    record_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username', required=False)
    media_img = MediaImgSerializer(many=True, read_only=True)

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     if not data['describe']:
    #         data['describe'] = ""
    #     if not data['remark']:
    #         data['remark'] = ""
    #     return data

    class Meta:
        model = MaterialInfo
        # fields = ['id', 'item_code', 'item_name', 'describe', 'firm_code', 'firm_name', 'material_img', 'specification',
        #           'remark', 'record_time', 'user', 'media_img']
        fields = '__all__'


