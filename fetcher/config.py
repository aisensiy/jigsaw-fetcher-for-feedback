import os

JIGSAW_TOKEN = os.getenv('JIGSAW_TOKEN')
ENTRYPOINT = os.getenv('ENTRYPOINT', 'http://ketsu-backend.aisensiy.com')
USERNAME = os.getenv('USERNAME', 'admin')
PASSWORD = os.getenv('PASSWORD', '123')
