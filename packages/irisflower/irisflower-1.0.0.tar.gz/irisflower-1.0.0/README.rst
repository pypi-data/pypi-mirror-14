========================
Irish Flower Classifier
========================

Simple module for identiying Irish flower species based on it's sepal and petal dimensions.

Dependencies
------------------------

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


This is my first attempt to learn machine learning and also
my first code written in Python! :snake:
