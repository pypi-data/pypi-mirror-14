html-json-forms
===============

An implementation of the `HTML JSON
Form <https://www.w3.org/TR/html-json-forms/>`__ specification for use
with the `Django REST
Framework <http://www.django-rest-framework.org/>`__. Extracted from
`wq.db <https://wq.io/wq.db>`__ for general use.

HTML JSON Forms use an array-style naming convention that makes it
possible to represent complex nested JSON objects with regular HTML
fields. The idea is that client applications (such as
`wq.app <https://wq.io/wq.app>`__) and eventually browsers could parse
these fields and submit structured JSON to the server. For backwards
compatibility with older clients, the spec recommends implementing a
fallback parser on the server to ensure that older clients can submit
forms using the traditional method. This Python package is an
implementation of that algorithm.

.. code:: html

    <!-- Input -->
    <form>
      <input name="items[0][name]" value="Example">
      <input name="items[0][count]" value="5">
    </form>

.. code:: js

    // Output
    {
        "items": [
            {
                "name": "Example",
                "count": "5"
            }
        ]
    }

Note that the HTML JSON Form spec was never finalized. The
implementation is still useful as a formal way of representing
structured data via traditional HTML forms.

|Latest PyPI Release| |Release Notes| |License| |GitHub Stars| |GitHub
Forks| |GitHub Issues|

|Travis Build Status| |Python Support| |Django Support|

Usage
-----

``html-json-forms`` is available via PyPI:

.. code:: bash

    pip3 install html-json-forms

Functional
~~~~~~~~~~

.. code:: python

    from html_json_forms import parse_json_form

    parse_json_form({
        'items[0][name]': "Example",
        'items[0][count]': "5",
    })

DRF Integration
~~~~~~~~~~~~~~~

To enable HTML JSON Form parsing in Django REST Framework, subclass
``JSONFormSerializer``:

.. code:: python

    from rest_framework import serializers
    from html_json_forms.serializers import JSONFormSerializer
    from .models import Parent, Child

    class ChildSerializer(serializers.ModelSerializer):
        class Meta:
            model = Child

    class ParentSerializer(JSONFormSerializer, serializers.ModelSerializer):
        children = ChildSerializer(many=True)
        class Meta:
            model = Parent

Note that only the top-level serializer needs to have the
``JSONFormSerializer`` mixin; the nested serializers will "just work" as
if the data had been submitted via JSON. Note further that this module
only handles processing nested form data; it is still up to you to
figure out how to handle `writing nested
models <http://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations>`__
(unless you are using `wq.db <https://wq.io/wq.db>`__'s
`patterns <https://wq.io/docs/about-patterns>`__ module, which includes
writable nested serializers by default).

.. |Latest PyPI Release| image:: https://img.shields.io/pypi/v/html-json-forms.svg
   :target: https://pypi.python.org/pypi/html-json-forms
.. |Release Notes| image:: https://img.shields.io/github/release/wq/html-json-forms.svg
   :target: https://github.com/wq/html-json-forms/releases
.. |License| image:: https://img.shields.io/pypi/l/html-json-forms.svg
   :target: https://github.com/wq/html-json-forms/blob/master/LICENSE
.. |GitHub Stars| image:: https://img.shields.io/github/stars/wq/html-json-forms.svg
   :target: https://github.com/wq/html-json-forms/stargazers
.. |GitHub Forks| image:: https://img.shields.io/github/forks/wq/html-json-forms.svg
   :target: https://github.com/wq/html-json-forms/network
.. |GitHub Issues| image:: https://img.shields.io/github/issues/wq/html-json-forms.svg
   :target: https://github.com/wq/html-json-forms/issues
.. |Travis Build Status| image:: https://img.shields.io/travis/wq/html-json-forms/master.svg
   :target: https://travis-ci.org/wq/html-json-forms
.. |Python Support| image:: https://img.shields.io/pypi/pyversions/html-json-forms.svg
   :target: https://pypi.python.org/pypi/html-json-forms
.. |Django Support| image:: https://img.shields.io/badge/Django-1.8%2C%201.9-blue.svg
   :target: https://pypi.python.org/pypi/html-json-forms
