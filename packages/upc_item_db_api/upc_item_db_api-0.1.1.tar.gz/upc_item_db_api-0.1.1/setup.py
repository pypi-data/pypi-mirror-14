from setuptools import setup

setup(name='upc_item_db_api',
      version='0.1.1',
      description='Python wrapper for UPC Item DB API',
      author='Ben Muschol',
      author_email='benmuschol@gmail.com',
      url='https://github.com/benmusch/upc-item-db-api-python',
      license='MIT',
      install_requires=[
          'requests',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      packages=['upc_item_db_api'])
