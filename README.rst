## Linprog Solver

This website solves linear programming problem via a two-phase simplex algorithm using [scipy](https://github.com/scipy/scipy) library.

:License: MIT


## Live (screenshots)

![Screens](https://raw.githubusercontent.com/apirobot/django-linprog-solver-website/master/screens.png)


## How to run locally

Installing and running this website is very simple. Clone this repo, and then simply run:

```zsh
➜  ~ docker-compose -f dev.yml build
➜  ~ docker-compose -f dev.yml up
```

That's all. Isn't Docker amazing?


### Running tests with py.test

```zsh
➜  ~ py.test
```


### Docker

See detailed [`cookiecutter-django Docker documentation`](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html)


## Credits

Tools used in rendering this package:

- [`cookiecutter`](https://github.com/audreyr/cookiecutter)
- [`cookiecutter-djangopackage`](https://github.com/pydanny/cookiecutter-djangopackage)
