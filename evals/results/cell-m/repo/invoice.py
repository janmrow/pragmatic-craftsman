import csv
from decimal import Decimal, InvalidOperation


def invoice_total(text):
    """CSV description,amount header; blank rows ignored; invalid amounts/rows raise ValueError.
    An empty file totals Decimal(0). No partial success on invalid input.
    """
    total = Decimal(0)
    lines = text.splitlines(keepends=True)
    rows = csv.reader(lines, strict=True)
    try:
        next(rows, None)
        for fields in rows:
            # Only physical blank rows are ignored; a quoted empty field is invalid.
            if not fields or (len(fields) == 1 and not lines[rows.line_num - 1].strip()):
                continue
            if len(fields) != 2:
                raise ValueError('invalid invoice row')
            total += Decimal(fields[1])
    except (csv.Error, InvalidOperation) as exc:
        raise ValueError('invalid invoice row') from exc
    return total
