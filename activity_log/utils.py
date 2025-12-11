from .models import Activity

def log_activity(user, action):
    
    Activity.objects.create(
        user= user,
        action_performed =action,
    )