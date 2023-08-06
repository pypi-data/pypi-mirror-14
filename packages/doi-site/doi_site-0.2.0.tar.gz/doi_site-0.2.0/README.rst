Delegation of the Minting of Datacite DOIs within an Organisation
=================================================================

Introduction
------------
This code provides a shim layer in front of the Datacite API in order to apply
local security settings and limit the sub-domain for which a user can mint
DOIs. It is designed to hook into an organisation's LDAP server in order to
authenticate users.

The Issue Addressed by this Software
------------------------------------
We do not have a single central repository for our data and a number of groups
are wishing to mint DOIs for their data. DataCite only provides one username
and password and there is no way to limit the sub-domain (name space) within
the organisation's allocated domain, in which users mint DOIs. We wish to
divide up the organisation's domain in a controlled manner and allow named
individuals to manage the minting of DOIs within confines of a given
sub-domain.

The Solution
------------
Named individuals will have responsibility for a given sub-domain. The 
individuals will have to agree to abide by the DataCite terms and conditions.
This software provides the ability to define sub-domains and an authorisation
mechanism to control minting within those sub-domains.

In effect it provides a MDS service to control access to the DataCite MDS.
Calls via the API are validated before the organisation's credentials are used
to passed on the call to DataCite.

The aim is to provide a thin a layer as possible and simply pass on authorised
calls. Authentication is done via the organisation's LDAP server and
authorisation via local database which maps LDAP ids to sub-domains. The MDS
ReST API is provided and users are referred to the DataCite API documentation. 

The software makes use of the django framework.

In addition to the API some basic web pages are provided.

Future Work
-----------
It is intended to extend the web site to allow users to mint DOIs for their
sub-domains via a web form.

Following on from this it is intended to link this system with a central
repository. This system would be extended to generate landing pages for data in
the central repository. The system could then be opened up to anyone in the
organisation to store data sets and mint DOIs under a central sub-domain.

Installation and Configuration
==============================

Prerequisites
-------------

- Python => 2.7
- python-virtualenv
- gcc
- mod_ssl.x86_64
- mod_wsgi.x86_64
- openldap-devel
- Apache

Installation
------------

Create the directory for the static files

.. code:: bash

    mkdir -p /var/www/html/doi

Create the directory for the sqlite database

.. code:: bash

    mkdir -p /var/doi

Create the python virtual environment

.. code:: bash

    cd /opt
    virtualenv doi
    cd doi
    source bin/activate
    export DJANGO_PROJECT_STATIC_FILES=/var/www/html/doi/


Local customisation for proxy, if required

.. code:: bash

    export http_proxy=http://example.org:8080
    export https_proxy=http://example.org:8080
    
Install the software

.. code:: bash

    pip install doi_site

Configuration
-------------

local_settings.py
^^^^^^^^^^^^^^^^^
Create a copy of the ``local_settings.py.ini`` file as ``local_settings.py``
Review the contents of this file and update the parameters. You MUST provide
values for:

- ``DOI_PREFIX`` - The organisation's DataCite prefix in the form nn.nnnn
- ``DATACITE_USER_NAME`` - The organisation's username for DataCite
- ``DATACITE_PASSWORD`` - The organisation's password for DataCite
- ``AUTH_LDAP_SERVER_URI`` - The URI of the organisation's LDAP server
- ``AUTH_LDAP_USER_DN_TEMPLATE`` - The organisation's LDAP DN template
- ``ORGANISATION_NAME`` - The name of your organisation, this will be displayed on the home page
- ``ORGANISATION_DOI_EMAIL`` - An email address for people to contact you about the this service, this will be displayed on the home page
- ``SECRET_KEY`` - A secret key for a particular Django installation. This is used to provide cryptographic signing, and should be set to a unique, unpredictable value.
- ``ALLOWED_HOSTS`` - A list of strings representing the host/domain names that this Django site can serve. This should include your server's hostname.

You should provide values for:

- ``ROLES_URL`` - The URL of the location of the document detailing users roles and responsibilities
- ``NOTES_URL`` - The URL of the location of the document containing notes for issuers

Additionally if necessary provide values for:

- ``HTTP_PROXY_HOST`` - Web proxy host
- ``HTTP_PROXY_PORT`` - Web proxy port

By default the DataCite ``TEST`` MDS is used. To use the ``PRODUCTION`` MDS
uncomment:

- ``DATACITE_URL``
- ``DATACITE_HANDLER``

In a testing environment you can set ``DEBUG = True``

Initialisation and Admin User Creation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

    python lib/python2.7/site-packages/doi_site/manage.py collectstatic --clear --noinput
    python lib/python2.7/site-packages/doi_site/manage.py syncdb --noinput
    python lib/python2.7/site-packages/doi_site/manage.py createsuperuser
    deactivate

Stuff for apache
^^^^^^^^^^^^^^^^

.. code:: bash

    cp -p  /opt/doi/lib/python2.7/site-packages/doi_site/resources/doi_wsgi.conf /etc/httpd/conf.d/

Assuming apache is running as the user ``apache``

.. code:: bash

    chown -R apache /opt/doi
    chown -R apache /var/doi
    
    systemctl start httpd
    

Customisation of the Web Pages
==============================

This code makes use of inheritance within the templates. It has been structured
to make it relatively easy to customise the look and feel of the site.
Everything inherits from base.html.

base.html -> organisation_wrapper.html -> everything else

To customise the appearance of the site provide your own
``organisation_skin.html``, which should inherit from ``base.html``.

Change ``organisation_wrapper.html`` to inherit from your ``organisation_skin.html``

base.html -> organisation_wrapper.html -> organisation_wrapper.html -> everything else

Within your ``organisation_skin.html`` you can override the following blocks:

- head
- page_header
- navbar
- content
- footer

Place any css files in the directory ``static/doi_site/css/``

If you have made any changes you will have to restart apache

Adding DOI Domains via the Admin Web Page
=========================================

The software makes use of the ``Groups`` model provided by the django
framework. ``Group`` has been extended to include sub-domain information. There
is a one to one mapping between group and sub-domain.

In a browser go to the admin pages, i.e. ``https://example.org/admin/``

In order to log in you will need you the credentials that you used to create
the superuser

Click on ``+Add`` besides the ``Groups`` label

Give a name to the group and a DOI suffix

Save your changes


Granting Minting Privileges to Users
====================================

Get the user to log in with their LDAP username and password, this will create
a local account (the password is not stored in the django database).

In a browser go to the admin pages, i.e. ``https://example.org/admin/``

You will need you credentials that you used to create the superuser to log on

Click on ``Users``

Click on the user name you wish to edit

Fill in their personal information, first name, last name, email address (yes
we should really pull this in from LDAP)

Within the ``Groups`` in the ``Permissions`` section, assign the user to the
required groups

Save the changes

The user will then be able to mint DOIs for that groups DOI prefix
