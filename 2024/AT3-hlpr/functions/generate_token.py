import time
import random
import base64
import uuid
import random


from functions.uuid_slug import uuid2slug, slug2uuid
def generate_token(userID: uuid.uuid4):
    slug = uuid2slug(userID)
    # current unix time stored in 4 bytes
    unixtimeBytes = int(time.time()).to_bytes(4)
    # Convert bytes to base64
    unixTimeB64 = base64.urlsafe_b64encode(unixtimeBytes).decode("utf-8").strip('=')

    # Random number within 64 bit integer limit, then converted to 8 bytes and
    # converted to base64
    randomN = int(random.randint(0, 18_446_744_073_709_551_616)).to_bytes(8)
    randomSafe = base64.urlsafe_b64encode(randomN).decode('utf-8').strip('=')

    return f"{slug}.{unixTimeB64}.{randomSafe}"


