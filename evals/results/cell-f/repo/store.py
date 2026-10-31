class Store:
    """In-memory local store. Requests are serialized. Missing keys return None.
    The production adapter has the same API and trusted tenant_id records.
    """
    def __init__(self, rows):
        self.rows = {r['id']: dict(r) for r in rows}
    def get(self, document_id):
        row = self.rows.get(document_id)
        return dict(row) if row else None
    def delete(self, document_id):
        self.rows.pop(document_id, None)
