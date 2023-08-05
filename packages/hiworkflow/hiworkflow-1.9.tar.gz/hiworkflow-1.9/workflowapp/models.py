from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Workflow(models.Model):
    """
    For storing Work flow description
    """
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    tasktitle = models.CharField(max_length=100, null=True)
    def __str__(self):
        return 'Workflow-{}'.format(self.id)

class State(models.Model):
    """
    For storing various states of a work flow
    """
    workflow_id = models.ForeignKey(Workflow)
    title = models.CharField(max_length=100)
    is_start = models.BooleanField(default=False)
    is_end = models.BooleanField(default=False)
    is_automated = models.BooleanField(default=False)
    
    def __str__(self):
        return 'State-{}'.format(self.id)
    
class Transition(models.Model):
    """
    For storing various states of a work flow
    """
    workflow_id = models.ForeignKey(Workflow)
    state_id = models.ForeignKey(State)
    action = models.CharField(max_length=100)
    next_state = models.ForeignKey(State, related_name="next_state_id")
    
    def __str__(self):
        return 'State-{}'.format(self.id)


class Task(models.Model):
    """
    Task created by a user
    """
    created_by = models.ForeignKey(User)
    workflow_id = models.ForeignKey(Workflow)
    title = models.CharField(max_length=50, null=True)
    description = models.TextField(max_length=300)
    current_state = models.ForeignKey(State, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return 'Task-{}'.format(self.id)


class Assignee(models.Model):
    task_id = models.ForeignKey(Task)
    assignee = models.ForeignKey(User, related_name="assignee_id")
    assigned_by = models.ForeignKey(User, related_name="assigned_by")
    def __str__(self):
        return 'Assignee-{}'.format(self.id)


class Permission(models.Model):
    task_id = models.ForeignKey(Task)
    allow_access = models.CharField(max_length=300, null=True)
    deny_access = models.CharField(max_length=300, null=True)

    def __str__(self):
        return 'Permission-{}'.format(self.id)

