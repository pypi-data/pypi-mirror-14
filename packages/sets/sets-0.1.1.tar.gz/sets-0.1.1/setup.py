import setuptools


if __name__ == '__main__':
    setuptools.setup(
        name='sets',
        version='0.1.1',
        description='Read datasets in a standard way.',
        url='http://github.com/danijar/sets',
        author='Danijar Hafner',
        author_email='mail@danijar.com',
        license='MIT',
        packages=['sets', 'sets.core'],
        install_requires=['numpy'],
    )
