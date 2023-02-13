from bucket import Bucket


def upload_image_task(name, image):
    result = Bucket.upload_image(name=name, image=image)
    return result

