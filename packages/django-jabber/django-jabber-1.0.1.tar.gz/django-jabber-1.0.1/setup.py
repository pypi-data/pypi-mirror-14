import setuptools


def parse_requirements(requirements_file):
    with open(requirements_file, 'r') as f:
        return [line for line in f
                if line.strip() and not line.startswith('#')]

setuptools.setup(
    name="django-jabber",
    version="1.0.1",
    url="https://github.com/alexmorozov/django-jabber",

    author="Alex Morozov",
    author_email="inductor2000@mail.ru",

    description="Send Jabber notifications from Django",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=parse_requirements('requirements.txt'),

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
