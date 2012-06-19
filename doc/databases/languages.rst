Database: languages
===================

``languages`` is the main table for data about each language.

Structure
---------

Family
^^^^^^

.. _Table.Language.Family:

Stores information about language families.

* name: Family name
* slug: `slug` of Family name


Language
^^^^^^^^

.. _Table.Language.Language:

Stores language information.

* name: Language name
* slug: `slug` of Language name
* isocode: Tree character ISO code for this language
* classification: Classification string.
* family: Foreign Key -> :ref:`Family <Table.Language.Family>`.
    

AlternateNames
^^^^^^^^^^^^^^

.. _Table.Language.AlternateNames:

Handles languages with multiple names

* name: Language name
* slug: `slug` of Language name
* language: Foreign Key -> :ref:`Language <Table.Language.Language>`.
    
Links
^^^^^

.. _Table.Language.Links:

Stores links to language appropriate resources

* link: URL of link
* description: Short text description of link
* language: Foreign Key -> :ref:`Language <Table.Language.Language>`.

Locations
^^^^^^^^^

.. _Table.Language.Locations:

* longitude: FloatField containing longitude
* latitude: FloatField containing latitude
* language: Foreign Key -> :ref:`Language <Table.Language.Language>`.

