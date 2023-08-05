from django.conf.urls import url, include

from dedal import ACTIONS_RE
from dedal.views import (
    DedalCreateView,
    DedalDeleteView,
    DedalListView,
    DedalReadView,
    DedalUpdateView,
)
from dedal.exceptions import ModelIsNotInRegisterError


class Dedal(object):
    list_view_class = DedalListView
    read_view_class = DedalReadView
    update_view_class = DedalUpdateView
    create_view_class = DedalCreateView
    delete_view_class = DedalDeleteView

    def __init__(self, model, actions):
        self.actions = actions
        self.model = model
        self.add_views_to_class(actions)

    def add_views_to_class(self, actions):
        for action in actions:
            class_view = getattr(self, '{}_view_class'.format(action))
            get_class_view = getattr(
                self, 'get_{}_view_class'.format(action), None
            )
            if get_class_view:
                class_view = get_class_view()
            setattr(self, action, class_view.as_view(
                model=self.model, action_name=action
            ))

    @property
    def model_name(self):
        return self.model._meta.model_name

    @property
    def urls(self):
        return [
            url(
                ACTIONS_RE[action],
                getattr(self, action),
                name='{}_{}'.format(self.model_name, action)
            )
            for action in self.actions
        ]


class DedalSite(object):
    def __init__(self):
        self._register = {}

    def register(self, model, actions):
        self._register[model] = Dedal(model, actions)

    def unregister(self, model):
        if not self.is_registered(model):
            raise ModelIsNotInRegisterError()
        del self._register[model]
        return True

    def is_registered(self, model):
        return model in list(self._register)

    def get_urls(self):
        urlpatterns = []
        for model, dedal in self._register.items():
            urlpatterns += [
                url(r'^{}'.format(
                    model.__name__.lower()
                ), include(dedal.urls))
            ]
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls()


site = DedalSite()
