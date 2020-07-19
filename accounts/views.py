
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserCreateSerializer, UserLoginSerializer, UserSerializer
from .models import User
from hacks.models import Application, Team, Hacks
from rest_framework.viewsets import ModelViewSet

@api_view(['POST'])
@permission_classes([AllowAny])
def sign_in(request):
  """
  /accounts/sign-up/
  로그인 예시
  {
    "email":"test@test.com",
    "password": "admin12345"
  }
  """
  if request.method == 'POST':
    serializer = UserLoginSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=True):
      return Response({"message": "Request Body Error."}, status=status.HTTP_400_BAD_REQUEST)
    if serializer.validated_data['email'] == "None":
      return Response({'message': 'fail'}, status=status.HTTP_400_BAD_REQUEST)
    query = User.objects.filter(email=serializer.validated_data['email']).values()[0]
    id = query['id']
    email = query['email']
    portfolio_link = query['portfolio_link']
    name = query['name']
    belong = query['belong']
    role = query['role']
  
    data = serializer.validated_data
    response = {
      'id': id,
      'portfolio_link':portfolio_link ,
      'role' : role,
      'belong': belong,
      'name': name,
      'token': serializer.data['token']
    }
    return Response(response, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):  
  """
  /accounts/sign-up/
  회원가입 예시
  {
    "email":"test1@test.com",
    "name": "백경준",
    "belong": "코멘토",
    "role": "백엔드",
    "password": "admin12345"
  }
  """
  if request.method == 'POST':
    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=True):
      return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
    if User.objects.filter(email=serializer.validated_data['email']).first() is None:  #
      serializer.save()  
      return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
    return Response({"message": "duplicate email"}, status=status.HTTP_409_CONFLICT)




class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
      qs = super().get_queryset()
      qs = qs.filter(id = self.request.user.id)
      return qs
    def perform_update(self, serializer):
        serializer.save(user=self.request.user.id)
user_list = UserViewSet.as_view({
    'get': 'list',
    # 'post': 'create',
})
user_detail = UserViewSet.as_view({
    # 'get': 'retrieve',
    'patch': 'partial_update',
    # 'delete': 'destroy',
})
