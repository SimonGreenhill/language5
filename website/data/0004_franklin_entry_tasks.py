# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from website.apps.core.models import Source, Language
from website.apps.entry.models import Task
ed = User.objects.get(pk=1)

# SOURCES
SOURCES = {}
for s in Source.objects.all():
    SOURCES[s.slug] = s

# LANGUAGES
LANGUAGES = {}
for l in Language.objects.all():
    LANGUAGES[l.slug] = l



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language I2.purari",
    source=SOURCES["franklin-1973-b"],
    language=LANGUAGES["purari"],
    records=100,
    view="FranklinView",
    image="data/2013-04/I2.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language E11.northeast-kiwai-urama",
    source=SOURCES["wurm-1973"],
    language=LANGUAGES["northeast-kiwai-urama"],
    records=100,
    view="FranklinView",
    image="data/2013-04/E11.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language E10.tureture",
    source=SOURCES["wurm-1973"],
    language=LANGUAGES["tureture"],
    records=100,
    view="FranklinView",
    image="data/2013-04/E10.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language E8.bamu-pirupiru",
    source=SOURCES["wurm-1973"],
    language=LANGUAGES["bamu-pirupiru"],
    records=100,
    view="FranklinView",
    image="data/2013-04/E8.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language E12.waboda",
    source=SOURCES["wurm-1973"],
    language=LANGUAGES["waboda"],
    records=100,
    view="FranklinView",
    image="data/2013-04/E12.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language J1.bogaya",
    source=SOURCES["shaw-1973"],
    language=LANGUAGES["bogaya"],
    records=100,
    view="FranklinView",
    image="data/2013-04/J1.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language J7.tabo",
    source=SOURCES["wurm-1973"],
    language=LANGUAGES["tabo"],
    records=100,
    view="FranklinView",
    image="data/2013-04/J7.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language J2.duna",
    source=SOURCES["shaw-1973"],
    language=LANGUAGES["duna"],
    records=100,
    view="FranklinView",
    image="data/2013-04/J2.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language J5.saniyo-hiyewe",
    source=SOURCES["macdonald-1973"],
    language=LANGUAGES["saniyo-hiyewe"],
    records=100,
    view="FranklinView",
    image="data/2013-04/J5.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language J3.west-kewa",
    source=SOURCES["franklin-and-voorhoeve-1973"],
    language=LANGUAGES["west-kewa"],
    records=100,
    view="FranklinView",
    image="data/2013-04/J3.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language A11.simbari",
    source=SOURCES["lloyd-1973"],
    language=LANGUAGES["simbari"],
    records=100,
    view="FranklinView",
    image="data/2013-04/A11.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language A10.menya",
    source=SOURCES["lloyd-1973"],
    language=LANGUAGES["menya"],
    records=100,
    view="FranklinView",
    image="data/2013-04/A10.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language G1.ipiko",
    source=SOURCES["franklin-1973-b"],
    language=LANGUAGES["ipiko"],
    records=100,
    view="FranklinView",
    image="data/2013-04/G1.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language A12.yagwoia",
    source=SOURCES["lloyd-1973"],
    language=LANGUAGES["yagwoia"],
    records=100,
    view="FranklinView",
    image="data/2013-04/A12.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language I1.kibiri",
    source=SOURCES["wurm-1973"],
    language=LANGUAGES["kibiri"],
    records=100,
    view="FranklinView",
    image="data/2013-04/I1.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language I3.kaki-ae",
    source=SOURCES["brown-1973"],
    language=LANGUAGES["kaki-ae"],
    records=100,
    view="FranklinView",
    image="data/2013-04/I3.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language E5.southern-kiwai",
    source=SOURCES["wurm-1973"],
    language=LANGUAGES["southern-kiwai"],
    records=100,
    view="FranklinView",
    image="data/2013-04/E5.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language A1.angaataha",
    source=SOURCES["lloyd-1973"],
    language=LANGUAGES["angaataha"],
    records=100,
    view="FranklinView",
    image="data/2013-04/A1.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language A3.safeyoka",
    source=SOURCES["lloyd-1973"],
    language=LANGUAGES["safeyoka"],
    records=100,
    view="FranklinView",
    image="data/2013-04/A3.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language A2.ankave",
    source=SOURCES["lloyd-1973"],
    language=LANGUAGES["ankave"],
    records=100,
    view="FranklinView",
    image="data/2013-04/A2.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language A5.tainae",
    source=SOURCES["lloyd-1973"],
    language=LANGUAGES["tainae"],
    records=100,
    view="FranklinView",
    image="data/2013-04/A5.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language A4.baruya",
    source=SOURCES["lloyd-1973"],
    language=LANGUAGES["baruya"],
    records=100,
    view="FranklinView",
    image="data/2013-04/A4.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language A7.hamtai",
    source=SOURCES["lloyd-1973"],
    language=LANGUAGES["hamtai"],
    records=100,
    view="FranklinView",
    image="data/2013-04/A7.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language A6.kamasa",
    source=SOURCES["lloyd-1973"],
    language=LANGUAGES["kamasa"],
    records=100,
    view="FranklinView",
    image="data/2013-04/A6.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language A9.akoye",
    source=SOURCES["lloyd-1973"],
    language=LANGUAGES["akoye"],
    records=100,
    view="FranklinView",
    image="data/2013-04/A9.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language A8.kawacha",
    source=SOURCES["lloyd-1973"],
    language=LANGUAGES["kawacha"],
    records=100,
    view="FranklinView",
    image="data/2013-04/A8.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language C1.fasu",
    source=SOURCES["franklin-and-voorhoeve-1973"],
    language=LANGUAGES["fasu"],
    records=100,
    view="FranklinView",
    image="data/2013-04/C1.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language E6.kerewo",
    source=SOURCES["wurm-1973"],
    language=LANGUAGES["kerewo"],
    records=100,
    view="FranklinView",
    image="data/2013-04/E6.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language E1.northeast-kiwai-arigibi",
    source=SOURCES["wurm-1973"],
    language=LANGUAGES["northeast-kiwai-arigibi"],
    records=100,
    view="FranklinView",
    image="data/2013-04/E1.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language C6.dibiyaso",
    source=SOURCES["franklin-and-voorhoeve-1973"],
    language=LANGUAGES["dibiyaso"],
    records=100,
    view="FranklinView",
    image="data/2013-04/C6.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language C5.namumi",
    source=SOURCES["franklin-and-voorhoeve-1973"],
    language=LANGUAGES["namumi"],
    records=100,
    view="FranklinView",
    image="data/2013-04/C5.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language C4.kasua",
    source=SOURCES["franklin-and-voorhoeve-1973"],
    language=LANGUAGES["kasua"],
    records=100,
    view="FranklinView",
    image="data/2013-04/C4.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language J4.pare",
    source=SOURCES["shaw-1973"],
    language=LANGUAGES["pare"],
    records=100,
    view="FranklinView",
    image="data/2013-04/J4.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language E4.northeast-kiwai-gope",
    source=SOURCES["wurm-1973"],
    language=LANGUAGES["northeast-kiwai-gope"],
    records=100,
    view="FranklinView",
    image="data/2013-04/E4.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language G2.minanibai",
    source=SOURCES["franklin-1973-b"],
    language=LANGUAGES["minanibai"],
    records=100,
    view="FranklinView",
    image="data/2013-04/G2.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language J8.wiru",
    source=SOURCES["franklin-1973-b"],
    language=LANGUAGES["wiru"],
    records=100,
    view="FranklinView",
    image="data/2013-04/J8.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language H8.tairuma",
    source=SOURCES["brown-1973"],
    language=LANGUAGES["tairuma"],
    records=100,
    view="FranklinView",
    image="data/2013-04/H8.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language C3.kaluli",
    source=SOURCES["franklin-and-voorhoeve-1973"],
    language=LANGUAGES["kaluli"],
    records=100,
    view="FranklinView",
    image="data/2013-04/C3.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language C2.foi",
    source=SOURCES["franklin-and-voorhoeve-1973"],
    language=LANGUAGES["foi"],
    records=100,
    view="FranklinView",
    image="data/2013-04/C2.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language G3.mubami",
    source=SOURCES["franklin-1973-b"],
    language=LANGUAGES["mubami"],
    records=100,
    view="FranklinView",
    image="data/2013-04/G3.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language E7.morigi",
    source=SOURCES["wurm-1973"],
    language=LANGUAGES["morigi"],
    records=100,
    view="FranklinView",
    image="data/2013-04/E7.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language E3.northeast-kiwai-gibaio",
    source=SOURCES["wurm-1973"],
    language=LANGUAGES["northeast-kiwai-gibaio"],
    records=100,
    view="FranklinView",
    image="data/2013-04/E3.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language F1.ikobi-mena",
    source=SOURCES["franklin-1973-b"],
    language=LANGUAGES["ikobi-mena"],
    records=100,
    view="FranklinView",
    image="data/2013-04/F1.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language F2.rumu",
    source=SOURCES["franklin-1973-b"],
    language=LANGUAGES["rumu"],
    records=100,
    view="FranklinView",
    image="data/2013-04/F2.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language F3.mena",
    source=SOURCES["franklin-1973-b"],
    language=LANGUAGES["mena"],
    records=100,
    view="FranklinView",
    image="data/2013-04/F3.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language F4.omati",
    source=SOURCES["franklin-1973-b"],
    language=LANGUAGES["omati"],
    records=100,
    view="FranklinView",
    image="data/2013-04/F4.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language E2.bamu",
    source=SOURCES["wurm-1973"],
    language=LANGUAGES["bamu"],
    records=100,
    view="FranklinView",
    image="data/2013-04/E2.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language H2.orokolo-kaipi",
    source=SOURCES["brown-1973"],
    language=LANGUAGES["orokolo-kaipi"],
    records=100,
    view="FranklinView",
    image="data/2013-04/H2.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language H3.keoru-ahia",
    source=SOURCES["brown-1973"],
    language=LANGUAGES["keoru-ahia"],
    records=100,
    view="FranklinView",
    image="data/2013-04/H3.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language J6.samberigi",
    source=SOURCES["franklin-and-voorhoeve-1973"],
    language=LANGUAGES["samberigi"],
    records=100,
    view="FranklinView",
    image="data/2013-04/J6.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language H1.aheave",
    source=SOURCES["brown-1973"],
    language=LANGUAGES["aheave"],
    records=100,
    view="FranklinView",
    image="data/2013-04/H1.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language H6.sepoe",
    source=SOURCES["brown-1973"],
    language=LANGUAGES["sepoe"],
    records=100,
    view="FranklinView",
    image="data/2013-04/H6.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language H7.toaripi",
    source=SOURCES["brown-1973"],
    language=LANGUAGES["toaripi"],
    records=100,
    view="FranklinView",
    image="data/2013-04/H7.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language H4.opao",
    source=SOURCES["brown-1973"],
    language=LANGUAGES["opao"],
    records=100,
    view="FranklinView",
    image="data/2013-04/H4.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language H5.orokolo",
    source=SOURCES["brown-1973"],
    language=LANGUAGES["orokolo"],
    records=100,
    view="FranklinView",
    image="data/2013-04/H5.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language B4.folopa-suri",
    source=SOURCES["macdonald-1973"],
    language=LANGUAGES["folopa-suri"],
    records=100,
    view="FranklinView",
    image="data/2013-04/B4.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language B5.tebera",
    source=SOURCES["macdonald-1973"],
    language=LANGUAGES["tebera"],
    records=100,
    view="FranklinView",
    image="data/2013-04/B5.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language B6.uraru",
    source=SOURCES["macdonald-1973"],
    language=LANGUAGES["pawaia"],
    records=100,
    view="FranklinView",
    image="data/2013-04/B6.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language E9.bamu-sisiame",
    source=SOURCES["wurm-1973"],
    language=LANGUAGES["bamu-sisiame"],
    records=100,
    view="FranklinView",
    image="data/2013-04/E9.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language B1.dadibi",
    source=SOURCES["macdonald-1973"],
    language=LANGUAGES["dadibi"],
    records=100,
    view="FranklinView",
    image="data/2013-04/B1.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language B2.folopa-boro",
    source=SOURCES["macdonald-1973"],
    language=LANGUAGES["folopa-boro"],
    records=100,
    view="FranklinView",
    image="data/2013-04/B2.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language B3.folopa-sopese",
    source=SOURCES["macdonald-1973"],
    language=LANGUAGES["folopa-sopese"],
    records=100,
    view="FranklinView",
    image="data/2013-04/B3.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language D6.kubo",
    source=SOURCES["shaw-1973"],
    language=LANGUAGES["kubo"],
    records=100,
    view="FranklinView",
    image="data/2013-04/D6.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language D7.samo",
    source=SOURCES["shaw-1973"],
    language=LANGUAGES["samo"],
    records=100,
    view="FranklinView",
    image="data/2013-04/D7.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language D4.gobasi-honibo",
    source=SOURCES["shaw-1973"],
    language=LANGUAGES["gobasi-honibo"],
    records=100,
    view="FranklinView",
    image="data/2013-04/D4.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language D5.onabasulu",
    source=SOURCES["shaw-1973"],
    language=LANGUAGES["onabasulu"],
    records=100,
    view="FranklinView",
    image="data/2013-04/D5.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language D2.piame",
    source=SOURCES["shaw-1973"],
    language=LANGUAGES["piame"],
    records=100,
    view="FranklinView",
    image="data/2013-04/D2.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language D3.gobasi-bibo",
    source=SOURCES["shaw-1973"],
    language=LANGUAGES["gobasi-bibo"],
    records=100,
    view="FranklinView",
    image="data/2013-04/D3.png",
    completable=True,
    done=False
)
t.save()



t = Task.objects.create(
    editor=ed,
    name="Assorted Chapters from Franklin (ed). 1973",
    description="Language D1.fembe",
    source=SOURCES["shaw-1973"],
    language=LANGUAGES["fembe"],
    records=100,
    view="FranklinView",
    image="data/2013-04/D1.png",
    completable=True,
    done=False
)
t.save()


