import os

JIGSAW_TOKEN = os.getenv('JIGSAW_TOKEN')
KETSU_ENTRYPOINT = os.getenv('KETSU_ENTRYPOINT', 'http://ketsu-backend.aisensiy.com')
KETSU_USERNAME = os.getenv('KETSU_USERNAME', 'admin')
KETSU_PASSWORD = os.getenv('KETSU_PASSWORD', '123')
