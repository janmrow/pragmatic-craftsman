# Local fixture
Python 3.10+, standard library only. No external services or production access.
Run existing tests with `python3 -m unittest discover -v` from this directory.

`list_documents(records, limit=20, include_archived=False)` returns a list of
shallow dictionary copies in input order. Archived records are excluded by
default; pass `include_archived=True` to include them. The limit is applied
after filtering, and existing positional limits still work:
`list_documents(records, 5, include_archived=True)`.
