=================
bottle-streamline
=================

.. image:: https://readthedocs.org/projects/bottle-streamline/badge/?version=latest
    :target: http://bottle-streamline.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status
                
.. image:: https://readthedocs.org/projects/bottle-streamline/badge/?version=develop
    :target: http://bottle-streamline.readthedocs.org/en/develop/?badge=develop
    :alt: Development documentation Status


This project is a collection of classes for writing complex, modullar, and/or
reusable route handlers using `bottle <http://bottlepy.org>`_ web framework.

Even though 'complex route handlers' may seem like an oximoron, there may be
situations where support for multiple parameters are needed or where a simple
branching in the route handler code may completely change the logic of your 
route handler. If you find yourself running into this type of situation and
struggle to organize the code, you may find bottle-streamline is a good fit for
your project.

Quick example
=============

Example of a classic Hello world app::

    import bottle
    from streamline import RouteBase


    class Hello(BaseRoute):
        def get(self):
            return 'Hello world!'


    Hello.route('/')
    bottle.run()

Documentation
=============

You will find the complete documentation and tutorials `on ReadTheDocs
<http://bottle-streamline.readthedocs.org/>`_.
