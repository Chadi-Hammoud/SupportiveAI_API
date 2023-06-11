from rest_framework import serializers
from rest_framework.settings import api_settings
from .models import *


class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = ('id','name','phone','address','email','dob','gender')

class TherapistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Therapist
        fields = ('id','name','phone','address','email','dob','gender')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = User.objects.filter(username=username).first()

            if user:
                if user.check_password(password):
                    if user.is_active:
                        payload = api_settings.JWT_PAYLOAD_HANDLER(user)
                        token = api_settings.JWT_ENCODE_HANDLER(payload)
                        return {
                            'user': user,
                            'token': token
                        }
                    else:
                        raise serializers.ValidationError("User account is disabled.")
                else:
                    raise serializers.ValidationError("Incorrect password.")
            else:
                raise serializers.ValidationError("User does not exist.")
        else:
            raise serializers.ValidationError("Must provide both username and password.")
