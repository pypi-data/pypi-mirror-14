from setuptools import setup

setup(name='dautil',
      version='0.0.1a30',
      description='Data analysis utilities',
      url='https://www.packtpub.com/books/info/authors/ivan-idris',
      author='Ivan Idris',
      author_email='ivan.idris@gmail.com',
      license='MIT',
      packages=['dautil'],
      include_package_data=True,
      test_suite='nose.collector',
      tests_require=['nose', 'nose-parameterized'],
      install_requires=[
          'appdirs',
          'landslide'
      ],
      zip_safe=False)
