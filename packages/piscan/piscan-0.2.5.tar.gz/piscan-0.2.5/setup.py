from setuptools import setup

setup(name='piscan',
      version='0.2.5',
      description='RXWave.com Uniden DMA Police Scanner agent',
      url='http://www.rxwave.com',
      author='Dave Kolberg',
      author_email='dave@netagile.com',
      license='MIT',
      packages=['piscan'],
      install_requires=['pika','boto','flask'],
      zip_safe=False,
      include_package_data=True,
      package_dir={'piscan': 'piscan'},
      package_data={
        'data' : ['*'],
        'frontend' : ['*'],
      },
      scripts=['bin/piscan-setup.sh'],
)
