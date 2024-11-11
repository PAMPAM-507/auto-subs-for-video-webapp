
from django.db.models.base import Model as Model

from web_app_auto_subs.models import ChangeEmailModel


class ChangeEmailMixin():
    
    @staticmethod
    def mark_user_for_changing_password(user: Model, email: str) -> None:
        
        
        changing = ChangeEmailModel.objects.filter(user=user)
        
        if changing:
            changing.update(email2=email)
            
        else:
            obj = ChangeEmailModel(user=user, email2=email)
            obj.save()
        
        # user.is_active = False
        # user.save()
        