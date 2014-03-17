#!/usr/bin/env python
from django.contrib.auth.models import User

# import models
from website.apps.core.models import Family, Language, AlternateName

# get editor
ed = User.objects.get(pk=1)
TNG = Family.objects.get(slug="transnewguinea")


LObj = Language.objects.create(
                        language="Kare", 
                        slug="kare",
                        dialect=None, 
                        isocode="kmf", 
                        classification="Trans-New Guinea, Madang, Croisilles, Kare",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Girawa", 
                        slug="girawa",
                        dialect=None, 
                        isocode="bbr", 
                        classification="Trans-New Guinea, Madang, Croisilles, Kokon",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Munit", 
                        slug="munit",
                        dialect=None, 
                        isocode="mtc", 
                        classification="Trans-New Guinea, Madang, Croisilles, Kokon",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Kein", 
                        slug="kein",
                        dialect=None, 
                        isocode="bmh", 
                        classification="Trans-New Guinea, Madang, Croisilles, Kokon",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

a = AlternateName.objects.create(
    language=LObj, 
    editor=ed,
    name="Bemal", 
    slug="bemal"
)

LObj = Language.objects.create(
                        language="Sihan", 
                        slug="sihan",
                        dialect=None, 
                        isocode="snr", 
                        classification="Trans-New Guinea, Madang, Croisilles, Gum",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Gumalu", 
                        slug="gumalu",
                        dialect=None, 
                        isocode="gmu", 
                        classification="Trans-New Guinea, Madang, Croisilles, Gum",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Isebe", 
                        slug="isebe",
                        dialect=None, 
                        isocode="igo", 
                        classification="Trans-New Guinea, Madang, Croisilles, Gum",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Amele", 
                        slug="amele",
                        dialect=None, 
                        isocode="aey", 
                        classification="Trans-New Guinea, Madang, Croisilles, Gum",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Bau", 
                        slug="bau",
                        dialect=None, 
                        isocode="bbd", 
                        classification="Trans-New Guinea, Madang, Croisilles, Gum",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Panim", 
                        slug="panim",
                        dialect=None, 
                        isocode="pnr", 
                        classification="Trans-New Guinea, Madang, Croisilles, Gum",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Rapting", 
                        slug="rapting",
                        dialect=None, 
                        isocode="rpt", 
                        classification="Trans-New Guinea, Madang, Croisilles, Hanseman",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Wamas", 
                        slug="wamas",
                        dialect=None, 
                        isocode="wmc", 
                        classification="Trans-New Guinea, Madang, Croisilles, Hanseman",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Samosa", 
                        slug="samosa",
                        dialect=None, 
                        isocode="swm", 
                        classification="Trans-New Guinea, Madang, Croisilles, Hanseman",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Murupi", 
                        slug="murupi",
                        dialect=None, 
                        isocode="mqw", 
                        classification="Trans-New Guinea, Madang, Croisilles, Hanseman",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Saruga", 
                        slug="saruga",
                        dialect=None, 
                        isocode="sra", 
                        classification="Trans-New Guinea, Madang, Croisilles, Hanseman",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Nake", 
                        slug="nake",
                        dialect=None, 
                        isocode="nbk", 
                        classification="Trans-New Guinea, Madang, Croisilles, Hanseman",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Mosimo", 
                        slug="mosimo",
                        dialect=None, 
                        isocode="mqv", 
                        classification="Trans-New Guinea, Madang, Croisilles, Hanseman",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Garus", 
                        slug="garus",
                        dialect=None, 
                        isocode="gyb", 
                        classification="Trans-New Guinea, Madang, Croisilles, Hanseman",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Yoidik", 
                        slug="yoidik",
                        dialect=None, 
                        isocode="ydk", 
                        classification="Trans-New Guinea, Madang, Croisilles, Hanseman",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Rempi", 
                        slug="rempi",
                        dialect=None, 
                        isocode="rmp", 
                        classification="Trans-New Guinea, Madang, Croisilles, Hanseman",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Bagupi", 
                        slug="bagupi",
                        dialect=None, 
                        isocode="bpi", 
                        classification="Trans-New Guinea, Madang, Croisilles, Hanseman",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Silopi", 
                        slug="silopi",
                        dialect=None, 
                        isocode="xsp", 
                        classification="Trans-New Guinea, Madang, Croisilles, Hanseman",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Utu", 
                        slug="utu",
                        dialect=None, 
                        isocode="utu", 
                        classification="Trans-New Guinea, Madang, Croisilles, Hanseman",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Mawan", 
                        slug="mawan",
                        dialect=None, 
                        isocode="mcz", 
                        classification="Trans-New Guinea, Madang, Croisilles, Hanseman",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Baimak", 
                        slug="baimak",
                        dialect=None, 
                        isocode="bmx", 
                        classification="Trans-New Guinea, Madang, Croisilles, Hanseman",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Matepi", 
                        slug="matepi",
                        dialect=None, 
                        isocode="mqe", 
                        classification="Trans-New Guinea, Madang, Croisilles, Hanseman",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Gal", 
                        slug="gal",
                        dialect=None, 
                        isocode="gap", 
                        classification="Trans-New Guinea, Madang, Croisilles, Hanseman",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Nobonob", 
                        slug="nobonob",
                        dialect=None, 
                        isocode="gaw", 
                        classification="Trans-New Guinea, Madang, Croisilles, Hanseman",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)
a = AlternateName.objects.create(
    language=LObj, 
    editor=ed,
    name="Garuh", 
    slug="garuh"
)

LObj = Language.objects.create(
                        language="Wagi", 
                        slug="wagi",
                        dialect=None, 
                        isocode="fad", 
                        classification="Trans-New Guinea, Madang, Croisilles, Hanseman",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)
a = AlternateName.objects.create(
    language=LObj, 
    editor=ed,
    name="Kamba", 
    slug="kamba"
)

LObj = Language.objects.create(
                        language="Bargam", 
                        slug="bargam",
                        dialect=None, 
                        isocode="mlp", 
                        classification="Trans-New Guinea, Madang, Croisilles, Mugil",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

a = AlternateName.objects.create(
    language=LObj, 
    editor=ed,
    name="Mugil", 
    slug="mugil"
)

LObj = Language.objects.create(
                        language="Gavak", 
                        slug="gavak",
                        dialect=None, 
                        isocode="dmc", 
                        classification="Trans-New Guinea, Madang, Croisilles, Isumrud",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)
a = AlternateName.objects.create(
    language=LObj, 
    editor=ed,
    name="Dimir", 
    slug="dimir"
)

LObj = Language.objects.create(
                        language="Malas", 
                        slug="malas",
                        dialect=None, 
                        isocode="mkr", 
                        classification="Trans-New Guinea, Madang, Croisilles, Isumrud",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Brem", 
                        slug="brem",
                        dialect=None, 
                        isocode="buq", 
                        classification="Trans-New Guinea, Madang, Croisilles, Isumrud",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)
a = AlternateName.objects.create(
    language=LObj, 
    editor=ed,
    name="Bunabun", 
    slug="bunabun"
)

LObj = Language.objects.create(
                        language="Korak", 
                        slug="korak",
                        dialect=None, 
                        isocode="koz", 
                        classification="Trans-New Guinea, Madang, South Adelbert Range, Kowan",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Waskia", 
                        slug="waskia",
                        dialect=None, 
                        isocode="wsk", 
                        classification="Trans-New Guinea, Madang, South Adelbert Range, Kowan",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Mala", 
                        slug="mala",
                        dialect=None, 
                        isocode="ped", 
                        classification="Trans-New Guinea, Madang, Croisilles, Pihom, Kaukombaran",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)
a = AlternateName.objects.create(
    language=LObj, 
    editor=ed,
    name="Pay", 
    slug="pay"
)


LObj = Language.objects.create(
                        language="Maia", 
                        slug="maia-pila",
                        dialect="Pila", 
                        isocode="sks", 
                        classification="Trans-New Guinea, Madang, Croisilles, Pihom, Kaukombaran",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Maia", 
                        slug="maia-saki",
                        dialect="Saki", 
                        isocode="sks", 
                        classification="Trans-New Guinea, Madang, Croisilles, Pihom, Kaukombaran",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Miani", 
                        slug="miani",
                        dialect=None, 
                        isocode="pla", 
                        classification="Trans-New Guinea, Madang, Croisilles, Pihom, Kaukombaran",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)
a = AlternateName.objects.create(
    language=LObj, 
    editor=ed,
    name="Tani", 
    slug="tani"
)



LObj = Language.objects.create(
                        language="Mauwake", 
                        slug="mauwake",
                        dialect=None, 
                        isocode="mhl", 
                        classification="Trans-New Guinea, Madang, Croisilles, Pihom, Kumilan",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Bepour", 
                        slug="bepour",
                        dialect=None, 
                        isocode="bie", 
                        classification="Trans-New Guinea, Madang, Croisilles, Pihom, Kumilan",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Moere", 
                        slug="moere",
                        dialect=None, 
                        isocode="mvq", 
                        classification="Trans-New Guinea, Madang, Croisilles, Pihom, Kumilan",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Mawak", 
                        slug="mawak",
                        dialect=None, 
                        isocode="mjj", 
                        classification="Trans-New Guinea, Madang, Croisilles, Pihom, Tiboran",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Musar", 
                        slug="musar",
                        dialect=None, 
                        isocode="mmi", 
                        classification="Trans-New Guinea, Madang, Croisilles, Pihom, Tiboran",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Wanambre", 
                        slug="wanambre",
                        dialect=None, 
                        isocode="wnb", 
                        classification="Trans-New Guinea, Madang, Croisilles, Pihom, Tiboran",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Yaben", 
                        slug="yaben",
                        dialect=None, 
                        isocode="ybm", 
                        classification="Trans-New Guinea, Madang, Croisilles, Pihom, Numugenan",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Yarawata", 
                        slug="yarawata",
                        dialect=None, 
                        isocode="yrw", 
                        classification="Trans-New Guinea, Madang, Croisilles, Pihom, Numugenan",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Bilakura", 
                        slug="bilakura",
                        dialect=None, 
                        isocode="bql", 
                        classification="Trans-New Guinea, Madang, Croisilles, Pihom, Numugenan",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Parawen", 
                        slug="parawen",
                        dialect=None, 
                        isocode="prw", 
                        classification="Trans-New Guinea, Madang, Croisilles, Pihom, Numugenan",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Ukuriguma", 
                        slug="ukuriguma",
                        dialect=None, 
                        isocode="ukg", 
                        classification="Trans-New Guinea, Madang, Croisilles, Pihom, Numugenan",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Amaimon", 
                        slug="amaimon",
                        dialect=None, 
                        isocode="ali", 
                        classification="Trans-New Guinea, Madang, Croisilles, Pihom, Amaimon",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Kowaki", 
                        slug="kowaki",
                        dialect=None, 
                        isocode="xow", 
                        classification="Trans-New Guinea, Madang, Croisilles, Pihom, Tiboran",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Pamosu", 
                        slug="pamosu",
                        dialect=None, 
                        isocode="hih", 
                        classification="Trans-New Guinea, Madang, Croisilles, Pihom, Tiboran",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Kobol", 
                        slug="kobol",
                        dialect=None, 
                        isocode="kgu", 
                        classification="Trans-New Guinea, Madang, Croisilles, Pihom, Omosan",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Pal", 
                        slug="pal",
                        dialect=None, 
                        isocode="abw", 
                        classification="Trans-New Guinea, Madang, Croisilles, Pihom, Omosan",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Usan", 
                        slug="usan",
                        dialect=None, 
                        isocode="wnu", 
                        classification="Trans-New Guinea, Madang, Croisilles, Pihom, Numugenan",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Sileibi", 
                        slug="sileibi",
                        dialect=None, 
                        isocode="sbq", 
                        classification="Trans-New Guinea, Madang, South Adelbert Range, Josephstaal, Sikan",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Utarmbung", 
                        slug="utarmbung",
                        dialect=None, 
                        isocode="omo", 
                        classification="Trans-New Guinea, Madang, South Adelbert Range, Josephstaal, Osum",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Moresada", 
                        slug="moresada",
                        dialect=None, 
                        isocode="msx", 
                        classification="Trans-New Guinea, Madang, South Adelbert Range, Josephstaal, Pomoikan",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Wadaginam", 
                        slug="wadaginam",
                        dialect=None, 
                        isocode="wdg", 
                        classification="Trans-New Guinea, Madang, South Adelbert Range, Josephstaal, Wadaginam",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Atemble", 
                        slug="atemble",
                        dialect=None, 
                        isocode="ate", 
                        classification="Trans-New Guinea, Madang, South Adelbert Range, Wanang, Atan",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Musak", 
                        slug="musak",
                        dialect=None, 
                        isocode="mmq", 
                        classification="Trans-New Guinea, Madang, South Adelbert Range, Wanang, Emuan",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Paynamar", 
                        slug="paynamar",
                        dialect=None, 
                        isocode="pmr", 
                        classification="Trans-New Guinea, Madang, South Adelbert Range, Wanang, Paynamar",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Biyom", 
                        slug="biyom",
                        dialect=None, 
                        isocode="bpm", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Biyom-Tauya",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Tauya", 
                        slug="tauya",
                        dialect=None, 
                        isocode="tya", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Biyom-Tauya",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Faita", 
                        slug="faita",
                        dialect=None, 
                        isocode="faj", 
                        classification="Trans-New Guinea, Madang, South Adelbert Range, Josephstaal, Faita",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Mum", 
                        slug="mum",
                        dialect=None, 
                        isocode="kqa", 
                        classification="Trans-New Guinea, Madang, South Adelbert Range, Josephstaal, Sikan",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Anam", 
                        slug="anam",
                        dialect=None, 
                        isocode="pda", 
                        classification="Trans-New Guinea, Madang, South Adelbert Range, Josephstaal, Pomoikan",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Anamgura", 
                        slug="anamgura",
                        dialect=None, 
                        isocode="imi", 
                        classification="Trans-New Guinea, Madang, South Adelbert Range, Josephstaal, Pomoikan",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Nend", 
                        slug="nend",
                        dialect=None, 
                        isocode="anh", 
                        classification="Trans-New Guinea, Madang, South Adelbert Range, Wanang, Atan",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Apali", 
                        slug="apali",
                        dialect=None, 
                        isocode="ena", 
                        classification="Trans-New Guinea, Madang, South Adelbert Range, Wanang, Emuan",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Isabi", 
                        slug="isabi",
                        dialect=None, 
                        isocode="isa", 
                        classification="Trans-New Guinea, Kainantu-Goroka, Gorokan, Isabi",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Sinsauru", 
                        slug="sinsauru",
                        dialect=None, 
                        isocode="snz", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Evapia",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Asas", 
                        slug="asas",
                        dialect=None, 
                        isocode="asd", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Evapia",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Sausi", 
                        slug="sausi",
                        dialect=None, 
                        isocode="ssj", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Evapia",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Kesawai", 
                        slug="kesawai",
                        dialect=None, 
                        isocode="xes", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Evapia",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Arawum", 
                        slug="arawum",
                        dialect=None, 
                        isocode="awm", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Kabenau",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Siroi", 
                        slug="siroi",
                        dialect=None, 
                        isocode="ssd", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Kabenau",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Watiwa", 
                        slug="watiwa",
                        dialect=None, 
                        isocode="wtf", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Evapia",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Lemio", 
                        slug="lemio",
                        dialect=None, 
                        isocode="lei", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Kabenau",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Pulabu", 
                        slug="pulabu",
                        dialect=None, 
                        isocode="pup", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Kabenau",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Yabong", 
                        slug="yabong",
                        dialect=None, 
                        isocode="ybo", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Yaganon",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Ganglau", 
                        slug="ganglau",
                        dialect=None, 
                        isocode="ggl", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Yaganon",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Saep", 
                        slug="saep",
                        dialect=None, 
                        isocode="spd", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Yaganon",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Sumau", 
                        slug="sumau",
                        dialect=None, 
                        isocode="six", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Peka",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Sop", 
                        slug="sop",
                        dialect=None, 
                        isocode="urw", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Peka",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Danaru", 
                        slug="danaru",
                        dialect=None, 
                        isocode="dnr", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Peka",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Urigina", 
                        slug="urigina",
                        dialect=None, 
                        isocode="urg", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Peka",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Uya", 
                        slug="uya",
                        dialect=None, 
                        isocode="usu", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Nuru",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Rerau", 
                        slug="rerau",
                        dialect=None, 
                        isocode="rea", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Nuru",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Jilim", 
                        slug="jilim",
                        dialect=None, 
                        isocode="jil", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Nuru",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Yangulam", 
                        slug="yangulam",
                        dialect=None, 
                        isocode="ynl", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Nuru",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Male", 
                        slug="male",
                        dialect=None, 
                        isocode="mdc", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Mindjim",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Bongu", 
                        slug="bongu",
                        dialect=None, 
                        isocode="bpu", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Mindjim",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Ogea", 
                        slug="ogea",
                        dialect=None, 
                        isocode="eri", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Nuru",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Waube", 
                        slug="waube",
                        dialect=None, 
                        isocode="kop", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Nuru",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Anjam", 
                        slug="anjam",
                        dialect=None, 
                        isocode="boj", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Mindjim",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Sam", 
                        slug="sam",
                        dialect=None, 
                        isocode="snx", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Mindjim",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Migum", 
                        slug="migum",
                        dialect=None, 
                        isocode="klm", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Kabenau",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)

LObj = Language.objects.create(
                        language="Uyajitaya", 
                        slug="uyajitaya",
                        dialect=None, 
                        isocode="duk", 
                        classification="Trans-New Guinea, Madang, Rai Coast, Nuru",
                        information="",
                        editor=ed
)
LObj.family.add(TNG)
print(LObj)















a = AlternateName.objects.create(
    language=Language.objects.get(slug="mauwake"), 
    editor=ed,
    name="Ulingan", 
    slug="ulingan"
)


a = AlternateName.objects.create(
    language=Language.objects.get(slug="pamosu"), 
    editor=ed,
    name="Hinihon", 
    slug="hinihon"
)


a = AlternateName.objects.create(
    language=Language.objects.get(slug="kobol"), 
    editor=ed,
    name="Koguman", 
    slug="koguman"
)


a = AlternateName.objects.create(
    language=Language.objects.get(slug="pal"), 
    editor=ed,
    name="Abasakur", 
    slug="abasakur"
)


a = AlternateName.objects.create(
    language=Language.objects.get(slug="usan"), 
    editor=ed,
    name="Wanuma", 
    slug="wanuma"
)


a = AlternateName.objects.create(
    language=Language.objects.get(slug="utarmbung"), 
    editor=ed,
    name="Osum", 
    slug="osum"
)


a = AlternateName.objects.create(
    language=Language.objects.get(slug="atemble"), 
    editor=ed,
    name="Atemple", 
    slug="atemple"
)


a = AlternateName.objects.create(
    language=Language.objects.get(slug="mum"), 
    editor=ed,
    name="Katiati", 
    slug="katiati"
)


a = AlternateName.objects.create(
    language=Language.objects.get(slug="anam"), 
    editor=ed,
    name="Pondoma", 
    slug="pondoma"
)


a = AlternateName.objects.create(
    language=Language.objects.get(slug="anamgura"), 
    editor=ed,
    name="Ikundun", 
    slug="ikundun"
)


a = AlternateName.objects.create(
    language=Language.objects.get(slug="nend"), 
    editor=ed,
    name="Angaua", 
    slug="angaua"
)


a = AlternateName.objects.create(
    language=Language.objects.get(slug="apali"), 
    editor=ed,
    name="Emerum", 
    slug="emerum"
)


a = AlternateName.objects.create(
    language=Language.objects.get(slug="siroi"), 
    editor=ed,
    name="Suroi", 
    slug="suroi"
)


a = AlternateName.objects.create(
    language=Language.objects.get(slug="watiwa"), 
    editor=ed,
    name="Dumpu", 
    slug="dumpu"
)


a = AlternateName.objects.create(
    language=Language.objects.get(slug="sop"), 
    editor=ed,
    name="Usino", 
    slug="usino"
)


a = AlternateName.objects.create(
    language=Language.objects.get(slug="uya"), 
    editor=ed,
    name="Usu", 
    slug="usu"
)


a = AlternateName.objects.create(
    language=Language.objects.get(slug="ogea"), 
    editor=ed,
    name="Erima", 
    slug="erima"
)


a = AlternateName.objects.create(
    language=Language.objects.get(slug="waube"), 
    editor=ed,
    name="Kwato", 
    slug="kwato"
)


a = AlternateName.objects.create(
    language=Language.objects.get(slug="anjam"), 
    editor=ed,
    name="Bom", 
    slug="bom"
)


a = AlternateName.objects.create(
    language=Language.objects.get(slug="sam"), 
    editor=ed,
    name="Songum", 
    slug="songum"
)


a = AlternateName.objects.create(
    language=Language.objects.get(slug="migum"), 
    editor=ed,
    name="Kolom", 
    slug="kolom"
)


a = AlternateName.objects.create(
    language=Language.objects.get(slug="uyajitaya"), 
    editor=ed,
    name="Deduela", 
    slug="deduela"
)


a = AlternateName.objects.create(
    language=Language.objects.get(slug="uyajitaya"), 
    editor=ed,
    name="Duduela", 
    slug="duduela"
)





