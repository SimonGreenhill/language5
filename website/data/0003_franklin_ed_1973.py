# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from website.apps.core.models import Source, Language, Family, AlternateName

ed = User.objects.get(pk=1)

s = Source.objects.create(
    year = 1973,
    editor = ed,
    author = "Lloyd",
    slug = "lloyd-1973",
    reference = "Lloyd, RG. 1973. The Angan Language Family. Pp. 31-107. In Franklin, KJ. (Ed). The Linguistic Situation in the Gulf District and Adjacent Area, Papua New Guinea. Canberra: Pacific Linguistics"
)
s.save()


s = Source.objects.create(
    year = 1973,
    editor = ed,
    author = "Franklin and Voorhoeve",
    slug = "franklin-and-voorhoeve-1973",
    reference = "Franklin, KJ & Voorhoeve, CL. 1973. Languages near the intersection of the Gulf, Southern Highlands, and Western Districts. Pp. 149-152. In Franklin, KJ. (Ed). The Linguistic Situation in the Gulf District and Adjacent Area, Papua New Guinea. Canberra: Pacific Linguistics"
)
s.save()


s = Source.objects.create(
    year = 1973,
    editor = ed,
    author = "Macdonald",
    slug = "macdonald-1973",
    reference = "MacDonald, GE. 1973. The Teberan Language Family. Pp. 111-121. In Franklin, KJ. (Ed). The Linguistic Situation in the Gulf District and Adjacent Area, Papua New Guinea. Canberra: Pacific Linguistics"
)
s.save()


s = Source.objects.create(
    year = 1973,
    editor = ed,
    author = "Wurm",
    slug = "wurm-1973",
    reference = "Wurm, SA. 1973. The Kiwaian Language Family. Pp. 217-224. In Franklin, KJ. (Ed). The Linguistic Situation in the Gulf District and Adjacent Area, Papua New Guinea. Canberra: Pacific Linguistics"
)
s.save()


s = Source.objects.create(
    year = 1973,
    editor = ed,
    author = "Shaw",
    slug = "shaw-1973",
    reference = "Shaw, RD. 1973. A tentative classification of the languages of the Mt Bosavi region. Pp. 187-214. In Franklin, KJ. (Ed). The Linguistic Situation in the Gulf District and Adjacent Area, Papua New Guinea. Canberra: Pacific Linguistics"
)
s.save()


s = Source.objects.create(
    year = 1973,
    editor = ed,
    author = "Franklin",
    slug = "franklin-1973-b",
    reference = "Franklin, KJ. 1973. Other language groups in the Gulf District and Adjacent Areas. Pp. 261-277 In Franklin, KJ. (Ed). The Linguistic Situation in the Gulf District and Adjacent Area, Papua New Guinea. Canberra: Pacific Linguistics"
)
s.save()

s = Source.objects.create(
    year = 1973,
    editor = ed,
    author = "Brown",
    slug = "brown-1973",
    reference = "Brown, HA. 1973. The Eleman language family. Pp. 279-374. In Franklin, KJ. (Ed). The Linguistic Situation in the Gulf District and Adjacent Area, Papua New Guinea. Canberra: Pacific Linguistics"
)
s.save()



# - LANGUAGES ----

l = Language.objects.create(editor=ed,
    language = "Purari",
    slug = "purari",
    isocode = "iar",
    classification = "Trans-New Guinea, Eleman, Purari"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))


l = Language.objects.create(editor=ed, 
    language = "Northeast Kiwai (Urama)",
    slug = "northeast-kiwai-urama",
    isocode = "kiw",
    classification = "Trans-New Guinea, Kiwaian"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

l = Language.objects.create(editor=ed, 
    language = "Angaataha",
    slug = "angaataha",
    isocode = "agm",
    classification = "Trans-New Guinea, Angan, Angaatiha"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))


l = Language.objects.create(editor=ed, 
    language = "Safeyoka",
    slug = "safeyoka",
    isocode = "apz",
    classification = "Trans-New Guinea, Angan, Nuclear Angan"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))
a = AlternateName.objects.create(
    language=l, editor=ed, name="Ampale", slug="ampale"
)
a.save()


