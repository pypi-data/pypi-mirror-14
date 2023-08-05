from setuptools import setup


setup(
    name='glb-slave',
    description='GLB slave client.',
    version='0.0.18',
    author='Lain',
    author_email='softliunaisen@gmail.com',
    url='https://pypi.python.org/pypi/glb-slave/',
    packages=['glb_slave'],
    data_files=[('glb_slave/data', ['glb_slave/data/nginx.conf.data'])],
    entry_points={
        'console_scripts': [
            'glb_slave=glb_slave:process'
        ]
    },
    install_requires=['click', 'websocket-client'],
    tests_require=['pytest'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
)
