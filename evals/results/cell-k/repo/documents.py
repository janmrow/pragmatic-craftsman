def list_documents(records, limit=20, include_archived=False):
    """Return up to limit shallow copies, optionally including archived records."""
    return [
        dict(row)
        for row in records
        if include_archived or not row.get('archived', False)
    ][:limit]