l = Language.objects.create(editor=ed, 
    language = "Ankave",
    slug = "ankave",
    isocode = "aak",
    classification = "Trans-New Guinea, Angan, Nuclear Angan"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

l = Language.objects.create(editor=ed, 
    language = "Baruya",
    slug = "baruya",
    isocode = "byr",
    classification = "Trans-New Guinea, Angan, Nuclear Angan"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

l = Language.objects.create(editor=ed, 
    language = "Tainae",
    slug = "tainae",
    isocode = "ago",
    classification = "Trans-New Guinea, Angan, Nuclear Angan"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

a = AlternateName.objects.create(
    language=l, editor=ed, name="Ivori", slug="ivori"
)
a.save()
#
l = Language.objects.create(editor=ed, 
    language = "Bogaya",
    slug = "bogaya",
    isocode = "boq",
    classification = "Trans-New Guinea, Duna-Bogaya"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

# 
l = Language.objects.create(editor=ed, 
    language = "Dadibi",
    slug = "dadibi",
    isocode = "mps",
    classification = "Trans-New Guinea, Teberan"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))
a = AlternateName.objects.create(
    language=l, editor=ed, name="Daribi", slug="daribi"
)
a.save()

l = Language.objects.create(editor=ed, 
    language = "Tabo",
    slug = "tabo",
    isocode = "knv",
    classification = "South-Central Papuan, Waia"
)
l.save()
l.family.add(Family.objects.get(slug="scpapuan"))
a = AlternateName.objects.create(
    language=l, editor=ed, name="Waia", slug="waia"
)
a.save()


l = Language.objects.create(editor=ed, 
    language = "Duna",
    slug = "duna",
    isocode = "duc",
    classification = "Trans-New Guinea, Duna-Bogaya"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))


l = Language.objects.create(editor=ed, 
    language = "Saniyo-Hiyewe",
    slug = "saniyo-hiyewe",
    isocode = "sny",
    classification = "Sepik, Sepik Hill, Sanio"
)
l.save()
l.family.add(Family.objects.get(slug="scpapuan"))
a = AlternateName.objects.create(
    language=l, editor=ed, name="Saniyo", slug="saniyo"
)
a.save()

l = Language.objects.create(editor=ed, 
    language = "West Kewa",
    slug = "west-kewa",
    isocode = "kew",
    classification = "Trans-New Guinea, Engan, Angal-Kewa"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

l = Language.objects.create(editor=ed, 
    language = "Simbari",
    slug = "simbari",
    isocode = "smb",
    classification = "Trans-New Guinea, Angan, Nuclear Angan"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))


l = Language.objects.create(editor=ed, 
    language = "Hamtai",
    slug = "hamtai",
    isocode = "hmt",
    classification = "Trans-New Guinea, Angan, Nuclear Angan"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))
a = AlternateName.objects.create(
    language=l, editor=ed, name="Kapau", slug="kapau"
)
a.save()


l = Language.objects.create(editor=ed, 
    language = "Kamasa",
    slug = "kamasa",
    isocode = "klp",
    classification = "Trans-New Guinea, Angan, Nuclear Angan"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))


l = Language.objects.create(editor=ed, 
    language = "Akoye",
    slug = "akoye",
    isocode = "miw",
    classification = "Trans-New Guinea, Angan, Nuclear Angan"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))
a = AlternateName.objects.create(
    language=l, editor=ed, name="Lohiki", slug="lohiki"
)
a.save()


