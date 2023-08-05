import os

import os
os.path.dirname(os.path.abspath(__file__))

# A manifest of the included packages.
lambda_packages = {
    'psycopg2': {
        'version': '2.6.1',
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'psycopg2', 'psycopg2-2.6.1.tar.gz')
    }
}