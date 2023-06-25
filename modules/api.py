from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.tokens import default_token_generator
import random
import hashlib
import io
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import PatientSerializer,LoginSerializer,TherapistSerializer
from .models import *
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib import auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
from .models import Patient, Therapist


#email verification
def send_verification_email(request, user):
    mail_subject = 'Verify your email'
    message = get_verification_link(request, user)
    print(message)
    send_to=[user.email]
    email=EmailMessage(mail_subject, message, 'farahhtout15@example.com', send_to)
    email.send()
    return HttpResponse('Email sent successfully!')
#generate a link for account verification based on userid and token
def get_verification_link(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return f"{request.scheme}://{request.get_host()}/verify/{uid}/{token}/"

#api
class LoginViewApi(APIView):

    def get(self, request, format=None):
        return render(request, 'login.html')

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            uname = serializer.validated_data['username']
            pwd = serializer.validated_data['password']
            user_authenticate = auth.authenticate(username=uname, password=pwd)
            if user_authenticate is not None:
                user = User.objects.get(username=uname)
                try:
                    data = Patient.objects.get(username=user)
                    auth.login(request, user_authenticate)

                    # Generate JWT token
                    refresh = RefreshToken.for_user(user_authenticate)
                    token = str(refresh.access_token)

                    response_data = {
                        "message": "success",
                        "data": {
                            "Id": data.id,
                            "Name": data.name,
                            "Email": data.email,
                            "Token": token,
                            "usertype":'patient'
                        }
                    }

                    # return redirect('dash', user='P')
                    return Response(response_data, status=status.HTTP_200_OK)

                except Patient.DoesNotExist:
                    try:
                        data = Therapist.objects.get(username=user)
                        print('therapist has been Logged')
                        auth.login(request, user_authenticate)
                        # Generate JWT token
                        refresh = RefreshToken.for_user(user_authenticate)
                        token = str(refresh.access_token)

                        response_data = {
                            "message": "success",
                            "data": {
                                "Id": data.id,
                                "Name": data.name,
                                "Email": data.email,
                                "Token": token,
                                "usertype":'doctor'
                            }
                        }
                        # return redirect('mycalendlyregister', user=user.id)
                        return Response(response_data, status=status.HTTP_200_OK)

                    except Therapist.DoesNotExist:
                        response_data = {
                            "message": "invalid username or password",
                            "data": None
                        }
                        return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
            else:
                response_data = {
                    "message": "invalid username or password",
                    "data": None
                }
                return Response(response_data ,status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class RegisterViewApi(APIView):
    
    def get(self, request, format=None):
        
        return render(request, 'register.html')

    def post(self, request, format=None):
        type = request.data.get('post')
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        try:
            user = User.objects.get(username=username)
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, email=email, password=password)

        if type == 'patient':
            serializer = PatientSerializer(data=request.data)
            if serializer.is_valid():
                user.is_active = False
                user.save()
                serializer.save(username=user)
                send_verification_email(request, user)

                # Generate JWT token
                refresh = RefreshToken.for_user(user)
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'exp': (datetime.utcnow() + timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S'),
                }

                response_data = {
                    'username': username,
                    'password': password,
                    'name': serializer.validated_data.get('name'),
                    'phone': serializer.validated_data.get('phone'),
                    'address': serializer.validated_data.get('address'),
                    'email': email,
                    'dob': serializer.validated_data.get('dob'),
                    'gender': serializer.validated_data.get('gender'),
                    'post': 'patient',
                    'token': token,
                }

                # return redirect('checkemail')
                return Response(response_data, status=status.HTTP_200_OK)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = TherapistSerializer(data=request.data)
            if serializer.is_valid():
                user.is_active = False
                user.save()
                serializer.save(username=user)
                send_verification_email(request, user)

                # Generate JWT token
                refresh = RefreshToken.for_user(user)
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'exp': (datetime.utcnow() + timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S'),
                }

                response_data = {
                    'username': username,
                    'password': password,
                    'name': serializer.validated_data.get('name'),
                    'phone': serializer.validated_data.get('phone'),
                    'address': serializer.validated_data.get('address'),
                    'email': email,
                    'dob': serializer.validated_data.get('dob'),
                    'gender': serializer.validated_data.get('gender'),
                    'post': 'therapist',
                    'token': token,
                }

                # return redirect('checkemail')
                return Response(response_data, status=status.HTTP_200_OK)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#reset password email verif send
def send_reset_pass(request, user,number):
    print("send reset pass")
    mail_subject = "Reset Your Password"
    message = str(number)  
    send_to=[user.email]
    email=EmailMessage(mail_subject, message, 'farahhtout15@example.com', send_to)
    email.send()
    return HttpResponse('Email sent successfully!')

# def hash_number(number):
#     hashed_number = hashlib.sha256(str(number).encode()).hexdigest()
#     return hashed_number

# def forgetApi(request):
#     if request.method == "POST":
#         email = request.POST['email']
#         try:
#             user = User.objects.get(email=email)
#             number=random.randint(1000, 9999)
#             hashed_number = hash_number(number)
#             send_reset_pass(request, user, number)
#             response_data = {
#                 'hashedNumber' : hashed_number,
#                 'message':'Please check your inbox'
#             }
#             return Response(response_data,status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return HttpResponse('User does not exist.')
#     return render(request,'forget.html')

