# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from website.apps.core.models import Family

FAMILIES = [
    ('Trans-New Guinea', 'transnewguinea'),
    ('Austronesian', 'austronesian'),
    ('Isolate', 'isolate'),
    ('Lakes Plain', 'lakesplain'),
    ('Tor-Kwerba', 'torkwerba'),
    ('East Geelvink Bay', 'eastgeelvinkbay'),
    ('Mairasi', 'mairasi'),
    ("East Bird's Head", 'eastbirdshead'),
    ('Border', 'border'),
    ('Amto-Musan', 'amtomusan'),
    ('Arai-Kwomtari', 'araikwomtari'),
    ('Eastern Trans-Fly', 'easterntransfly'),
    ('Kaure', 'kaure'),
    ('Left May', 'leftmay'),
    ('Lower Mamberamo', 'lowermamberamo'),
    ('Maybrat', 'maybrat'),
    ('Nimboran', 'nimboran'),
    ('Pauwasi', 'pauwasi'),
    ('Piawi', 'piawi'),
    ('Lower Sepik-Ramu', 'lowersepikramu'),
    ('Sepik', 'sepik'),
    ('Senagi', 'senagi'),
    ('Sko', 'sko'),
    ('South-Central Papuan', 'scpapuan'),
    ('Somahai', 'somahai'),
    ('Torricelli', 'torricelli'),
    ('West Papuan', 'westpapuan'),
    ('Yuat', 'yuat'),
]


ed = User.objects.get(pk=1)

for family, slug in FAMILIES:
    f = Family.objects.create(family=family, slug=slug, editor=ed)
    f.save()
