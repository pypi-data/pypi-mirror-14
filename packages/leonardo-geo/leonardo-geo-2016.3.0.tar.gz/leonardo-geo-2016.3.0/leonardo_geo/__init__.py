
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


default_app_config = 'leonardo_geo.Config'


class Default(object):

    optgroup = 'Geolocation'

    apps = [
        'leonardo_geo'
    ]

    widgets = [
        'leonardo_geo.models.MapLocationWidget'
    ]


class Config(AppConfig, Default):
    name = 'leonardo_geo'
    verbose_name = _("Geolocation")

default = Default()
