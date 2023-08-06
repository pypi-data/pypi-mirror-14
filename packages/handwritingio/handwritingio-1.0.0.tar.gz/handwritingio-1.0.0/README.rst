Handwriting.io Python Client
============================

.. image:: https://img.shields.io/circleci/project/handwritingio/python-client.svg
    :target: https://circleci.com/gh/handwritingio/python-client

.. image:: https://img.shields.io/pypi/v/handwritingio.svg
    :target: https://pypi.python.org/pypi/handwritingio

.. image:: https://img.shields.io/pypi/pyversions/handwritingio.svg

.. image:: https://img.shields.io/pypi/l/handwritingio.svg


Installation
------------

.. code-block:: bash

    $ pip install handwritingio


Basic Example
-------------

Set up the client, render an image, and write it to a file:

.. code-block:: python

    import handwritingio

    hwio = handwritingio.Client('KEY', 'SECRET')
    png = hwio.render_png({
      'handwriting_id': '2D5S46A80003', # found in our catalog or by listing handwritings
      'text': 'Handwriting with Python!',
      'height': 'auto',
    })
    with open('handwriting.png', 'wb') as f:
      f.write(png)

If all goes well, this should create an image similar to the following:

.. image:: https://d2igm8ue20pook.cloudfront.net/python-client/handwriting.png


Advanced Examples
-----------------

List all handwritings, paging through the results as necessary:

.. code-block:: python

    import handwritingio

    hwio = handwritingio.Client('KEY', 'SECRET')
    all_handwritings = [] # we'll add all of the results to this list
    limit = 100 # number of handwritings to get per page
    offset = 0 # starting index
    while True:
      page_of_handwritings = hwio.list_handwritings({
        'limit': limit,
        'offset': offset,
      })
      if not page_of_handwritings:
        # We've exhausted the listing, so we're done
        break
      all_handwritings.extend(page_of_handwritings)
      offset += limit
    # all_handwritings now contains every handwriting available


If you don't need all of the (currently 200+) handwritings for your application,
you could simply fetch the five "most cursive" handwritings, for example:

.. code-block:: python

    import handwritingio

    hwio = handwritingio.Client('KEY', 'SECRET')
    handwritings = hwio.list_handwritings({
      'order_by': 'rating_cursivity',
      'order_dir': 'desc',
      'limit': 5,
    })

Render a PNG and manipulate it with `PIL <http://pillow.readthedocs.org/en/latest/>`_:

.. code-block:: python

    from cStringIO import StringIO

    import handwritingio
    from PIL import Image

    hwio = handwritingio.Client('KEY', 'SECRET')
    png = hwio.render_png({
      'handwriting_id': '2D5S46A80003', # found in our catalog or by listing handwritings
      'text': 'Handwriting with Python!',
      'height': 'auto',
    })
    # Image expects a file-like object, so wrap the image in StringIO:
    im = Image.open(StringIO(png))
    # Rotate the image by 180 degrees:
    im = im.rotate(180, expand=True)
    # Save it to a file:
    im.save('handwriting_upside_down.png')

Which should create the file:

.. image:: https://d2igm8ue20pook.cloudfront.net/python-client/handwriting_upside_down.png

Render a PDF, with a CMYK color for the text:

.. code-block:: python

    import handwritingio

    hwio = handwritingio.Client('KEY', 'SECRET')
    pdf = hwio.render_pdf({
      'handwriting_id': '2D5S46A80003', # found in our catalog or by listing handwritings
      'text': 'Handwriting with Python!',
      'height': 'auto',
      'handwriting_color': '(1, 0.5, 0, 0.2)',
    })
    with open('handwriting.pdf', 'wb') as f:
      f.write(pdf)

If something goes wrong with a request, an exception will be raised:

.. code-block:: python

    import handwritingio

    hwio = handwritingio.Client('KEY', 'SECRET')
    pdf = hwio.render_pdf({
      'handwriting_id': '2D5S46A80003',
      'text': 'Handwriting with Python!',
      'height': 'auto',
      'handwriting_color': 'cheesecake',
      'width': 'double wide',
    })

::

    Traceback (most recent call last):
      File "tester.py", line 9, in <module>
        'width': 'double wide',
      File "build/bdist.linux-x86_64/egg/handwritingio/__init__.py", line 145, in render_pdf
      File "build/bdist.linux-x86_64/egg/handwritingio/__init__.py", line 109, in _hit
    handwritingio.ValidationError: field: width, width unable to parse: "double wide"

But, there's more than one thing wrong with that request. We can see all of the
errors by catching the exception and inspecting the ``errors`` attribute:

.. code-block:: python

    import handwritingio

    hwio = handwritingio.Client('KEY', 'SECRET')
    try:
      pdf = hwio.render_pdf({
        'handwriting_id': '2D5S46A80003',
        'text': 'Handwriting with Python!',
        'height': 'auto',
        'handwriting_color': 'cheesecake',
        'width': 'double wide',
      })
    except handwritingio.ValidationError as e:
      print e.errors

::

    [{u'field': u'width', u'error': u'width unable to parse: "double wide"'},
     {u'field': u'handwriting_color', u'error': u'handwriting_color must be valid CMYK'}]


Reference
---------

See the `API Documentation <https://handwriting.io/docs/>`_ for details on
all endpoints and parameters. For the most part, the ``Client`` passes the
parameters through to the API directly.

The endpoints map to client methods as follows:

- `GET /handwritings <https://handwriting.io/docs/#get-handwritings>`_ -> ``Client.list_handwritings([params])``
- `GET /handwritings/{id} <https://handwriting.io/docs/#get-handwritings--id->`_ -> ``Client.get_handwriting(handwriting_id)``
- `GET /render/png <https://handwriting.io/docs/#get-render-png>`_ -> ``Client.render_png(params)``
- `GET /render/pdf <https://handwriting.io/docs/#get-render-pdf>`_ -> ``Client.render_pdf(params)``

Version Numbers
---------------

Version numbers for this package work slightly differently than standard
`semantic versioning <http://semver.org/>`_. For this package, the ``major``
version number will match the Handwriting.io API version number, and the
``minor`` version will be  incremented for any breaking changes to this package.
The ``patch`` version will be incremented for bug fixes and changes that add
functionality only.

For this reason, we recommend that you pin this dependency to the
**minor version**, for example, in your ``requirements.txt`` or ``setup.py``,
use::

    handwritingio>=1.0<1.1


Issues
------

Please open an issue on `Github <https://github.com/handwritingio/python-client>`_
or `contact us <https://handwriting.io/contact>`_ directly for help with any
problems you find.
