from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.utils import get_tokens_for_user
from .serializers import UserLoginSerializer, UserSerializer
from rest_framework import generics, status
from django.contrib.auth import authenticate

class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({
                'user_id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'token': token
            })
        return Response(serializer.errors)
    

class UserLoginView(APIView):
    
    def post(self, request):

        serializer = UserLoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)        
        email = serializer.data.get('email')
        password = serializer.data.get('password')  
        user = authenticate(request=request, username=email, password=password)

        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg': 'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Email or Password is not Valid'}, status=status.HTTP_404_NOT_FOUND)