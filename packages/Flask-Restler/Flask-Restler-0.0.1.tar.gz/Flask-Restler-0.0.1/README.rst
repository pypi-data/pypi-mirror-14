The Flask RESTler
#################

.. _badges:

.. _description:

The Flask RESTler -- Build REST API for Flask_ using Marshmallow_.

Example "Hello User" with the Flask-resler:

.. code-block:: python

    from flask_restler import Api, Resource


    # flask_restler.Api is subclass of Flask.Blueprint
    api = Api('My awesome API', __name__, url_prefix='/api/v1')

    # flask_restler.Resource is subclass of Flask.views.View
    @api.connect
    class HelloResource(Resource):

        def get(self, resource=None):
            return 'Hello World!'


    # Regiater with your application
    from your_project import app

    app.register_blueprint(api)

    if __name__ == '__main__':
        app.run()


Run the application and open http://localhost:5000/api/v1/ in your browser.


.. _contents:

.. contents::

Requirements
=============

- python 2.7+,3.4+

.. _installation:

Installation
=============

**Flask-RESTler** should be installed using pip: ::

    pip install flask-restler

.. _usage:

Usage
=====

.. _bugtracker:

Bug tracker
===========

If you have any suggestions, bug reports or
annoyances please report them to the issue tracker
at https://github.com/klen/flask-restler/issues

.. _contributing:

Contributing
============

Development of The Flask-restler happens at: https://github.com/klen/flask-restler


Contributors
=============

* `Kirill Klenov <https://github.com/klen>`_

.. _license:

License
========

Licensed under a MIT license (See LICENSE)

If you wish to express your appreciation for the project, you are welcome to
send a postcard to: ::

    Kirill Klenov
    pos. Severny 8-3
    MO, Istra, 143500
    Russia

.. _links:

.. _klen: https://github.com/klen
.. _Flask: http://flask.pocoo.org/
.. _Marshmallow: https://marshmallow.readthedocs.org/en/latest/
