from distutils.core import setup
setup(
    name='getgauge',
    packages=['getgauge', 'getgauge/messages'],
    version='0.0.4',
    description='Enables Python support for Gauge',
    author='Kashish Munjal',
    author_email='kashishmunjal64@gmail.com',
    url='https://github.com/kashishm/gauge-python',
    download_url='https://github.com/kashishm/gauge-python/archive/v0.0.4.zip',
    keywords=['testing', 'gauge', 'gauge-python', 'getgauge', 'automation'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=['protobuf', 'redBaron'],
)
