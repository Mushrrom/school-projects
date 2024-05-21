import base64
import uuid

def uuid2slug(user_uuid: uuid.uuid4):
    """converts from a uuid object to a url safe base64 slug

    Args:
        uuidstring (uuid.uuid4): uuid object

    Returns:
        string: the base64 slug
    """
    uuidString = str(user_uuid).encode('utf-8')
    # return base64.urlsafe_b64encode(user_uuid.bytes).decode("utf-8").strip('=')
    uuidb64 = str(base64.b64encode(uuidString))
    uuidb64 = uuidb64[2:-1]
    return uuidb64

def slug2uuid(slug):
    return str(base64.b64decode(slug))[2:-1]