# Local fixture
Python 3.10+, standard library only. No external services or production access.
Run existing tests with `python3 -m unittest discover -v` from this directory.

Not-found policy: raise service.NotFound for missing and unauthorized documents without revealing ownership.
Existing authorized get returns a dict; delete returns None. Read and delete are independent entry points.
Store.get returns trusted persisted records containing id,tenant_id,title; all writes are outside this ticket.
