
def clean_manga_title(title):
    # List of characters to keep
    valid_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789- "

    # Remove unwanted characters
    cleaned_titles = ''.join(char for char in title if char in valid_characters)

    return cleaned_titles
