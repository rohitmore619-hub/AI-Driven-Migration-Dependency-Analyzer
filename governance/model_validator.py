def validate_ai_output(response):
    if len(response) < 20:
        return False

    return True