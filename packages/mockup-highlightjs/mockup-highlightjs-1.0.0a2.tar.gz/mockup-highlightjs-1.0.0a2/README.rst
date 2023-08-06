Highlightjs for Plone 5.
============================

This addon integrates https://highlightjs.org/ via https://github.com/pcdummy/pat-highlightjs into Plone 5.

Patternslib searches for pre tags and calls https://github.com/pcdummy/pat-highlightjs/blob/master/src/pat-highlightjs.js#L46 on it.


Usage
=====

mockup-highlightjs has 3 profiles:

- **default**: Means register js/css and a extra bundle + download for highlightjs.
- **registerjs**: Just register js/css and include somewhere else.
- **uninstall**: Uninstall both of the above.

registerjs Usage:

Add to **YourAddon.site/profiles/default/metadata.xml**::

    <?xml version="1.0"?>
    <metadata>
      <version>1000</version>
        <dependencies>
          <dependency>profile-mockup-highlightjs:registerjs</dependency>
        </dependencies>
    </metadata>

Add to **YourAddon.theme/profiles/default/registry.xml**::

    <!-- bundle definition -->
    <records prefix="plone.bundles/youraddon-bundle"
              interface='Products.CMFPlone.interfaces.IBundleRegistry'>
      <value key="resources">
        <element>mockup-bundles-highlightjs</element>
        <element>mockup-styles-highlightjs-monokai-sublime</element>
      </value>
      <value key="enabled">True</value>
      <value key="compile">True</value>
      <value key="jscompilation">++theme++youraddon/js/bundle-compiled.js</value>
      <value key="csscompilation">++theme++youraddon/css/persona-compiled.css</value>
      <value key="last_compilation">2016-01-31 00:00:00</value>
    </records>



Bootstrap the JS environment for pattern development
----------------------------------------------------

Make sure, you have `GNU make`, `node` and `git` installed.

Then::

    $ git clone https://github.com/collective/mockup-highlightjs.git
    $ cd mockup-highlightjs
    $ make bootstrap

Then::

    $ python -m SimpleHTTPServer
    $ chrome http://localhost:8000


Run the tests.

In watch mode::

    $ make test pattern=pattern-highlightjs

Only once::

    $ make test-once pattern=pattern-highlightjs

In Google Chrome browser::

    $ make test-dev pattern=pattern-highlightjs


Generate **registerjs entries** for all the available styles::

    $ src/mockup-highlightjs/scripts/echo_less_resources.sh
    $ src/mockup-highlightjs/scripts/echo_less_resources-remove.sh


Bootstrap Plone for testing the Plone integration
----------------------------------------------------

Just use the provided ``make`` target commands (see ``Makefile``, for what they
are doing).

.. note::

    The make targets to bootstrap Plone erase the ``var`` directory! You will
    loose any changes made to your Plone database.

    $ make plone


Contribute
----------

- Issue Tracker: https://github.com/collective/mockup-highlightjs/issues
- Source Code: https://github.com/collective/mockup-highlightjs


Support
-------

If you are having issues, please let me know.


License
-------

The project is licensed under the BSD license.
