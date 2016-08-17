import os

JIGSAW_TOKEN = os.getenv('JIGSAW_TOKEN')
FEEDBACK_ENTRYPOINT = os.getenv('FEEDBACK_ENTRYPOINT', 'http://ketsu-backend.aisensiy.com')
FEEDBACK_USERNAME = os.getenv('FEEDBACK_USERNAME', 'admin')
FEEDBACK_PASSWORD = os.getenv('FEEDBACK_PASSWORD', '123')
