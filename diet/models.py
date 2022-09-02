from django.db import models
from django.contrib.auth.models import User

class User(User):
    pass

class Food(models.Model):
    name = models.TextField()
    scientific_name = models.TextField()
    description = models.TextField()
    group_id = models.IntegerField()
    subgroup_id = models.IntegerField(default=200)

class Foodgroup(models.Model):
    group_name = models.TextField(unique=True)

class Subgroup(models.Model):
    name = models.TextField(unique=True)

class Record(models.Model):
    user_id = models.IntegerField()
    time = models.DateTimeField(auto_now=False, auto_now_add=True)
    vf_amt = models.IntegerField()
    protein_amt = models.IntegerField()
    grain_amt = models.IntegerField()
    liquid_amt = models.IntegerField()
    other_amt = models.IntegerField()