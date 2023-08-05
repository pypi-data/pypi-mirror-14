Flask-RESTy |Travis| |PyPI|
===========================

Building blocks for REST APIs for `Flask <http://flask.pocoo.org/>`__.

|Coveralls|

Usage
-----

Create a `SQLAlchemy <http://www.sqlalchemy.org/>`__ model and a
`marshmallow <http://marshmallow.rtfd.org/>`__ schema, then:

.. code:: python

    from flask_resty import Api, GenericModelView

    from .models import Widget
    from .schemas import WidgetSchema


    class WidgetViewBase(GenericModelView):
        model = Widget
        schema = WidgetSchema()


    class WidgetListView(WidgetViewBase):
        def get(self):
            return self.list()

        def post(self):
            return self.create()


    class WidgetView(WidgetViewBase):
        def get(self, id):
            return self.retrieve(id)

        def patch(self, id):
            return self.update(id, partial=True)

        def delete(self, id):
            return self.destroy(id)


    api = Api(app, '/api')
    api.add_resource('/widgets', WidgetListView, WidgetView)

.. |Travis| image:: https://img.shields.io/travis/4Catalyzer/flask-resty/master.svg
   :target: https://travis-ci.org/4Catalyzer/flask-resty
.. |PyPI| image:: https://img.shields.io/pypi/v/Flask-RESTy.svg
   :target: https://pypi.python.org/pypi/Flask-RESTy
.. |Coveralls| image:: https://img.shields.io/coveralls/4Catalyzer/flask-resty/master.svg
   :target: https://coveralls.io/github/4Catalyzer/flask-resty
