chembl_migration_model
======


.. image:: https://img.shields.io/pypi/v/chembl_migration_model.svg
    :target: https://pypi.python.org/pypi/chembl_migration_model/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/dm/chembl_migration_model.svg
    :target: https://pypi.python.org/pypi/chembl_migration_model/
    :alt: Downloads

.. image:: https://img.shields.io/pypi/pyversions/chembl_migration_model.svg
    :target: https://pypi.python.org/pypi/chembl_migration_model/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/status/chembl_migration_model.svg
    :target: https://pypi.python.org/pypi/chembl_migration_model/
    :alt: Development Status

.. image:: https://img.shields.io/pypi/l/chembl_migration_model.svg
    :target: https://pypi.python.org/pypi/chembl_migration_model/
    :alt: License

.. image:: https://badge.waffle.io/chembl/chembl_migration_model.png?label=ready&title=Ready 
 :target: https://waffle.io/chembl/chembl_migration_model
 :alt: 'Stories in Ready'

This is chembl_migration_model package developed at Chembl group, EMBL-EBI, Cambridge, UK.

This package contains Django ORM model suitable for data exports and migrations.
It excludes some tables present in chembl_core_model (such as COMPOUND_MOLS and COMPOUND_IMAGES) as well as some columns in remaining tables.

The model is generated dynamically from chembl_core_model and this is why models.py file is empty.
Whole logic sits in __init__.py.
All classes are unmanaged by default so you can't use them to syncdb.
To create tables from the model you have to run migrate command from chembl_migrate.
