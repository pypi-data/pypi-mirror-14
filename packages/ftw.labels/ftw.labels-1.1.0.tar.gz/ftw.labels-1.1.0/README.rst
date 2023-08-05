ftw.labels
==========

A Plone addon for labels.

Containers, Folders for example, can be marked as label container.
For each label container a set of labels with colors can be defined.
Items whithin this container which support labelling can then be labelled
with one or more labels.


Screenshots
-----------

Managing labels on the label container (``ILabelJar``):

.. image:: https://raw.github.com/4teamwork/ftw.labels/master/docs/label_jar.png


Set label for a content (``ILabelSupport``):

.. image:: https://raw.github.com/4teamwork/ftw.labels/master/docs/label_support.png



Installation
------------

- Add ``ftw.labels`` to your buildout configuration:

.. code:: rst

    [instance]
    eggs +=
        ftw.labels

- Install the generic setup profile of ``ftw.labels``.


Usage / Integration
-------------------

Add the ``ILabelJar`` marker interface to any container class you want:

.. code:: xml

    <class class="Products.ATContentTypes.content.folder.ATFolder">
        <implements interface="ftw.labels.interfaces.ILabelRoot" />
    </class>

For objects providing ``ILabelJar`` a left-column-portlet is added
on the root of the Plone site which allows to manage labels.


Add the ``ILabelSupport`` marker interface to any item you want to be able to
set labels on:

.. code:: xml

    <class class="plone.app.blob.content.ATBlob">
        <implements interface="ftw.labels.interfaces.ILabelSupport" />
    </class>

For objects providing ``ILabelSupport`` a right-column-portlet is added
on the root of the Plone site which allows to manage labels.


Add the ``ILabelJarChild`` marker interface to any container class to
display the labels stored in a parents ``ILabelJar``

.. code:: xml

    <class class="Products.ATContentTypes.content.folder.ATFolder">
        <implements interface="ftw.labels.interfaces.ILabelJarChild" />
    </class>

For objects providing ``ILabelJarChild`` you can manage and store the
same labels as defined in the ``ILabelJar`` content without defining
a new ``ILabelRoot``


Uninstall
---------

The package provides an uninstall mechanism.
Use Plone's addon control panel or portal_quickInstaller to uninstall
the package.



Links
-----

- Github: https://github.com/4teamwork/ftw.labels
- Issues: https://github.com/4teamwork/ftw.labels/issues
- Pypi: http://pypi.python.org/pypi/ftw.labels
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.labels


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.labels`` is licensed under GNU General Public License, version 2.
