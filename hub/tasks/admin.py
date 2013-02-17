# -*- coding: utf-8 -*-

"""
admin.py
Auto-register admin classes based on models in your project
Questions? email: dodgyville@gmail.com
"""
from django.contrib import admin
from django.db import models as dmodels
from django.db.models import Field
import models

#get the models from myproject.models]
mods = [x for x in models.__dict__.values() if issubclass(type(x), dmodels.base.ModelBase)]

admins = []
#for each model in our models module, prepare an admin class
#that will edit our model (Admin<model_name>, model)
for c in mods:
	admins.append(("%sAdmin"%c.__name__, c))

#create the admin class and register it
for (ac, c) in admins:
    try: #pass gracefully on duplicate registration errors
        admin_class = type(ac, (admin.ModelAdmin,), dict())
        admin_class.list_display = tuple(x.name for x in c._meta.fields
            if issubclass(type(x), Field))
        admin.site.register(c, admin_class)
    except:
        pass