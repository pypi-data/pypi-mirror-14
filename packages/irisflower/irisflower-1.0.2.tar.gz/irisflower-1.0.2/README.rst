========================
Irish Flower Classifier
========================

.. image:: https://travis-ci.org/risan/iris-flower-classifier.svg?branch=master
    :target: https://travis-ci.org/risan/iris-flower-classifier
.. image:: https://coveralls.io/repos/github/risan/iris-flower-classifier/badge.svg?branch=master
    :target: https://coveralls.io/github/risan/iris-flower-classifier?branch=master
.. image:: https://img.shields.io/pypi/v/irisflower.svg
    :target: https://pypi.python.org/pypi/irisflower/
.. image:: https://img.shields.io/pypi/l/irisflower.svg
    :target: https://pypi.python.org/pypi/irisflower/

Simple module for identiying Irish flower species based on it's sepal and petal dimensions.

Dependencies
------------------------

- `SciPy <http://www.scipy.org/>`_
- `Scikit Learn <http://scikit-learn.org/>`_

Installation
------------------------

The recomended way to install this module is through `pip <https://pip.pypa.io/>`_.

.. code-block:: bash

    pip install irisflower

How To Use
------------------------

.. code-block:: python

    # Import IrishFlowerClassifier class.
    from irisflower.classifier import IrisFlowerClassifier

    # Create a new instance of IrisFlowerClassifier.
    iris_flower = IrisFlowerClassifier()

    # Finaly classify the flower species.
    print iris_flower.classify(sepal_length=5,sepal_width=3,petal_length=1,petal_width=0.2)

Running Test
------------------------

If you already have `node <https://nose.readthedocs.org/>`_nose installed on your machine, simple run the following command:

.. code-block:: bash

    nosetests

Or you can also run the built in Python unittest command like so:

.. code-block:: bash

    python -m unittest tests.test_classifier

This is my first attempt to learn machine learning and also
my first code written in Python! :snake:
