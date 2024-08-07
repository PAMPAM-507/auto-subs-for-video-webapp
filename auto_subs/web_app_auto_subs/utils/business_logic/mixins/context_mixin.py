
menu = [
    {'title': 'Главная', 'url_name': 'main'},
    {'title': 'Загрузить видео', 'url_name': 'upload_video'},
    # {'title': 'Профиль', 'url_name': 'personal_account'}

]

class ContextMixin:

    def get_mixin_context(self, context, **kwargs):
        context['menu'] = menu
        context['title'] = 'ПАМ ПАМ'
        context.update(kwargs)

        return context
