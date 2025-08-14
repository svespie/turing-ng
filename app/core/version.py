def get_version() -> str:
    """
    Returns the current version as described in the VERSION file.
    """
    try:
        with open("VERSION", "r") as f:
            return f.read().strip()
    except Exception:
        return "unknown"