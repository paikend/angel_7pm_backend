from django.db import models

# Create your models here.
class Hacks(models.Model):
  title = models.CharField(max_length = 100, blank=True, null=True)
  # plan , do, complete
  host = models.ForeignKey(
        'accounts.User',
        related_name= 'hacks',
        blank=True, null=True, on_delete=models.CASCADE,
  )
  state = models.CharField(max_length = 1, blank=True, null=True)
  started_at = models.DateTimeField(blank=True, null=True)
  ended_at = models.DateTimeField(blank=True, null=True)
  hacks_rule = models.TextField(blank=True, null=True)
  max_personnel =  models.PositiveIntegerField(blank=True, null=True, default = 5)
  created_at = models.DateTimeField(auto_now=True)
  updated_at = models.DateTimeField(auto_now_add=True)

class Team(models.Model):
  hacks = models.ForeignKey(
        'hacks.Hacks',
        blank=True, null=True, 
        on_delete=models.CASCADE,
  )
  user = models.ForeignKey(
        'accounts.User',
        blank=True, null=True, on_delete=models.CASCADE,
  )
  is_leader = models.BooleanField(default=False, blank=True, null=True,)
  name = models.CharField(max_length = 100, blank=True, null=True)
  max_personnel = models.PositiveIntegerField(blank=True, null=True, default = 5)
  created_at = models.DateTimeField(auto_now=True)
  updated_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
  parent = models.ForeignKey('self', related_name="child_comment",
  blank=True, null=True, on_delete=models.CASCADE,)
  user = models.ForeignKey(
        'accounts.User',
        related_name= 'comments',
        blank=True, null=True, on_delete=models.CASCADE,
  )
  # find team , generel
  type = models.CharField(blank=True, null=True, max_length=1 )
  hacks = models.ForeignKey(
        'hacks.Hacks',
        related_name= 'comments',
        blank=True, null=True, 
        on_delete=models.CASCADE,
  )
  team = models.ForeignKey(
        'hacks.Team',
        related_name= 'comments',
        blank=True, null=True, 
        on_delete=models.CASCADE,
  )
  created_at = models.DateTimeField(auto_now=True)
  updated_at = models.DateTimeField(auto_now_add=True)
  class Meta:
    ordering = ["created_at"]