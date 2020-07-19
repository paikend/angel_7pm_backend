from rest_framework import serializers
from .models import Hacks, Application, Team
from rest_framework.fields import CurrentUserDefault


class HacksSerializer(serializers.ModelSerializer):
  current_personnel = serializers.ReadOnlyField(source='get_current_personnel')
  total_fee = serializers.ReadOnlyField(source='get_total_fee')
  host_name = serializers.ReadOnlyField(source='get_host_name')
  role = serializers.ReadOnlyField(source='get_role')
  belong = serializers.ReadOnlyField(source='get_belong')
  email = serializers.ReadOnlyField(source='get_email')

  class Meta:
        model = Hacks
        fields = (
          'id', 'title', 'started_at', 'ended_at' ,
          'fee', 'intro', 'subject', 'status',
          'max_personnel', 'team_personnel', 'created_at', 
          'updated_at', 'chat_url', 'role', 
          'current_personnel', 'total_fee', 
          'belong', 'email', 'host_name',
          # 'id','title', 'started_at', 'ended_at' 
          )
  def create(self, validated_data):
      return  super().create(validated_data)

  def update(self, instance, validated_data):
      return super().update(instance, validated_data)

class TeamSerializer(serializers.ModelSerializer):
  class Meta:
        model = Team
        fields = (
          '__all__'
          # 'id', 'hacks', 'name', 
          # 'max_personnel', 'vote',
          # 'created_at', 'updated_at', 
        )
  def create(self, validated_data):
      return  super().create(validated_data)

  #수정 및 로그 데이터
  def update(self, instance, validated_data):
      return super().update(instance, validated_data)

class ApplicationSerializer(serializers.ModelSerializer):
  class Meta:
        model = Application
        fields = (
          '__all__' 
          # 'id', 'hacks', 'team', 
          # 'user', 'is_leader', 'is_joined' 
          )
  def create(self, validated_data):
      return  super().create(validated_data)

  def update(self, instance, validated_data):
      return super().update(instance, validated_data)