l = Language.objects.create(editor=ed, 
    language = "Menya",
    slug = "menya",
    isocode = "mcr",
    classification = "Trans-New Guinea, Angan, Nuclear Angan"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

l = Language.objects.create(editor=ed, 
    language = "Yagwoia",
    slug = "yagwoia",
    isocode = "ygw",
    classification = "Trans-New Guinea, Angan, Nuclear Angan"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

l = Language.objects.create(editor=ed, 
    language = "Kawacha",
    slug = "kawacha",
    isocode = "kcb",
    classification = "Trans-New Guinea, Angan, Nuclear Angan"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

l = Language.objects.create(editor=ed, 
    language = "Minanibai",
    slug = "minanibai",
    isocode = "mcv",
    classification = "Trans-New Guinea, Inland Gulf, Minanibai"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))


l = Language.objects.create(editor=ed, 
    language = "Ipiko",
    slug = "ipiko",
    isocode = "ipo",
    classification = "Trans-New Guinea, Inland Gulf, Ipiko"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

l = Language.objects.create(editor=ed, 
    language = "Kasua",
    slug = "kasua",
    isocode = "khs",
    classification = "Trans-New Guinea, Bosavi"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

l = Language.objects.create(editor=ed, 
    language = "Kaluli",
    slug = "kaluli",
    isocode = "bco",
    classification = "Trans-New Guinea, Bosavi"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

l = Language.objects.create(editor=ed, 
    language = "Onabasulu",
    slug = "onabasulu",
    isocode = "onn",
    classification = "Trans-New Guinea, Bosavi"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

l = Language.objects.create(editor=ed, 
    language = "Pare",
    slug = "pare",
    isocode = "ppt",
    classification = "Trans-New Guinea, Awin-Pare"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))


l = Language.objects.create(editor=ed, 
    language = "Gobasi (Bibo)",
    slug = "gobasi-bibo",
    isocode = "goi",
    classification = "Trans-New Guinea, E. Strickland"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

l = Language.objects.create(editor=ed, 
    language = "Gobasi (Honibo)",
    slug = "gobasi-honibo",
    isocode = "goi",
    classification = "Trans-New Guinea, E. Strickland"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

l = Language.objects.create(editor=ed, 
    language = "Fembe",
    slug = "fembe",
    isocode = "agl",
    classification = "Trans-New Guinea, E. Strickland"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

a = AlternateName.objects.create(
    language=l, editor=ed, name="Agala", slug="agala"
)
a.save()
a = AlternateName.objects.create(
    language=l, editor=ed, name="Sinale", slug="sinale"
)
a.save()

l = Language.objects.create(editor=ed, 
    language = "Kubo",
    slug = "kubo",
    isocode = "jko",
    classification = "Trans-New Guinea, E. Strickland"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))


l = Language.objects.create(editor=ed, 
    language = "Samo",
    slug = "samo",
    isocode = "smq",
    classification = "Trans-New Guinea, E. Strickland"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))


l = Language.objects.create(editor=ed, 
    language = "Bamu (Sisiame)",
    slug = "bamu-sisiame",
    isocode = "bcf",
    classification = "Trans-New Guinea, Kiwaian"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

l = Language.objects.create(editor=ed, 
    language = "Southern Kiwai (Tureture)",
    slug = "tureture",
    isocode = "kjd",
    classification = "Trans-New Guinea, Kiwaian"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))


l = Language.objects.create(editor=ed, 
    language = "Southern Kiwai",
    slug = "southern-kiwai",
    isocode = "kjd",
    classification = "Trans-New Guinea, Kiwaian"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))
a = AlternateName.objects.create(
    language=l, editor=ed, name="Island Kiwai", slug="island-kiwai"
)
a.save()

l = Language.objects.create(editor=ed, 
    language = "Kerewo",
    slug = "kerewo",
    isocode = "kxz",
    classification = "Trans-New Guinea, Kiwaian"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))
a = AlternateName.objects.create(
    language=l, editor=ed, name="Kerewo Kiwai", slug="kerewo-kiwai"
)
a.save()


l = Language.objects.create(editor=ed, 
    language = "Northeast Kiwai (Arigibi)",
    slug = "northeast-kiwai-arigibi",
    isocode = "kiw",
    classification = "Trans-New Guinea, Kiwaian"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

l = Language.objects.create(editor=ed, 
    language = "Northeast Kiwai (Gope)",
    slug = "northeast-kiwai-gope",
    isocode = "kiw",
    classification = "Trans-New Guinea, Kiwaian"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

l = Language.objects.create(editor=ed, 
    language = "Morigi",
    slug = "morigi",
    isocode = "mdb",
    classification = "Trans-New Guinea, Kiwaian"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))
a = AlternateName.objects.create(
    language=l, editor=ed, name="Morigi Kiwai", slug="morigi-kiwai"
)
a.save()

l = Language.objects.create(editor=ed, 
    language = "Northeast Kiwai (Gibaio)",
    slug = "northeast-kiwai-gibaio",
    isocode = "kiw",
    classification = "Trans-New Guinea, Kiwaian"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))


l = Language.objects.create(editor=ed, 
    language = "Bamu",
    slug = "bamu",
    isocode = "bcf",
    classification = "Trans-New Guinea, Kiwaian"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))
a = AlternateName.objects.create(
    language=l, editor=ed, name="Bamu Kiwai", slug="bamu-kiwai"
)
a.save()


l = Language.objects.create(editor=ed, 
    language = "Waboda",
    slug = "waboda",
    isocode = "kmx",
    classification = "Trans-New Guinea, Kiwaian"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))
a = AlternateName.objects.create(
    language=l, editor=ed, name="Wabuda Kiwai", slug="wabuda-kiwai"
)
a.save()


l = Language.objects.create(editor=ed, 
    language = "Kibiri",
    slug = "kibiri",
    isocode = "prm",
    classification = "Trans-New Guinea, Kiwaian"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

a = AlternateName.objects.create(
    language=l, editor=ed, name="Porome", slug="porome"
)
a.save()

l = Language.objects.create(editor=ed, 
    language = "Kaki Ae",
    slug = "kaki-ae",
    isocode = "tbd",
    classification = "Trans-New Guinea, Eleman, Tate"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

a = AlternateName.objects.create(
    language=l, editor=ed, name="Raepa Tati", slug="raepa-tati"
)
a.save()
a = AlternateName.objects.create(
    language=l, editor=ed, name="Tate", slug="tate"
)
a.save()

l = Language.objects.create(editor=ed, 
    language = "Dibiyaso",
    slug = "dibiyaso",
    isocode = "dby",
    classification = "Trans-New Guinea, Bosavi"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))
a = AlternateName.objects.create(
    language=l, editor=ed, name="Bainapi", slug="bainapi"
)
a.save()


l = Language.objects.create(editor=ed, 
    language = "Wiru",
    slug = "wiru",
    isocode = "wiu",
    classification = "Trans-New Guinea, Wiru"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))


l = Language.objects.create(editor=ed, 
    language = "Tairuma",
    slug = "tairuma",
    isocode = "uar",
    classification = "Trans-New Guinea, Eleman, Nuclear Eleman, E."
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))
a = AlternateName.objects.create(
    language=l, editor=ed, name="Uaripi", slug="uaripi"
)
a.save()

l = Language.objects.create(editor=ed, 
    language = "Ikobi-Mena",
    slug = "ikobi-mena",
    isocode = "meb",
    classification = "Trans-New Guinea, Turama-Kikorian, Turama-Omatian"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))
