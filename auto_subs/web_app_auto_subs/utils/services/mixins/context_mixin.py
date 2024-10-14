
menu = [
    {'title': 'Main', 'url_name': 'main'},
    {'title': 'Upload video', 'url_name': 'upload_video'},
    # {'title': 'Профиль', 'url_name': 'personal_account'}

]

class ContextMixin:

    def get_mixin_context(self, context, **kwargs):
        context['menu'] = menu
        context['title'] = 'PAM PAM'
        context.update(kwargs)

        return context
