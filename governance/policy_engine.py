def validate_dependency_input(data):
    if not data:
        return False, "Empty dependency input"

    if len(data) > 500:
        return False, "Dependency volume too high"

    return True, "Validated"