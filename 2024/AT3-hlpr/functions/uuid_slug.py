import base64
import uuid

def uuid2slug(user_uuid: uuid.uuid4):
    """converts from a uuid object to a url safe base64 slug

    Args:
        uuidstring (uuid.uuid4): uuid object

    Returns:
        string: the base64 slug
    """
    uuidString = str(user_uuid)
    return base64.urlsafe_b64encode(user_uuid.bytes).decode("utf-8").strip('=')

def slug2uuid(slug):
    return uuid.UUID(bytes=base64.urlsafe_b64decode(slug+'=='))