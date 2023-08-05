import imp
from logging import exception

from django.shortcuts import  render_to_response

from workflowapp.models import Workflow, State, Transition, Task, Assignee, Permission


#from django.contrib.auth.models import User
class BuildWorkflow(object):
    """
    Class for creating workflow - adding states, transitions, precondition, triggers, start state,
    end state and dropping workflow
    """
    workflow_id=""
    conditions = {}
    triggers = {}
    
    def __init__(self, title, description = "", tasktitle = "flow"):
        """
        Constructor to Initialize object of class BuildWorkflow
        """
        try:
            new_workflow = Workflow.objects.update_or_create(title = title, description = description, tasktitle = tasktitle)
            self.workflow_id = new_workflow[0].id
        except exception:
            self
        
    
                
    def create_workflow(self, title, description = "", tasktitle = "flow"):
        """
        Function to create Workflow and store it in database
        """
        new_workflow = Workflow(title = title, description = description, tasktitle = tasktitle)
        try:
            new_workflow = Workflow.objects.update_or_create(title = title, description = description, tasktitle = tasktitle)
            self.workflow_id = new_workflow.id
            return self
        except exception:
            return self
    
        
    def add_states(self, state_list):
        """
        Function to add states of a workflow in the database
        """
        workflow_id = Workflow.objects.filter(id = self.workflow_id)
        for states in state_list:
            #new_state = State(workflow_id = self.workflow_id, title = states)
            try:
                State.objects.update_or_create(workflow_id = workflow_id[0], title = states)
            except exception:
                return self
            
        return self
    
    def make_automated_state(self, state_list):
        """
        Function to add automated field to the states of a workflow in the database
        """
        workflow_id = Workflow.objects.filter(id = self.workflow_id)
        for states in state_list:
            State.objects.filter(workflow_id = workflow_id[0], title = states).update(is_automated = True)

        return self
    
        
    def add_transition(self, prestate, condition, poststate, preconditions=[]):
        """
        Function to add transition between states of a workflow and add precondition for a transition
        """
        prestate = State.objects.filter(workflow_id = self.workflow_id , title = prestate)
        poststate = State.objects.filter(workflow_id = self.workflow_id , title = poststate)
        current_workflow = Workflow.objects.filter(id = self.workflow_id)    
        Transition.objects.update_or_create(workflow_id = current_workflow[0], state_id = prestate[0], action = condition, next_state = poststate[0])
        transition = Transition.objects.filter(workflow_id = current_workflow[0], state_id = prestate[0])
        list = []
        for precondition in preconditions:
            list.append(precondition)
        self.conditions.update({transition[0].id : list})
        return self
    
    
    def add_precondition(self, prestate, condition, poststate, preconditions=None):
        """
        Function to add a preconditon for a transition
        """
        prestate = State.objects.filter(workflow_id = self.workflow_id , title = prestate)
        poststate = State.objects.filter(workflow_id = self.workflow_id , title = poststate)
        current_workflow = Workflow.objects.filter(id = self.workflow_id)    
        Transition.objects.update_or_create(workflow_id = current_workflow[0], state_id = prestate[0], action = condition, next_state = poststate[0])
        transition = Transition.objects.filter(workflow_id = current_workflow[0], state_id = prestate[0])
        condition_list = []
        for precondition in preconditions:
            condition_list.append(precondition)
        self.conditions.update({transition[0].id : list})
        return self
        
        
    def add_trigger(self, state_title, triggers):
        """
        Function to add trigger for a transition - which should be invoked on successful transtion
        """
        state_id = State.objects.filter(workflow_id = self.workflow_id , title = state_title)
        trigger_list = []
        for trigger in triggers:
            trigger_list.append(trigger)
        self.triggers.update({state_id[0].id : trigger_list})
        return self
        """
        library = imp.load_source('test', filename)
        getattr(library,triggers)()
        """
    
    
    def set_start_state(self, state_title):
        """
        Function to set a state as start state
        """
        State.objects.update_or_create(workflow_id = self.workflow_id , title = state_title, defaults={'is_start': True} )
        return self
    
    
    def set_end_state(self, state_title):
        """
        Function to set a state as end state
        """
        State.objects.update_or_create(workflow_id = self.workflow_id , title = state_title, defaults={'is_end': True} )
        return self
    
    def drop_workflow(self):
        """
        Function to drop a Workflow
        """
        Workflow.objects.filter(id = self.workflow_id).delete()

    def get_workflow_name(self):
        """
        Function to return workflow name
        """
        workflow_obj = Workflow.objects.filter(id = self.workflow_id)
        return workflow_obj.title
    
    def get_open_task_list(self):
        
        workflow_id = Workflow.objects.filter(id = self.workflow_id)
        all_tasks = Task.objects.filter(workflow_id = workflow_id[0],is_active = True)
        list_all_tasks=[]
        
        for tasks in all_tasks:
            list_all_tasks.append(tasks)
            
        return list_all_tasks
    
    def get_close_task_list(self):
        
        workflow_id = Workflow.objects.filter(id = self.workflow_id)
        all_tasks = Task.objects.filter(workflow_id = workflow_id[0],is_active = False)
        list_all_tasks=[]
        
        for tasks in all_tasks:
            list_all_tasks.append(tasks)
            
        return list_all_tasks
    
    
    def visualize(self):
        start_state = State.objects.filter(workflow_id = self.workflow_id, is_start=True)
        end_states = State.objects.filter(workflow_id = self.workflow_id, is_end=True)
        all_states = State.objects.filter(workflow_id = self.workflow_id)
        result = {} 
        state_list=[]
        state_index = {}
        
        state_list.append(start_state[0].title)
        state_index.update({start_state[0].title: 0})
        count = 1

        for states in all_states:
            if not(states.is_start==True or states.is_end==True):
                state_list.append(states.title)
                state_index.update({states.title: count})
                count = count + 1
        
        for states in end_states:
            state_list.append(states.title)
            state_index.update({states.title: count})
            count = count + 1
        
        transition_list1=[]
        transition_list2=[]
        transition_list3=[]    
        all_transitions = Transition.objects.filter(workflow_id = self.workflow_id)
        for transitions in all_transitions:
            transition_list1.append(state_index[transitions.state_id.title])
            transition_list2.append(transitions.action)
            transition_list3.append(state_index[transitions.next_state.title])
        
        workflowname = Workflow.objects.filter(id = self.workflow_id)
        workflowname = workflowname[0].title
        result.update({'state_list':state_list ,'transition_list1':transition_list1,'transition_list2':transition_list2,
                       'transition_list3':transition_list3 ,'workflowname':workflowname})
        return result
        
    
