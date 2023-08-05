from django.contrib import admin

from workflowapp.models import Transition

from .models import Workflow, State, Task, Assignee, Permission


# Register your models here.
admin.site.register(Workflow)
admin.site.register(State)
admin.site.register(Transition)
admin.site.register(Task)
admin.site.register(Assignee)
admin.site.register(Permission)
