from setuptools import setup, find_packages

setup(
    author='Thomas Steinert',
    author_email='monk@10forge.org',
    classifiers=[
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Systems Administration',
        'Programming Language :: Python :: 3.5',
    ],
    description='Python interface for interacting with proxmox.',
    install_requires=[
        'paramiko>=1.16.0',
    ],
    keywords=['api', 'http', 'proxmox', 'pve', 'shell'],
    license='GPLv3',
    name='libpve',
    package_data={
        '': ['LICENSE.txt', 'README.md'],
    },
    packages=find_packages(
         exclude=[
            'test'
        ]
    ),
    url='https://github.com/m-o-n-k/python.libpve.git',
    version='0.1.2',
    zip_safe=False)
