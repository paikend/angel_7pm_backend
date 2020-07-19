from django.db import models
from django.contrib.auth import get_user_model
from config.storage_backends import PrivateMediaStorage
from .utils import move_two_days

User = get_user_model()
class Hacks(models.Model):
  # 해커톤 제목
  title = models.CharField(help_text='해커톤 이룸', max_length = 100,  blank=True, null=True)
  # 해커톤 소개
  intro = models.TextField(help_text='해커톤 소개',blank=True, null=True)
  #  프로젝트 주제
  subject = models.TextField(help_text='해커톤 주제', blank=True, null=True)
  rule = models.TextField(help_text='해커톤 규칙',blank=True, null=True)
  # 개최자
  host = models.ForeignKey(
        'accounts.User',
        help_text='개최자',
        related_name= 'hacks',
        blank=True, null=True, on_delete=models.CASCADE,
  )
  img = models.ImageField(
        help_text='해커톤 썸네일',
        max_length=200,
        blank=True, null=True,
        upload_to='hacks/%Y/%m/%d',
        storage=PrivateMediaStorage(),
    )
  fee = models.PositiveIntegerField(
    help_text='참가 비용',
    blank=True, null=True, default = 0)
  status = models.CharField(
    max_length = 1, 
    help_text="해커톤 상태 \
            ('w', '작성(write)'),\
            ('p', '예정(plan)'),\
            ('i', '진행(ing)'),\
            ('c', '완료(complete)')",
    choices=(
            ('w', '작성(write)'),
            ('p', '예정(plan)'),
            ('i', '진행(ing)'),
            ('c', '완료(complete)'),
        ),
    blank=True, null=True
  )
  started_at = models.DateField(
    help_text='해커톤 시작일',
    blank=True, null=True)
  ended_at = models.DateField(
    help_text='예정일',
    blank=True, null=True)
  judge_line = models.TextField(
    help_text='판단 기준',
    blank=True, null=True)
  judge_day = models.PositiveIntegerField(
    help_text='해커톤이 끝나고 며칠 후 까지 심사할 지 1은 1일',
    blank=True, null=True, default = 1)
  max_personnel = models.PositiveIntegerField(
    help_text='최대 참가 인원',
    blank=True, null=True, default = 5)
  team_personnel = models.PositiveIntegerField(
    help_text='팀당 권장 인원',
    blank=True, null=True, default = 5)
  # 상 갯수 
  awards_count = models.PositiveIntegerField(
    help_text='상의 갯수',
    blank=True, null=True, default =1)
  awards = models.TextField(
    help_text='상을 받는 팀(팀의 PK를넘겨주세요\
      ex) 1,2,3,4\
    )',
    blank=True, null=True)
  created_at = models.DateTimeField(
    help_text='해커톤 생성일',
    auto_now_add=True)
  updated_at = models.DateTimeField(
    help_text='헤커톤 수정일',
    auto_now=True)
  chat_url = models.CharField(
  help_text='슬랙 URL',
    max_length = 100, blank=True, null=True)

  def save(self, force_insert=False, force_update=False, using=None,update_fields=None):
    if self.started_at is not None:
      move_two_days(date=self.started_at)
      self.ended_at = move_two_days(date=self.started_at)
    super(Hacks, self).save(force_insert, force_update, using, update_fields)
  def get_total_fee(self):
    paid_person = Application.objects.filter(hacks=self).filter(is_paid=True).count()
    if paid_person is None:
      paid_person = 0
    if self.fee is None:
      self.fee =0
    return self.fee * paid_person
  def get_current_personnel(self):
    paid_person = Application.objects.filter(hacks=self.id).filter(is_paid=True).count()
    if paid_person is None:
      paid_person = 0
    return paid_person
  def get_host_name(self):
    user = None
    if self.host:
      user = User.objects.get(email=self.host)
    name = None
    if user:
      name = user.name
    return name
  def get_role(self):
    user = None
    if self.host:
      user = User.objects.get(email=self.host)
    role = None
    if user:
      role = user.role
    return role
  def get_belong(self):
    user = None
    if self.host:
      user = User.objects.get(email=self.host)
    belong = None
    if user:
      belong = user.belong
    return belong
  def get_email(self):
    user = None
    if self.host:
      user = User.objects.get(email=self.host)
    email = None
    if user:
      email = user.email
    return email

  class Meta:
    ordering = ('created_at',)
  def __str__(self):
    return self.title
class Team(models.Model):
  # 팀원 수는 쿼리 날려서 
  hacks = models.ForeignKey(
        'hacks.Hacks',
        blank=True, null=True, 
        on_delete=models.CASCADE,
  )
  name = models.CharField(
    help_text='팀명',
    max_length = 100, blank=True, null=True)
  service_name = models.CharField(max_length=100, blank=True, null=True)
  service_detail = models.TextField(blank=True, null=True)
  github_url = models.TextField(blank=True, null=True)
  demo_url = models.TextField(blank=True, null=True)
  pitch_url = models.TextField(blank=True, null=True)
  present_url = models.TextField(blank=True, null=True)
  vote = models.PositiveIntegerField(
      help_text='투표수',
    default=0)
  created_at = models.DateTimeField(
    help_text='팀 생성일',
    auto_now_add=True)
  updated_at = models.DateTimeField(
    help_text='수정일',
    auto_now=True)
  class Meta:
    ordering = ('created_at',) 
  def __str__(self):
    return self.name
class Application(models.Model):
  hacks = models.ForeignKey(
        'hacks.Hacks',
        blank=True, null=True, 
        on_delete=models.CASCADE,
  )
  team = models.ForeignKey(
        'hacks.Team',
        blank=True, null=True,
        on_delete=models.CASCADE,
  )
  user = models.ForeignKey(
        'accounts.User',
        blank=True, null=True,
        on_delete=models.CASCADE,
  )
  # 리더 여부 
  is_leader = models.BooleanField(
        help_text='리더 여부',
    default=False, blank=True, null=True,)
  # 돈을 지불 여부 
  is_paid = models.BooleanField(
    help_text='참가비 지불 여부',
    default=False)
  is_joined = models.BooleanField(
        help_text='팀 가입 여부',
    default=False)
  # 중도 포기등을 단계로 나눔
  mission_level = models.CharField(
        blank=True, null=True,default="h",
      help_text="[미션 완료 여부] \
        h:해커톤 참여 신청,\
        s:슬랙 참여\
        d:개발링크 제출\
        v:데모영상 제출 \
        p:기획안 링크 제출 \
        t:팀빌딩 완료 \
        i:아이디어 완료",
        max_length = 7, 
        )
  role = models.CharField(
    blank=True, null=True,
    help_text="팀 역할",
    max_length = 100, 
  )
  created_at = models.DateTimeField(
    help_text='지원일',
    auto_now_add=True)
  updated_at = models.DateTimeField(
    help_text='수정일',
    auto_now=True)
  class Meta:
    ordering = ('created_at',)
  def __str__(self):
      return self.user.name