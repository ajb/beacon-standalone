Beacon
======

Beacon is a tool for City Purchasers to advertise new opportunities and businesses to sign up to receive information about those front. It is divided into two sections: a public-facing section and an administrative section. The public-facing section contains a list and detail view of both currently available and past opportunities, along with overview informational pages, signup pages, and a page to manage email subscriptions.

The administrative section handles the creation and editing of new opportunities along with an approval flow for front.

Additionally, Beacon has two nightly jobs that run: one nightly job sends emails whenever new opportunities become "published" (see the :py:class:`~purchasing.models.front.Opportunity` model for more information), and a job that runs and sends a bi-weekly update with a list of all non-expired opportunities that have been posted in the past two weeks to all signed-up Vendors. See more in the :ref:`beacon-nightly` section.

.. seealso::

    `How to use Beacon <https://docs.google.com/document/d/1z2ujIVJ0pa0lN9rO_1W3MrLTUe_smpwrWyXpWZEVp4Q/export?format=pdf>`_, an internal product guide for more information about the user interface and user experience.

Models Used
-----------

* :py:class:`purchasing.models.front.Opportunity`
* :py:class:`purchasing.models.front.OpportunityDocument`
* :py:class:`purchasing.models.front.RequiredBidDocument`
* :py:class:`purchasing.models.front.Vendor`
* :py:class:`purchasing.models.front.Category`

Forms
-----

Forms
^^^^^

.. automodule:: purchasing.forms.opportunities
    :members:

Validators
^^^^^^^^^^

.. automodule:: purchasing.beacon.forms.validators
    :members:

Helper functions
----------------

.. automodule:: purchasing.beacon.blueprints.opportunity_view_util
    :members:

Views
-----

Public-facing
^^^^^^^^^^^^^

.. autoflask:: purchasing.app:create_app()
    :blueprints: opportunities
    :undoc-endpoints: front.static

Administration
^^^^^^^^^^^^^^

.. autoflask:: purchasing.app:create_app()
    :blueprints: opportunities_admin
    :undoc-endpoints: beacon_admin.static

.. _beacon-nightly:

Nightly Jobs
------------

.. automodule:: purchasing.jobs.beacon_nightly
    :members:
