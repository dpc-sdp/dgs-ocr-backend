
def mask_username(username):
    # Mask the username by showing only the first two letters and the last two letters
    if len(username) > 4:
        masked_chars = '*' * (len(username) - 4)
        masked_username = username[:2] + masked_chars + username[-2:]
    else:
        masked_username = '*' * len(username)
    return masked_username
