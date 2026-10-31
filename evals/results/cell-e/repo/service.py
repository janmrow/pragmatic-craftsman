class NotFound(Exception):
    pass


def get_document(store, tenant_id, document_id):
    document = store.get(document_id)
    if document is None or document["tenant_id"] != tenant_id:
        raise NotFound
    return document


def delete_document(store, tenant_id, document_id):
    get_document(store, tenant_id, document_id)
    store.delete(document_id)