class BuildTask(object):
    """
    Class to create a task and perform various operations on a task - start task, transition on a task,
    assignment of a task to a specific user, allowing or denying access, checking if a user has permission 
    for a task.
    """
    current_state = ""
    workflow_obj = None
    workflow_id = ""
    title = ""
    task_id = ""
    parameter = ""
    
    def __init__(self, workflow_object, created_by, task):
        """
        Constructor to initialize an object of class BuildTask
        """
        workflow_obj =  Workflow.objects.filter(id = workflow_object.workflow_id)
        new_task = Task.objects.update_or_create(created_by = created_by, workflow_id = workflow_obj[0], title = task, is_active=True)
        
        print new_task
        
        self.workflow_id = workflow_obj[0].id
        self.current_state = "Initialized"
        self.title = task
        self.task_id = new_task[0].id
        self.workflow_obj = workflow_object
        
    def create_task(self, workflow_object, created_by, task):
        """
        Function to create a new task
        """
        workflow_obj =  Workflow.objects.filter(id = workflow_object.workflow_id)
        new_task = Task.objects.update_or_create(created_by = created_by, workflow_id = workflow_obj[0], title = task, is_active=True)
        
        print new_task
        
        self.workflow_id = workflow_obj[0].id
        self.current_state = "Initialized"
        self.title = task
        self.task_id = new_task[0].id
        self.workflow_obj = workflow_object
            
        return self
    
    def start(self):
        """
        Function to start a task and initialize its current state to start state
        """
        all_states = State.objects.filter(workflow_id = self.workflow_id, is_start = True)
        self.current_state = all_states[0]
        Task.objects.update_or_create(workflow_id = self.workflow_id , title = self.title, defaults={'current_state': all_states[0]})
        return self
    
    def get_current_state(self):
        current_task = Task.objects.filter(id=self.task_id)
        current_state = State.objects.filter(id = current_task[0].current_state.id)
        return current_state[0].title
    
    def get_possible_actions(self):
        current_task = Task.objects.filter(id=self.task_id)
        current_state = State.objects.filter(id = current_task[0].current_state.id)
        all_transitions = Transition.objects.filter(state_id = current_state[0])
        possible_actions = []
        for transition in all_transitions:
            possible_actions.append(transition.action)
            
        return possible_actions
    
    def assignment(self, assignee_id, logged_user):
        """
        Function to assign a task to a specific user
        """
        current_task = Task.objects.filter(id=self.task_id)
        Assignee.objects.update_or_create(task_id = current_task[0],assignee = assignee_id[0],assigned_by = logged_user)
        return self
    
    def transition(self, transition_action = None):
        """
        Function to make transition of a task to next state after checking if preconditions are 
        satisfied and user has the permission. On successful transition the triggers are invoked.
        """
        current_task = Task.objects.filter(id=self.task_id)
        current_state = State.objects.filter(id = current_task[0].current_state.id)
        
        print "Current State", current_task[0].current_state.id
        
        """
        Checking for automated transition based on conditions and invoking triggers
        """
        
        if current_state[0].is_end == False and current_state[0].is_automated == True:
            conditional_transitions = Transition.objects.filter(state_id = current_state[0])
            
            for conditional_transition in conditional_transitions:
                
                if conditional_transition.id in self.workflow_obj.conditions.keys():
                    conditions = self.workflow_obj.conditions[conditional_transition.id]
                    
                    for condition in conditions:
                        if condition() == True:
                            Task.objects.filter(id = current_task[0].id).update(current_state = conditional_transition.next_state)
                            self.current_state = current_task[0].current_state
                            self.transition(transition_action)
                            return self
        
        """
        Checking for manual transitions based on conditions and invoking triggers
        """                        
        if transition_action:
            
            print current_state[0]
            state_transition = Transition.objects.filter(state_id = current_state[0],action = transition_action)
            print state_transition[0]
            precondition_flag = True
            preconditions = self.workflow_obj.conditions[state_transition[0].id]  
            for precondition in preconditions:
                if precondition() == False:
                    precondition_flag = False
            if precondition_flag:
                if current_state[0].id in self.workflow_obj.triggers.keys():
                    triggers = self.workflow_obj.triggers[current_state[0].id]
                    print triggers
                    for trigger in triggers:
                        trigger()
                        print "Triggers"
                    
                if state_transition:
                    Task.objects.filter(id = current_task[0].id).update(current_state = state_transition[0].next_state)
                    self.current_state = current_task[0].current_state
                    print "Current State", current_task[0].current_state.id
                    
                    print "Transition to next state done"             
        print "Current Updated State", current_task[0].current_state.id
        return self
    
    def allow_access(self, group_name):
        """
        Function to allow access for a task to a group
        """
        current_task = Task.objects.filter(id=self.task_id)
        Permission.objects.update_or_create(task_id = current_task[0], allow_access = group_name)
           
    def deny_access(self, group_name):
        """
        Function to deny access to a group for a task
        """
        current_task = Task.objects.filter(id=self.task_id)
        Permission.objects.update_or_create(task_id = current_task[0], deny_access = group_name)
        
    def has_permission(self, user):
        """
        Function to check if a user has permission to access the task or not
        """
        group = "Developer"
        allow_permission = Permission.objects.filter(task_id = self.task_id, allow_access = group)
        deny_permission = Permission.objects.filter(task_id = self.task_id, deny_access = group)
        if allow_permission and not(deny_permission):
            return True
        return False


def visualize_workflow(approval_workflow):
    result = approval_workflow.visualize()
    return render_to_response('visualize.html',{'result':result})


def get_assigned_tasks(user_object):
    """
        Function to return the names of all tasks assigned to a person
        """
    task_list = Assignee.objects.filter(assignee = user_object)
    return task_list

def tasks_assigned_by(user_object):
    """
        Function to return the names of all tasks assigned by a person
    """
    task_list = Assignee.objects.filter(assigned_by = user_object)
    return task_list

def user_tasks(user_object):
    """
        Function to return the names of all tasks created by a person
    """
    task_list = Task.objects.filter(created_by = user_object)
    return task_list

def all_workflows():
    """
        Function to return the names of all tasks created by a person
    """
    workflows_list = Workflow.objects.all()
    list_of_workflows=[]
    for workflows in workflows_list:
        list_of_workflows.append(workflows.title)
    return list_of_workflows