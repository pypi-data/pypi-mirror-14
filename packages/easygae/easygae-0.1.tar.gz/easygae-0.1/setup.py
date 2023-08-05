from setuptools import setup


setup(
    name="easygae",
    version="0.1",
    description="Painless Google App Engine Testing - Nose2 Plugin",
    author="Nicholas Amorim",
    author_email="nicholas@alienretro.com",
    url="https://github.com/nicholasamorim/easygae",
    license="MIT",
    install_requires=['nose2'],
    keywords="unittest testing gae appengine nose2 app engine",
    py_modules=["easygae"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
    ],
)
