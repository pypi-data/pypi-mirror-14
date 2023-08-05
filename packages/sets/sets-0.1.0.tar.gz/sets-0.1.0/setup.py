import setuptools


if __name__ == '__main__':
    setuptools.setup(
        name='sets',
        version='0.1.0',
        description='Read datasets in a standard way.',
        url='http://github.com/danijar/sets',
        author='Danijar Hafner',
        author_email='mail@danijar.com',
        license='MIT',
        packages=['sets'],
        install_requires=['numpy'],
    )
