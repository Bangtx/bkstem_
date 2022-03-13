from utils import aws
from config.setting import (
    THUMBNAIL_SERVICE_AWS_SECRET_KEY,
    THUMBNAIL_SERVICE_AWS_ACCESS_KEY,
    THUMBNAIL_SERVICE_S3_BUCKET_NAME,
    THUMBNAIL_SERVICE_S3_REGION,
    THUMBNAIL_SERVICE_CLOUDFRONT_DOMAIN,
)
import uuid
import datetime


def upload_image(content: bytes, mime: str) -> str:
    """
    Upload image and return s3 key
    :param content: file content
    :param mime:
    :return: str s3 path of file
    """
    now = datetime.datetime.now()
    key = f"{now.year}/{now.month}/{now.day}/{uuid.uuid4()}"

    s3_client = aws.get_s3_client(
        aws_access_key_id=THUMBNAIL_SERVICE_AWS_ACCESS_KEY,
        aws_secret_access_key=THUMBNAIL_SERVICE_AWS_SECRET_KEY,
        region_name=THUMBNAIL_SERVICE_S3_REGION,
    )
    s3_client.put_object(
        Bucket=THUMBNAIL_SERVICE_S3_BUCKET_NAME,
        Key=f"{key}/original",
        Body=content,
        ContentType=mime,
        ACL="private",
    )
    return key


def get_link_thumbnail(
    key: str, dimension: int = 300, fit: str = "cover"
) -> str:
    """
    return thumbnail image url
    :param key: s3 key
    :param dimension:
    :param fit:
    :return: cloudfront url
    """
    return get_link(key, dimension, fit)


def get_link_resize(
    key: str, dimension: int = 2000, fit: str = "inside"
) -> str:
    """
    return resized image url
    :param key: s3 key
    :param dimension:
    :param fit:
    :return: cloudfront url
    """
    return get_link(key, dimension, fit)


def get_link(key: str, dimension: int, fit: str) -> str:
    """
    return cloudfront url
    :param key:
    :param dimension:
    :param fit:
    :return:
    """
    return (
        f"https://{THUMBNAIL_SERVICE_CLOUDFRONT_DOMAIN}/{key}.jpeg"
        f"?dim={dimension}x{dimension}&fit={fit}"
    )
