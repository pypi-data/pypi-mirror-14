from setuptools import setup

setup(name='piscan',
      version='0.2.7',
      description='RXWave.com Uniden DMA Police Scanner agent',
      keywords='RXwave Police-scanner Uniden DMA RXWave.com RX-Wave.com radio scanner',
      url='http://www.rxwave.com',
      author='Dave Kolberg',
      author_email='dave@netagile.com',
      license='MIT',
      packages=['piscan'],
      install_requires=['pika','boto','flask','sh'],
      zip_safe=False,
      include_package_data=True,
      package_dir={'piscan': 'piscan'},
      package_data={
        'data' : ['*'],
        'frontend' : ['*'],
      },
      scripts=['bin/piscan-setup.sh'],
)
