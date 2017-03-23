from azure.storage.blob import BlockBlobService
block_blob_service = BlockBlobService(account_name='wangpiaoliang', account_key='cp9hQ73nKEmVv3RxPynT+Z3AvlvRLjw84GHh+FgkMjgfKv+rG+mHn65ZDLT3BxdhQZnQkoU/KtgWCxs2P1wvmQ==')

# block_blob_service.create_container('mycontainer')
generator = block_blob_service.list_blobs('mei')
for blob in generator:
    print(blob.name)

from azure.storage.blob import ContentSettings
block_blob_service.create_blob_from_path(
    'mei',
    'WechatIMG81.jpeg',
    'WechatIMG81.jpeg',
    content_settings=ContentSettings(content_type='image/jpeg')
            )

generator = block_blob_service.list_blobs('mei')
for blob in generator:
    print(blob.name)
