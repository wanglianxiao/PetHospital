import azure.storage.file
from azure.storage.file import FileService
# from azure.storage.file import ContentSettings

file_service = **FileService**(account_name='wangpiaoliang', account_key='cXfnJkmgJgwZH6frhAeqOHSqOrK+KH9Dhau4YGtcIt6ylRDIDnHOu3TQj9lPir7DPecPS1oogU+SNmp1mzyLVg==')

file_service.create_share('mei')

file_service.create_file_from_path(
    'mei',
    None, # We want to create this blob in the root directory, so we specify None for the directory_name
    'case',
    'wanglianxiao.jpeg',
    content_settings=azure.storage.file.ContentSettings(content_type='image/jpeg'))