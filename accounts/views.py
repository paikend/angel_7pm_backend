
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserCreateSerializer, UserLoginSerializer
from .models import User


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_in(request):
  if request.method == 'POST':
    serializer = UserLoginSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=True):
      return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
    if serializer.validated_data['email'] == "None":
      return Response({'message': 'fail'}, status=status.HTTP_200_OK)
    query = User.objects.filter(email=serializer.validated_data['email']).values()[0]
    username = query['username']
    response = {
      'success': 'True',
      'username': username,
      'token': serializer.data['token']
    }
    return Response(response, status=status.HTTP_200_OK)