a = AlternateName.objects.create(
    language=l, editor=ed, name="Ikobi-Kairi", slug="ikobi-kairi"
)
a.save()


l = Language.objects.create(editor=ed, 
    language = "Mena",
    slug = "mena",
    isocode = "meb",
    classification = "Trans-New Guinea, Turama-Kikorian, Turama-Omatian"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

l = Language.objects.create(editor=ed, 
    language = "Omati",
    slug = "omati",
    isocode = "mgx",
    classification = "Trans-New Guinea, Turama-Kikorian, Turama-Omatian"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

l = Language.objects.create(editor=ed, 
    language = "Toaripi (Sepoe)",
    slug = "sepoe",
    isocode = "tqo",
    classification = "Trans-New Guinea, Eleman, Nuclear Eleman, E."
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))


l = Language.objects.create(editor=ed, 
    language = "Toaripi",
    slug = "toaripi",
    isocode = "tqo",
    classification = "Trans-New Guinea, Eleman, Nuclear Eleman, E."
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))


l = Language.objects.create(editor=ed, 
    language = "Opao",
    slug = "opao",
    isocode = "opo",
    classification = "Trans-New Guinea, Eleman, Nuclear Eleman, W."
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))


l = Language.objects.create(editor=ed, 
    language = "Orokolo",
    slug = "orokolo",
    isocode = "oro",
    classification = "Trans-New Guinea, Eleman, Nuclear Eleman, W."
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

l = Language.objects.create(editor=ed, 
    language = "Orokolo (Kaipi)",
    slug = "orokolo-kaipi",
    isocode = "oro",
    classification = "Trans-New Guinea, Eleman, Nuclear Eleman, W."
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

l = Language.objects.create(editor=ed, 
    language = "Keoru-Ahia",
    slug = "keoru-ahia",
    isocode = "xeu",
    classification = "Trans-New Guinea, Eleman, Nuclear Eleman, W."
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))
a = AlternateName.objects.create(
    language=l, editor=ed, name="Keuru", slug="keuru"
)
a.save()


l = Language.objects.create(editor=ed, 
    language = "Keoru-Ahia (Aheave)",
    slug = "aheave",
    isocode = "xeu",
    classification = "Trans-New Guinea, Eleman, Nuclear Eleman, W."
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))


