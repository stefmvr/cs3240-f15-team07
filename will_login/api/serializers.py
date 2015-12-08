from rest_framework import serializers
from api.models import api, LANGUAGE_CHOICES, STYLE_CHOICES
from api.models import report_api, LANGUAGE_CHOICES, STYLE_CHOICES
from api.models import report2_api, LANGUAGE_CHOICES, STYLE_CHOICES


class apiSerializer(serializers.ModelSerializer):
   class Meta:
        model = api
        fields = ('username', 'password',)

        def create(self, validated_data):
            """
            Create and return a new `Snippet` instance, given the validated data.
            """
            return api.objects.create(**validated_data)

        def update(self, instance, validated_data):
            """
            Update and return an existing `Snippet` instance, given the validated data.
            """
            instance.username = validated_data.get('username', instance.username)
            instance.password =  validated_data.get('password', instance.password)
            instance.save()
            return instance

class reportsSerializer(serializers.ModelSerializer):
   class Meta:
        model = report_api
        fields = ('report_title', 'report_body', 'id_num')

        def create(self, validated_data):
            """
            Create and return a new `Snippet` instance, given the validated data.
            """
            return report_api.objects.create(**validated_data)

        def update(self, instance, validated_data):
            """
            Update and return an existing `Snippet` instance, given the validated data.
            """
            instance.report_title  = validated_data.get('report_title', instance.report_title)
            instance.report_body  =  validated_data.get('report_body', instance.report_body)
            instance.id_num  =  validated_data.get('id_num', instance.id_num)
            instance.save()
            return instance

class filesSerializer(serializers.ModelSerializer):
   class Meta:
        model = report2_api
        fields = ('file_name',)

        def create(self, validated_data):
            """
            Create and return a new `Snippet` instance, given the validated data.
            """
            return api.objects.create(**validated_data)

        def update(self, instance, validated_data):
            """
            Update and return an existing `Snippet` instance, given the validated data.
            """
            instance.file_name = validated_data.get('file_name', instance.file_name)
            instance.save()
            return instance
