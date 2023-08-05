from setuptools import setup

setup(
    name='django-directed-edge',
    version='2.0.2',
    packages=(
        'django_directed_edge',
    ),
    url='https://chris-lamb.co.uk/projects/django-directed-edge',
    author="Chris Lamb",
    author_email="chris@chris-lamb.co.uk",
    description="Helpful Django-oriented sugar around around DirectedEdge's Python API",

    install_requires=(
        'Django>=1.8',
    ),
)
