def list_documents(records, limit=20, include_archived=False):
    """Return ordered copies of records, excluding archived records by default."""
    return [
        dict(row)
        for row in records
        if include_archived or not row.get('archived', False)
    ][:limit]
