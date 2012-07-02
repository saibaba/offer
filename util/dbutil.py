from util.monad import do, Right, Left, Just, Nothing

@do
def find(tbl, column_name, value):
    r = None
    s = tbl.select(tbl.columns[column_name] == value)
    rs = s.execute()
    i = 0
    for row in rs:
        i = i + 1
        if i > 1:
            break
        r = row

    if i == 0:
        yield Left("%s with %s: %s not found" % (tbl, column_name, value) )
    elif i > 1:
        yield Left("Too many records in %s with %s = %s" % (tbl, column_name, value) )
    else:
        yield Right(r)

@do
def list(tbl):
    s = tbl.select()
    rs = s.execute()
    rows =  [row for row in rs]
    if len(rows) > 0:
        yield Just(rows)
    else:
        yield Nothing()
