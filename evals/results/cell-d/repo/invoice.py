import csv
from decimal import Decimal, DecimalException
from io import StringIO


def invoice_total(text):
    """CSV description,amount header; blank rows ignored; invalid amounts/rows raise ValueError.
    An empty file totals Decimal(0). No partial success on invalid input.
    """
    total = Decimal(0)
    rows = csv.reader(StringIO(text, newline=''), strict=True)
    try:
        next(rows, None)
        for fields in rows:
            if not fields or (len(fields) == 1 and not fields[0].strip()):
                continue
            if len(fields) != 2:
                raise ValueError('expected description and amount')
            total += Decimal(fields[1])
    except (csv.Error, DecimalException, ValueError) as exc:
        raise ValueError('invalid invoice row') from exc
    return total
