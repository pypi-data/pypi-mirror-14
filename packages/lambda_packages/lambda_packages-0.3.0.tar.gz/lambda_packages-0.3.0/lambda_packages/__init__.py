import os

# A manifest of the included packages.
lambda_packages = {
    'MySQL-Python': {
        'version': '1.2.5',
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'MySQL-Python', 'MySQL-Python-1.2.5.tar.gz')
    },
    'psycopg2': {
        'version': '2.6.1',
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'psycopg2', 'psycopg2-2.6.1.tar.gz')
    },
    'Pillow':{
    	'version':'3.1.1',
    	'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Pillow', 'Pillow-3.1.1.tar.gz')
    }
}