l = Language.objects.create(editor=ed, 
    language = "Samberigi",
    slug = "samberigi",
    isocode = "ssx",
    classification = "Trans-New Guinea, Engan, Angal-Kewa"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

a = AlternateName.objects.create(
    language=l, editor=ed, name="Sau", slug="sau"
    )
a.save()

l = Language.objects.create(editor=ed, 
    language = "Folopa (Suri)",
    slug = "folopa-suri",
    isocode = "ppo",
    classification = "Trans-New Guinea, Teberan"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

l = Language.objects.create(editor=ed, 
    language = u"Folopa (Bɔro)",
    slug = "folopa-boro",
    isocode = "ppo",
    classification = "Trans-New Guinea, Teberan"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))


l = Language.objects.create(editor=ed, 
    language = "Folopa (Sopese)",
    slug = "folopa-sopese",
    isocode = "ppo",
    classification = "Trans-New Guinea, Teberan"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))


l = Language.objects.create(editor=ed, 
    language = "Tebera",
    slug = "tebera",
    isocode = "",
    classification = "Trans-New Guinea, Teberan"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))


# already in database
l = Language.objects.get(slug="pawaia")
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

a = AlternateName.objects.create(
    language=l, editor=ed, name="Uraru", slug="uraru"
    )
a.save()

l = Language.objects.create(editor=ed, 
    language = "Fasu",
    slug = "fasu",
    isocode = "faa",
    classification = "Trans-New Guinea, W. Kutubu"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))

l = Language.objects.create(editor=ed, 
    language = "Fasu (Namumi)",
    slug = "namumi",
    isocode = "faa",
    classification = "Trans-New Guinea, W. Kutubu"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))


l = Language.objects.create(editor=ed, 
    language = "Rumu",
    slug = "rumu",
    isocode = "klq",
    classification = "Trans-New Guinea, Turama-Kikorian, Kairi"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))
a = AlternateName.objects.create(
    language=l, editor=ed, name="Kairi", slug="kairi"
    )
a.save()

l = Language.objects.create(editor=ed, 
    language = "Foi",
    slug = "foi",
    isocode = "foi",
    classification = "Trans-New Guinea, East Kutubu"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))
a = AlternateName.objects.create(
    language=l, editor=ed, name="Foe", slug="foe"
    )
a.save()

l = Language.objects.create(editor=ed, 
    language = "Bamu (Pirupiru)",
    slug = "bamu-pirupiru",
    isocode = "bcf",
    classification = "Trans-New Guinea, Kiwaian"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))


l = Language.objects.create(editor=ed, 
    language = "Piame",
    slug = "piame",
    isocode = "pin",
    classification = "Sepik, Sepik Hill, Sanio"
)
l.save()
l.family.add(Family.objects.get(slug="sepik"))
a = AlternateName.objects.create(
    language=l, editor=ed, name="Biami", slug="biami"
    )
a.save()


l = Language.objects.create(editor=ed, 
    language = "Mubami",
    slug = "mubami",
    isocode = "tsx",
    classification = "Trans-New Guinea, Inland Gulf, Minanibai"
)
l.save()
l.family.add(Family.objects.get(slug="transnewguinea"))
a = AlternateName.objects.create(
    language=l, editor=ed, name="Tao-Suamato", slug="tao-suamato"
    )
a.save()


