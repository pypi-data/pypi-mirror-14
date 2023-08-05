# encoding: utf-8
from __future__ import print_function

import table
import expressions

def test_0():
    t = table.Table(["a", "b", "c", "d", "e", "f", "g"],
                    [int, float, str, bool, tuple, object, table.Table],
                    ["%d", "%f", "%s", "%s", "%r", "%r", "%r"],
                    rows=[[1, 2.0, "hi", False, (1, 2), list(), None],
                        [None] * 7])
    print(t.rows)
    print()
    print(t.rows.info())
    print()
    print(t.none_positions)
    print()
    print(t._colTypes)
    print()
    print(t.a.values, map(type, t.a.values))
    print(t.b.values, map(type, t.b.values))
    print(t.c.values, map(type, t.c.values))
    print(t.d.values, map(type, t.d.values))
    print(t.e.values, map(type, t.e.values))
    print(t.f.values, map(type, t.f.values))
    print(t.g.values, map(type, t.g.values))
    print()

    print(t)
    t.addColumn("h", (3, None), type_=int)
    t.replaceColumn("h", (4, None), type_=int)
    print(t)
    print()

    t.addRow([0] * 8)
    print(t)
    print()
    for name in "abcdefgh":
        print(t.rows[name].values)
        print(t.getColumn(name).values)

    t.addRow([None] * 8)
    print(t)
    print()
    for name in "abcdefgh":
        print(t.rows[name].values)

    print(t.getColNames())
    print(t)
    t.info()
    print(t.getVisibleCols())
    t.setColFormat("h", None)
    print(t.getVisibleCols())
    t.setColFormat("h", "%d")
    print(t)
    print(t.getColumnValues("a"))
    print(t.getColumnValues("h"))
    print(t[0])
    print(t[0:2, 1:])
    import cPickle
    t = cPickle.loads(cPickle.dumps(t))
    print(t)
    for row in t:
        print(row)

    t.addEnumeration()
    print(t)
    t.sortBy("a")
    print(t)
    print(t.extractColumns("h", "g", "a"))
    t.renameColumns(a="aa", b="bb")
    print(t)
    print(t.aa.values)
    print(t.bb.values)
    t.setColFormat("id", "%03d")
    print(t)
    t.storeCSV("ohne.csv", False)
    t.storeCSV("mit.csv", True)
    t.store("neu.table", True)
    print(table.Table.load("neu.table"))
    print(table.Table.load("old.table"))
    print(t.buildEmptyClone())
    t.dropColumns("a*")
    print(t)
    ti = t.splitBy("d")




def main():
    import cStringIO
    import sys
    import difflib
    sys.stdout = cStringIO.StringIO()
    test_0()
    collected = sys.stdout.getvalue()
    sys.stdout = sys.__stdout__
    tobe = open("tobe", "r").read()

    if tobe != collected:
        if len(sys.argv) > 1:
            open("tobe", "w").write(collected)
        tobe = tobe.split("\n")
        collected = collected.split("\n")
        tobe = map(lambda s: s.rstrip(), tobe)
        collected = map(lambda s: s.rstrip(), collected)
        collected = list(difflib.unified_diff(collected, tobe, "is", "tobe", lineterm=""))
        print("\n".join(collected))

main()
