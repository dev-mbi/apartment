import subprocess
import sys

from app import create_app

app = create_app()

if __name__ == '__main__':
    sys.exit(subprocess.call([
        sys.executable, '-m', 'gunicorn',
        '--bind', '0.0.0.0:5000',
        '--workers', '2', '--threads', '4',
        'app:create_app()'
    ]))
