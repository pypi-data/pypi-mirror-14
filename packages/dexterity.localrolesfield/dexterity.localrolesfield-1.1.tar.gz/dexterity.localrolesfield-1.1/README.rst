.. contents::

Introduction
============

This package permits to give a local role on a content following a content field value and the workflow state.
It uses borg.localrole.

A new configuration page is added as a new tab on each dexterity type configuration.

You can there define for each local role field and each state which local roles will be automatically given to the selected principal in the field.

You will find in each configuration line an additional field names suffix.
If completed, the suffix name will be added at the end of the local role field value to define a principal name.

By example: if the configuration suffix is "director" and the local role field value is "group1", the local role will be given to "group1_director".

This last functionality is used with the package collective.contact.plonegroup. 

Technically, this package extends dexterity.localroles:

* provides a principal selector field
* extends the configuration page

This is a refactoring of collective.z3cform.rolefield.

Installation
============

* Add dexterity.localrolesfield to your eggs.
* Re-run buildout.
* Done.

Credits
=======

Have an idea? Found a bug? Let us know by `opening a ticket`_.

.. _`opening a ticket`: https://github.com/collective/dexterity.localrolesfield/issues


Tests
=====

This package is tested using Travis CI. The current status of the add-on is :

.. image:: https://api.travis-ci.org/collective/dexterity.localrolesfield.png
    :target: https://travis-ci.org/collective/dexterity.localrolesfield
.. image:: https://coveralls.io/repos/collective/dexterity.localrolesfield/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/collective/dexterity.localrolesfield?branch=master
