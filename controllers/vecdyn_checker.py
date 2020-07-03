import sys
import csv
from vecdyn_csv_validator import *
import os
import cStringIO
from gluon.serializers import xml

def vecdyn_csv_checker():
    data = ()
    form = SQLFORM(db.vecdyn_validator, comments=False, fields=['csvfile'],
                   labels={'csvfile': 'Click to search and select a file:'})
    if form.process().accepted:
        filename, csvfile = db.vecdyn_validator.csvfile.retrieve(form.vars.csvfile)
        csvfile = csv.reader(csvfile)
        # Get all rows of csv from csv_reader object as list of tuples
        csvfile = list(map(tuple, csvfile))
        # a simple validator to be tested
        field_names = ('foo', 'bar')
        validator = CSVValidator(field_names)
        validator.add_value_check('foo', not_required_datatype(int),
                                  'foo', 'not an integer')
        validator.add_value_check('bar', not_required_datatype(float),
                                  'bar', 'not a float')
        summarize = False
        limit = 0
        # some test data
        problems = validator.validate(csvfile)
        """
            Write problems as restructured text to a file (or stdout/stderr).
            """
        #file = open('myfile.txt', 'w')
        file = cStringIO.StringIO()
        w = file.write  # convenience variable
        w("""
        =================
        Vecdyn Validation Report
        =================
        """)
        counts = dict()  # store problem counts per problem code
        total = 0
        for i, p in enumerate(problems):
            if limit and i >= limit:
                break  # bail out
            if total == 0 and not summarize:
                w("""
        Problems
        ========
        """)
            total += 1
            code = p['code']
            if code in counts:
                counts[code] += 1
            else:
                counts[code] = 1
            if not summarize:
                ptitle = '\n%s - %s\n' % (p['code'], p['message'])
                w(ptitle)
                underline = ''
                for i in range(len(ptitle.strip())):
                    underline += '-'
                underline += '\n'
                w(underline)
                for k in sorted(p.viewkeys() - set(['code', 'message', 'context'])):
                    w(':%s: %s\n' % (k, p[k]))
                if 'context' in p:
                    c = p['context']
                    for k in sorted(c.viewkeys()):
                        w(':%s: %s\n' % (k, c[k]))

        w("""
        Summary
        =======
        Found %s%s problem%s in total.
        """ % ('at least ' if limit else '', total, 's' if total != 1 else ''))
        for code in sorted(counts.viewkeys()):
            w(':%s: %s\n' % (code, counts[code]))
        file.seek(0)  # <---
        return response.stream(file, attachment=True, filename='Vecdyn-Validation-Report.txt')
    return locals()




