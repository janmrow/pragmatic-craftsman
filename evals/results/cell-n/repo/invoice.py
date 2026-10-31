import csv
from decimal import Decimal, InvalidOperation


def invoice_total(text):
    """CSV description,amount header; blank rows ignored; invalid amounts/rows raise ValueError.
    An empty file totals Decimal(0). No partial success on invalid input.
    """
    total = Decimal(0)
    lines = text.splitlines(keepends=True)
    reader = csv.reader(lines, strict=True)
    try:
        next(reader, None)
        previous_line = reader.line_num
        for fields in reader:
            raw_row = ''.join(lines[previous_line:reader.line_num])
            previous_line = reader.line_num
            if not raw_row.strip():
                continue
            if len(fields) != 2:
                raise ValueError('invalid invoice row')
            total += Decimal(fields[1])
    except (csv.Error, InvalidOperation, ValueError) as exc:
        raise ValueError('invalid invoice row') from exc
    return total
