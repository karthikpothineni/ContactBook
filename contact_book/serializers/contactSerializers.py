from ..models.contactModels import *
from rest_framework import serializers


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        exclude = ("created_at", "updated_at")

    def create(self, validated_data):
        return Contact.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.country = validated_data.get('country', instance.country)
        instance.address = validated_data.get('address', instance.address)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ("created_at", "updated_at","password")


    def create(self, validated_data, exclude=None):
        if self.context['password']:
            validated_data['password'] = self.context['password']
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.password = validated_data.get('password',instance.password)
        instance.save()
        return instance



class TokenValidationSerializer(serializers.ModelSerializer):

    class Meta:
        model = TokenValidation
        fields = '__all__'

    def create(self, validated_data, exclude=None):
        return TokenValidation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.soft_delete=validated_data.get('soft_delete',instance.soft_delete)
        instance.save()
        return instance
