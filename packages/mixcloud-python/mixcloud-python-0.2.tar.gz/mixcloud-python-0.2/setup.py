import setuptools

setuptools.setup(
    name="mixcloud-python",
    version="0.2",
    url="https://github.com/Said007/mixcloud-python",

    author="Said Ali",
    author_email="said.ali@msn.com",

    description="A Python wrapper around the Mixcloud API",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=['six>=1.10.0', 'requests>=2.9.1'],

    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
