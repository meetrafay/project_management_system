from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'password2']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'password': {'required': True},
            'password2': {'required': True},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Passwords must match')
        elif User.objects.filter(email=data['email']).first():
            raise serializers.ValidationError('user already exists')
        return data

    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['email'],
            password=validated_data['password']
        )
        user.set_password(validated_data['password'])
        user.save()
        print(user.password)

        return user
    

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255, required=True)
    class Meta:

        model = User
        fields = ['email','password']
        extra_kwargs = {
            'email': {'required': True},
            'password': {'required': True},
        }