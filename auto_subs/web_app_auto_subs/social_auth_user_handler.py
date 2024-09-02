
from django.contrib.auth.models import Group

def new_user_handler(backend, user, response, *args, **kwargs):
    group = Group.objects.filter(name='social')
    
    if len(group):
        user.groups.add(group[0])


# from django.contrib.auth.models import Permission
# from django.contrib.auth.models import ContentType
# from django.contrib.auth.models import User

# content_type = ContentType.objects.get_for_model(User)
# permission = Permission.objects.create(
#     codename='usual_user', 
#     name='Usual user', 
#     content_type=content_type)