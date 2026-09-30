# Base62 uses 62 characters: 0-9, a-z, A-Z (10 + 26 + 26 = 62 symbols)
# More symbols per digit = shorter codes for the same number, compared to base10.
BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encode_base62(number: int) -> str:
    """
    Converts an integer (like a database row's auto-incrementing id)
    into a short base62 string (like '47' -> 'p').
    """
    if number == 0:
        return BASE62_ALPHABET[0]

    base = len(BASE62_ALPHABET)  # 62
    result = []

    while number > 0:
        remainder = number % base       # find the next "digit" in base62
        result.append(BASE62_ALPHABET[remainder])
        number = number // base          # shrink the number for the next loop

    # We build the digits from least-significant to most-significant,
    # so reverse at the end to get the correct order.
    return "".join(reversed(result))