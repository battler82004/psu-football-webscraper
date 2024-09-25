# Decodes emails encoded By Cloudflare
# 2024-09-24

def decode_email(code):
    """
    Tokes an email that has been encoded by Cloudflare and returns the decoded email as a string.
    """
    r = int(code[:2], 16)
    email = "".join([chr(int(code[i : i + 2], 16) ^ r) for i in range(2, len(code), 2)])
    return email