from setuptools import setup

config = {
    'description': 'Analysis of antibody NGS data',
    'author': 'Bryan Briney',
    'url': 'www.github.com/briney/abtools/',
    # 'download_url': 'www.github.com/briney/abtools/',
    'author_email': 'briney@scripps.edu',
    'version': '0.1.1',
    'install_requires': ['nose',
                         'biopython',
                         'celery',
                         'ete2',
                         'matplotlib',
                         'numpy',
                         'nwalign',
                         'pandas',
                         'pymongo',
                         'scikit-bio',
                         'seaborn'],
    'packages': ['abtools'],
    'scripts': ['bin/abcompare',
                'bin/abcorrect',
                'bin/abfinder',
                'bin/abphylogeny',
                'bin/abstats',
                'bin/ssh_tunnel'],
    'name': 'abtools',
    'include_package_data': True
}

setup(**config)
