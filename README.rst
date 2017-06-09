Linprog Solver
==============

This website solves linear programming problem via a two-phase simplex algorithm using [scipy](https://github.com/scipy/scipy) library.

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django


:License: MIT


Live (screenshots)
-------
![Screenshot of my shell prompt](https://raw.githubusercontent.com/apirobot/django-linprog-solver-website/master/screens.png)


How to run locally
-------

Installing and running this website is very simple. Clone this repo, and then simply run:

```zsh
➜  ~ docker-compose -f dev.yml build
➜  ~ docker-compose -f dev.yml up
```

That's all. Isn't Docker amazing?


Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

```zsh
➜  ~ py.test
```


Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html


Credits
-------

Tools used in rendering this package:

*  `cookiecutter`_
*  `cookiecutter-djangopackage`_

.. _`cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
