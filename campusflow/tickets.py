# Allowed categories for support tickets
VALID_CATEGORIES = ["Network", "Hardware", "Software", "Other"]


def validate_category(category):
    """Validate the category and return its standardized form."""
    if not isinstance(category, str):
        raise ValueError("Category must be text.")

    category = category.strip().lower()

    for valid_category in VALID_CATEGORIES:
        if category == valid_category.lower():
            return valid_category

    raise ValueError(
        "Invalid category. Choose Network, Hardware, Software, or Other."
    )