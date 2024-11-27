import random

def get_random_verification_code(limit: int = 6):
    return ''.join(random.choices('0123456789', k=limit))
