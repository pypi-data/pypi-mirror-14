from setuptools import setup, find_packages

config = {
    'description': "A suite of tools for portable automated scientific protocols.",
    'author': "OpenTrons",
    'author_email': 'info@opentrons.com',
    'url': 'http://opentrons.com',
    'version': '0.4',
    'install_requires': ['pyyaml'],
    'packages': find_packages(),
    'package_data': { 
        "labsuite": [
            "config/containers/**/*.yml",
            "config/containers/legacy_containers.json",
            "compilers/data/*",
            "compilers/templates/*"
        ]
    },
    'name': 'labsuite',
    'test_suite': 'nose.collector',
    'zip_safe': False
}

setup(**config)
