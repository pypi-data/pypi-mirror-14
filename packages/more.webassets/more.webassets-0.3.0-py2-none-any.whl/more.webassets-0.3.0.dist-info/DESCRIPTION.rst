
`Webassets <https://webassets.readthedocs.org/en/latest/>`_ |
`Morepath <http://morepath.readthedocs.org/en/latest/>`_

This package is somewhat similar to
`more.static <https://github.com/morepath/more.static>`_, which integrates
`bowerstatic <https://bowerstatic.readthedocs.org/en/latest/>`_ into Morepath.
It is currently not really used anywhere, so you should probably stick to
`more.static <https://github.com/morepath/more.static>`_.

Now that you are sufficently discouraged from using more.webassets, these are
the reasons it might be for you:

* You don't have to learn about javascript package managers (i.e. Bower).
* You can have your assets compiled on the fly.
* Your stylesheets are rendered at the top, your scripts at the bottom. No
  configuration necessary.

If you are alreay familiar with webassets: This package might not be as
powerful as you're used to. It currently has little flexibility. It's also
the first time the author uses webassets, so things might be off.

If you're using Webassets differently than me and you want your ways to work
with more.webassets, do open an issue. I'm happy to turn this into something
more powerful.

Usage
-----

The following app serves a minified jquery from `assets/js/jquery.js`
(relative to the code):

.. code-block:: python

    from more.webassets import WebassetsApp

    class App(WebassetsApp):
        pass

    @App.webasset_path()
    def get_asset_path():
        return 'assets/js'

    @App.webasset_output()
    def get_output_path():
        return 'assets/bundles'

    @App.webasset_filter('js')
    def get_js_filter():
        return 'rjsmin'

    @App.webasset('jquery')
    def get_jquery_asset():
        yield 'jquery.js'

    @App.path('')
    class Root(object):
        pass

    @App.html(model=Root)
    def index(self, request):
        request.include('jquery')

        return '<html><head></head><body>hello</body></html>'

This will result in the following html (formatted for readability):

.. code-block:: html

    <html>
        <head></head>
        <body>hello</body>
        <script type="text/javascript" src="./assets/jquery.bundle.js?1234"></script>
    </html>

For it to work you need an 'assets/js' folder with a 'jquery.js' file in the
same folder as your python file where 'MyApp' is defined.

Documentation
-------------

Most documentation is currently found in source code. Have a look at the
comments `in the directives file <https://github.com/morepath/more.webassets/blob/master/more/webassets/directives.py>`_.

Run the Tests
-------------

Install tox and run it::

    pip install tox
    tox

Limit the tests to a specific python version::

    tox -e py27

Conventions
-----------

More Webassets follows PEP8 as close as possible. To test for it run::

    tox -e pep8

More Webassets uses `Semantic Versioning <http://semver.org/>`_

Build Status
------------

.. image:: https://travis-ci.org/morepath/more.webassets.png
  :target: https://travis-ci.org/morepath/more.webassets
  :alt: Build Status

Coverage
--------

.. image:: https://coveralls.io/repos/morepath/more.webassets/badge.png?branch=master
  :target: https://coveralls.io/r/morepath/more.webassets?branch=master
  :alt: Project Coverage

Latests PyPI Release
--------------------
.. image:: https://pypip.in/v/more.webassets/badge.png
  :target: https://crate.io/packages/more.webassets
  :alt: Latest PyPI Release

License
-------
more.webassets is released under the revised BSD license

Changelog
---------

0.3.0 (2016-04-08)
~~~~~~~~~~~~~~~~~~~

- *Breaking Changes* - This release changes everything!

  Assets are no longer registerd through special methods on the application.
  Instead proper Morepath directives are used. This enables better re-use
  of assets, less verbosity and proper support of inheritance (you can now
  have applications which define assets and child-applications which use
  those assets).

  Have a look at the `readme <https://github.com/morepath/more.webassets>`_ and
  at `the comments in the directives file <https://github.com/morepath/more.webassets/blob/master/more/webassets/directives.py>`_, to get an idea about what has changed.

  Don't hesitate to open an issue if you need help migrating your existing
  setup.

0.2.0 (2016-04-06)
~~~~~~~~~~~~~~~~~~~

- Adds compatibility with morepath 0.13.
  [href]

0.1.1 (2016-01-24)
~~~~~~~~~~~~~~~~~~~

- Disables webassets url caching if debug mode is active.
  [href]

0.1.0 (2016-01-24)
~~~~~~~~~~~~~~~~~~~

- Support webassets debug mode (before it would trigger an exception).
  [href]

0.0.3 (2015-08-07)
~~~~~~~~~~~~~~~~~~~

- Cache the resource urls for increased speed. Note that with this change a
  reload of the application is necessary to get the updated javascript files.

  If this is an issue for you, speak up and we might add a debug flag.
  [href]

0.0.2 (2015-05-18)
~~~~~~~~~~~~~~~~~~~

- Adds more checks to ensure we never serve anything outside the assets
  directory.
  [href]

0.0.1 (2015-04-29)
~~~~~~~~~~~~~~~~~~~

- Initial Release [href]


