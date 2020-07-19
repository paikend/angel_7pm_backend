from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status, parsers
from .models import Hacks, Team, Application
from .serializers import HacksSerializer, TeamSerializer, ApplicationSerializer
from rest_framework.permissions import IsAuthenticated
from .permission import IsAuthenticatedOnlyNotGet
class HacksViewSet(ModelViewSet):
    """
    quertString 
    ?is_mine=true =>  자신이 참여중인 해커톤만 나옴.
    
    """
    queryset = Hacks.objects.all()
    serializer_class = HacksSerializer
    permission_classes = [IsAuthenticatedOnlyNotGet]
    # parser_classes=[FormParser, MultiPartParser] # 폼 데이터를 파싱하기 위한 클래스
    # pagination_class = CustomSetPagination

    def get_queryset(self):
        qs = super().get_queryset()
        is_mine = self.request.query_params.get('is_mine', None)
        if is_mine=="true":
            user = self.request.user
            if not isinstance(user, AnonymousUser):
                applied = Application.objects.filter(user=user).first()
                qs = qs.filter(id=applied.hacks.id)
        status = 'i'
        qs = qs.filter(status = status)
        return qs
    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

    def perform_update(self, serializer):
        serializer.save(host=self.request.user)
    def create(self, request, *args, **kwargs):
        user = self.request.user
        if not isinstance(user, AnonymousUser):
            applied = Application.objects.filter(user=user).first()
            hacks = Hacks.objects.filter(id=applied.hacks.id)
            if hacks:
                if hacks.status == 'i':
                    return Response({"message":"duplicated apply"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

hacks_list = HacksViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
hacks_detail = HacksViewSet.as_view({
    'get': 'retrieve',
    # 'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    # parser_classes=[FormParser, MultiPartParser] # 폼 데이터를 파싱하기 위한 클래스
    # pagination_class = CustomSetPagination

    def get_queryset(self):
        qs = super().get_queryset()
        return qs
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
team_list = TeamViewSet.as_view({
    'get': 'list',
    # 'post': 'create',
})
team_detail = TeamViewSet.as_view({
    'get': 'retrieve',
    # 'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

class ApplicationViewSet(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    # parser_classes=[FormParser, MultiPartParser] # 폼 데이터를 파싱하기 위한 클래스
    # pagination_class = CustomSetPagination

    def get_queryset(self):
        qs = super().get_queryset()
        return qs
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
application_list = ApplicationViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
application_detail = ApplicationViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})



from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from hacks.models import Application, Team, Hacks

# @api_view(['POST'])
@permission_classes([IsAuthenticated])
def team_build(request, pk):
    """
    팀빌딩 API
    {
        t_name : 팀이름
        l_email : 리더이메일,
        ㅣ_role : 리더 역할
        teams:[
            {
                name : 팀원이름,
                email : 리더이메일,
            },
            {
                name : 팀원이름,
                email : 리더이메일,
            },  
            {
                name : 팀원이름,
                email : 리더이메일,
            }, 
        ]
    }
    """
    if request.method == 'POST':
            team_name = request.POST.get('t_name', None)
            leader_email = request.POST.get('l_email', None)
            leader_role = request.POST.get('l_role', None)
            teams = request.POST.get('teams', None)
            teams = json.loads(teams)
            hacks = Hacks.objects.get(id=pk)
            team = Team.objects.create(hacks=hacks, name = team_name)
            leader = Application.save(hacks= hacks, is_leader = True, role = leader_role, user = User.objects.get(email=leader_email))
            for t in teams:
                leader = Application.save(hacks= hacks, role = t.role, user = User.objects.get(email=t.mail))
            return Response({"message":"submit!"}, status=status.HTTP_201_CREATED)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hacks_check(request, pk):
    """
    해커톤 신청을 했는지 확인하는 로직
    """
    applied= Application.objects.filter(user=request.user).filter(hacks=pk)
    if applied:
        return Response({"is_applied":True}, status=status.HTTP_200_OK)
    return Response({"is_applied":False}, status=status.HTTP_200_OK)
@permission_classes([IsAuthenticated])
def ideation(request, pk):
    """
    아이디에이션  API
    {
        "team_name": "팀명(팀작성명과 같아야함), 다르면 400 에러",
        "i_name": "서비스명",
        "i_detail": "서비스 설명"
    }
    """
    if request.method == 'POST':
        hacks = Hacks.objects.get(id=pk)
        team_name =request.POST.get('team_name', None)
        name = request.POST.get('i_name', None)
        detail = request.POST.get('i_detail', None)
        t_id = Team.objects.filter(name=team_name).filter(hacks=id).first()
        if t_id:
            Teams.objects.save(id = t_id, service_name=name, service_detail = detail)
            return Response({"message":"submit!"}, status=status.HTTP_201_CREATED)
        return Response({"message":"submit fail"}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit(request, pk):
    """
    최종 제출 API
    {
        "team_name": "팀명(팀작성명과 같아야함), 다르면 400 에러
        ",
        "i_name": "서비스명",
        "i_detail": "서비스 설명"
    }
    """
    if request.method == 'POST':
        hacks = Hacks.objects.get(id=pk)
        team_name = request.POST.get('team_name', None)
        git = request.POST.get('github', None)
        demo = request.POST.get('demo', None)
        pitch = request.POST.get('pitch', None)
        present = request.POST.get('≈', None)
        t_id = Team.objects.filter(name=team_name).filter(hacks=id).first()
        if t_id:
            Teams.objects.save(id = t_id ,github_url = git, demo_url=demo, pitch_url = pitch, present_url = present)
            return Response({"message":"submit!"}, status=status.HTTP_201_CREATED)
        return Response({"message":"submit fail"}, status=status.HTTP_400_BAD_REQUEST)