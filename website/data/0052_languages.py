#!/usr/bin/env python
#coding=utf-8
from django.contrib.auth.models import User

# import models
from website.apps.core.models import Language

ed = User.objects.get(pk=1)


L = Language.objects.create(
    language="Nakame", 
    slug="nakame-sikalan",
    dialect="Sikalan", 
    isocode="nib", 
    classification="Trans-New Guinea, Finisterre-Huon, Finisterre, Erap",
    information="",
    editor=ed
)
L.save()

L = Language.objects.create(
    language="Nakame", 
    slug="nakame-sokan",
    dialect="Sokan", 
    isocode="nib", 
    classification="Trans-New Guinea, Finisterre-Huon, Finisterre, Erap",
    information="",
    editor=ed
)
L.save()

L = Language.objects.create(
    language="Nakame", 
    slug="nakame-dzenzen",
    dialect="Dzenzen", 
    isocode="nib", 
    classification="Trans-New Guinea, Finisterre-Huon, Finisterre, Erap",
    information="",
    editor=ed
)
L.save()

L = Language.objects.create(
    language="Nakame", 
    slug="nakame-wasin",
    dialect="Wasin", 
    isocode="nib", 
    classification="Trans-New Guinea, Finisterre-Huon, Finisterre, Erap",
    information="",
    editor=ed
)
L.save()

L = Language.objects.create(
    language="Nakame", 
    slug="nakame-popof",
    dialect="Popof", 
    isocode="nib", 
    classification="Trans-New Guinea, Finisterre-Huon, Finisterre, Erap",
    information="",
    editor=ed
)
L.save()

L = Language.objects.create(
    language="Nakame", 
    slug="nakame-munguleng",
    dialect="Munguleng", 
    isocode="nib", 
    classification="Trans-New Guinea, Finisterre-Huon, Finisterre, Erap",
    information="",
    editor=ed
)
L.save()

L = Language.objects.create(
    language="Nakame", 
    slug="nakame-gufin",
    dialect="Gufin", 
    isocode="nib", 
    classification="Trans-New Guinea, Finisterre-Huon, Finisterre, Erap",
    information="",
    editor=ed
)
L.save()

L = Language.objects.create(
    language="Nuk", 
    slug="nuk-tamben",
    dialect="Tamben", 
    isocode="noc", 
    classification="Trans-New Guinea, Finisterre-Huon, Finisterre, Erap",
    information="",
    editor=ed
)
L.save()

L = Language.objects.create(
    language="Nuk", 
    slug="nuk-tunam",
    dialect="Tunam", 
    isocode="noc", 
    classification="Trans-New Guinea, Finisterre-Huon, Finisterre, Erap",
    information="",
    editor=ed
)
L.save()

L = Language.objects.create(
    language="Numanggang", 
    slug="numanggang-kawalang",
    dialect="Kawalang", 
    isocode="nop", 
    classification="Trans-New Guinea, Finisterre-Huon, Finisterre, Erap",
    information="",
    editor=ed
)
L.save()

L = Language.objects.create(
    language="Numanggang", 
    slug="numanggang-tumung",
    dialect="Tumung", 
    isocode="nop", 
    classification="Trans-New Guinea, Finisterre-Huon, Finisterre, Erap",
    information="",
    editor=ed
)
L.save()

L = Language.objects.create(
    language="Nek", 
    slug="nek-goambot",
    dialect="Goambot", 
    isocode="nif", 
    classification="Trans-New Guinea, Finisterre-Huon, Finisterre, Erap",
    information="",
    editor=ed
)
L.save()

L = Language.objects.create(
    language="Uri", 
    slug="uri-siara",
    dialect="Siara", 
    isocode="uvh", 
    classification="Trans-New Guinea, Finisterre-Huon, Finisterre, Erap",
    information="",
    editor=ed
)
L.save()

L = Language.objects.create(
    language="Uri", 
    slug="uri-sintogoro",
    dialect="Sintogoro", 
    isocode="uvh", 
    classification="Trans-New Guinea, Finisterre-Huon, Finisterre, Erap",
    information="",
    editor=ed
)
L.save()

L = Language.objects.create(
    language="Wagi", 
    slug="wagi-kamba",
    dialect="Kamba", 
    isocode="fad", 
    classification="Trans-New Guinea, Madang, Croisilles, Hanseman",
    information="",
    editor=ed
)
L.save()

L = Language.objects.create(
    language="Wagi", 
    slug="wagi-kauris",
    dialect="Kauris", 
    isocode="fad", 
    classification="Trans-New Guinea, Madang, Croisilles, Hanseman",
    information="",
    editor=ed
)
L.save()

L = Language.objects.create(
    language="Wagi", 
    slug="wagi-silibob",
    dialect="Silibob", 
    isocode="fad", 
    classification="Trans-New Guinea, Madang, Croisilles, Hanseman",
    information="",
    editor=ed
)
L.save()

L = Language.objects.create(
    language="Wagi", 
    slug="wagi-mis",
    dialect="Mis", 
    isocode="fad", 
    classification="Trans-New Guinea, Madang, Croisilles, Hanseman",
    information="",
    editor=ed
)
L.save()

L = Language.objects.create(
    language="Wagi", 
    slug="wagi-foran",
    dialect="Foran", 
    isocode="fad", 
    classification="Trans-New Guinea, Madang, Croisilles, Hanseman",
    information="",
    editor=ed
)
L.save()
