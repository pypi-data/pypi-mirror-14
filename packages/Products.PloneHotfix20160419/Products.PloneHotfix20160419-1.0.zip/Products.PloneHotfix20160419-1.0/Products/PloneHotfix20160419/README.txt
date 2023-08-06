Plone hotfix, 2016-04-19
========================

This hotfix fixes several security issues:

- An unauthorized changing of dexterity content in Plone.  Archetypes content is not affected.
- An attacker can potentially gain information on the ID of private content on your site.  This is for all content.
- A user who can create or edit templates can bypass Restricted Python.  This is only when Chameleon is used, via the ``five.pt`` package.

This hotfix should be applied to the following versions of Plone:

* Plone 5.0.4 and any version prior
* Plone 4.3.9 and any version prior
* Any older version of Plone

The hotfix is officially supported by the Plone security team on the
following versions of Plone in accordance with the Plone
`version support policy`_: 4.0.10, 4.1.6, 4.2.7, 4.3.9 and 5.0.4.
However it has also received some testing on older versions of Plone.
The fixes included here will be incorporated into subsequent releases of Plone,
so Plone 4.3.10, 5.0.5 and greater should not require this hotfix.


Installation
============

Installation instructions can be found at
https://plone.org/products/plone-hotfix/releases/20160419


Q&A
===

Q: How can I confirm that the hotfix is installed correctly and my site is protected?
  A: On startup, the hotfix will log a number of messages to the Zope event log
  that look like this::

    2016-04-19 17:31:58 INFO Products.PloneHotfix20160419 Applied publishing patch
    2016-04-19 17:31:58 INFO Products.PloneHotfix20160419 Applied dexterity patch
    2016-04-19 17:31:58 INFO Products.PloneHotfix20160419 Applied five_pt patch
    2016-04-19 17:31:58 INFO Products.PloneHotfix20160419 Hotfix installed

  The exact number of patches applied, will differ depending on what packages you are using.
  If a patch is attempted but fails, it will be logged as a warning that says
  "Could not apply". This may indicate that you have a non-standard Plone
  installation.

Q: How can I report problems installing the patch?
  A: Contact the Plone security team at security@plone.org, or visit the
  #plone channel on freenode IRC.

Q: How can I report other potential security vulnerabilities?
  A: Please email the security team at security@plone.org rather than discussing
  potential security issues publicly.

.. _`version support policy`: http://plone.org/support/version-support-policy
