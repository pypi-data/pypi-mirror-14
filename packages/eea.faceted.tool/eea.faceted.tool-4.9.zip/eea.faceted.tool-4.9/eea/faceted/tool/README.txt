EEA Faceted Tool

  Extends eea.facetednavigation functionality.


  Requires

    * "eea.faceted.vocabularies", http://eggrepo.eea.europa.eu/simple

    * "Plone 2.5", http://launchpad.net/plone/2.5/2.5.5 (fully supported)

      - "plone.app.form", http://svn.plone.org/svn/plone/plone.app.form/branches/plone-2.5

      - "CMFonFive", http://codespeak.net/svn/z3/CMFonFive/trunk

      - "Five", http://svn.zope.org/repos/main/Products.Five/branches/1.4

      - "FiveSite", http://svn.eionet.europa.eu/repositories/Zope/trunk/FiveSite

    * "Plone 3.3", https://launchpad.net/plone/3.3/3.3.1 (fully supported)

  Install

    1. zc.buildout

      * buildout.cfg should look like::

        find-links =
            http://eggrepo.eea.europa.eu/simple
            ...

        develop =
            src/plone.app.form (Plone 2.5 only)
            ...

        eggs =
          eea.faceted.tool
          ...

        [instance]
        zcml =
            eea.faceted.tool

Documentation

  See the **docs** directory in this package.

Authors and contributors

  * "Alin Voinea", mailto:alin.voinea@eaudeweb.ro

  * "Antonio De Marinis", mailto:antonio.de.marinis@eea.europa.eu

  * "Alec Ghica", mailto:alec.ghica@eaudeweb.ro
