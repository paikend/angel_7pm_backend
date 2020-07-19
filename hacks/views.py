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
import json
from django.contrib.auth import get_user_model
from config.tasks import simple_mail
User = get_user_model()
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
                if applied:
                    qs = qs.filter(id=applied.hacks.id)
                else:
                    qs = qs.filter(id=None)
        status = self.request.query_params.get('status ', None)
        if status is not 'my':
            status = 'i'
            qs = qs.filter(status = status)
        return qs
    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

    def perform_update(self, serializer):
        serializer.save(host=self.request.user)
    def create(self, request, *args, **kwargs):
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
        qs = qs.filter(user=self.request.user)
        return qs
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
    def create(self, request, *args, **kwargs):
        user = self.request.user
        h = request.data["hacks"]
        hacks = Hacks.objects.get(id=h)
        # simple_mail.delay(
        #     '[끝장개발대회] 참가 확정 안내',
        #     "안녕하세요. 참가자님!\n끝장개발대회에 참여해주셔서 감사합니다.\n\n금요일 오후 7시 전까지 아래 슬랙에 입장해주세요!\
        #     \n금요일에 만나요👋\n슬랙 참가 URL :"+ str(hacks.chat_url) +"\n",
        #     '',
        #     [user.email],
        #     fail_silently=False)
        if not isinstance(user, AnonymousUser):
            applied = Application.objects.filter(user=user).filter(hacks=h)
            if applied:
                return Response({"message":"duplicated apply"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # if serializer.data['is_paid']:

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

@api_view(['POST'])
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
                email : 팀원이메일,
                role : 팀원역할
            },
            {
                email : 팀원이메일,
                role : 팀원역할
            },  
            {                email : 팀원이메일,
                role : 팀원역할
            }, 
        ]
    }
    """
    if request.method == 'POST':
        try:
            team_name = request.data['t_name']
            leader_email = request.data['l_email']
            leader_role = request.data['ㅣ_role']
            teams = request.data['teams']
            hacks = Hacks.objects.get(id=pk)
            team = Team.objects.create(hacks = hacks, name = team_name)
            leader = User.objects.get(email=leader_email)
            if not leader:
                return Response({"message":"leader email is not vaild!"}, status=status.HTTP_400_BAD_REQUEST)
            l_apply = Application.objects.get(user=leader.id)
            print(l_apply.id)
            l_apply.save(hacks= hacks, is_leader = True, role = leader_role, mission_level="t")
            for t in teams:
                member = User.objects.get(email=t["email"])
                member.save(user = member,hacks= hacks, role = t["role"], mission_level="t")
        except Exception as e:
            return Response({"message":"member email is not vaild!"}, status=status.HTTP_400_BAD_REQUEST)

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
        try:
            hacks = Hacks.objects.get(id=pk)
            team_name = request.data['team_name']
            name = request.data['i_name']
            detail = request.data['i_detail']
            t_id = Team.objects.filter(name=team_name).filter(hacks=id).get()
            Teams.objects.save(id = t_id, service_name=name, service_detail = detail)
            teams = Application.objects.filter(team=t_id.id)
            for team in teams:
                team.save(mission_level="i")

            return Response({"message":"submit!"}, status=status.HTTP_201_CREATED)
        except Exception as e :
            return Response({"message":"submit fail"}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit(request, pk):
    """
    최종 제출 API
    {
        "team_name": "팀명(팀작성명과 같아야함), 다르면 400 에러= ",
        "i_name": "서비스명",
        "i_detail": "서비스 설명"
    }
    """
    if request.method == 'POST':
        try:
            hacks = Hacks.objects.get(id=pk)
            team_name = request.data['team_name']
            git = request.data['github']
            demo = request.data['demo']
            pitch = request.data['pitch']
            present = request.data['present']
            team = Team.objects.filter(name=team_name).filter(hacks=id).get()
            team.objects.save( github_url = git, demo_url=demo, pitch_url = pitch, present_url = present)
            members = Application.objects.filter(team=team.id)
            for member in members:
                members.save(mission_level="s")
            return Response({"message":"submit!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message":"submit fail"}, status=status.HTTP_400_BAD_REQUEST)