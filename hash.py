import hashlib

def sha256_hash(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    hashed_data = sha256.hexdigest()
    return hashed_data