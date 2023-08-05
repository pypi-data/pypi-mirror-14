#!/usr/bin/env python2.7

'''Tests utils module for ease of running & integrating test results.
   Execute this function instead of the standard ut.main(), eg:
        run_tests(TestTimeutils)
'''

import unittest as ut

# ------------------------------------------------------------ #
def twrap(func):
    """Decorator for test functions to print out what test is being run"""
    def inner(*args):
        print "\n-- RUNNING TEST: <{}> --\n".format(func.__name__)
        return func(*args)
    return inner


# ------------------------------------------------------------ #
def run_tests(test_case):
    loader = ut.TestLoader().loadTestsFromTestCase(test_case)
    result = ut.TestResult()
    loader(result)
    print "=" * 60
    print "TEST RESULTS FOR", test_case.__name__

    print "*FAILURES*"
    print "-" * 60

    for t, f in result.failures:
        print "->", t, "<-"
        print f
    for t, e in result.errors:
        print "->", t, "<-"
        print e

    print "*ERRORS*"
    print "-" * 60

    tcount = result.testsRun
    fcount = len(result.failures)
    ecount = len(result.errors)
    pcount = tcount - fcount - ecount
    prate = round( 100.0* pcount/float(tcount), 2)

    summary = {}
    summary['Name'       ] = test_case.__name__
    summary['Pass'       ] = pcount
    summary['Failures'   ] = fcount
    summary['Errors'     ] = ecount
    summary['Total'      ] = tcount
    summary['Pass rate'  ] = prate

    # if result.wasSuccessful():    # relegate this to print_summary()
    print_summary(summary)

    return summary, result


# ------------------------------------------------------------ #
def append_summary(master, summary):
    if not master:
        master = summary.copy()
        master['Name'] = 'ALL TESTS'
        master['Sublist'] = [summary.copy()]     # store list of all test summaries
        return master

    for k in master.keys():
        if k == 'Sublist':
            master['Sublist'].append(summary.copy())
        else:
            master[k] += summary[k]

    if not master.has_key('Sublist'):
        master['Sublist'] = [summary.copy()]     # store list of all test summaries

    master['Pass rate'] = round( 100.0* master['Pass']/float(master['Total']), 2)
    master['Name'] = 'ALL TESTS'

    return master


# ------------------------------------------------------------ #
def print_breakdown(slist):
    """Prints breakdown of other tests in slist in shortened form"""
    print '   Name', ' '*20, 'Pass/Total  Fail Error PassRate '
    for s in slist: # slist is list of dict()s
        n = s['Name']
        p = s['Pass']
        f = s['Failures']
        e = s['Errors']
        t = s['Total']
        pr = str(s['Pass rate']) + '%'

        spc = ' '*(24 - len(n))
        print '   %s %s    %03d/%03d   %03d   %03d   %s ' % (n, spc, p, t, f, e, pr)


# ------------------------------------------------------------ #
def print_summary(summary, title=None):
    print
    if summary == {}:
        print "   WARNING. No tests available for {}".format(title)
        print "-" * 60
        return

    if title==None:
        title = "SUMMARY FOR '%s'" % (summary['Name'])

    print "*%s*" % (title)
    print "-" * 60


    if summary.has_key('Sublist'):
        print_breakdown(summary['Sublist'])

    print "-" * 60
    print "    Name       :", summary['Name']
    print "    Pass       :", summary['Pass']
    print "    Failures   :", summary['Failures']
    print "    Errors     :", summary['Errors']
    print "    Total count:", summary['Total']
    print "    Pass rate  :", str(summary['Pass rate']) + '%'
    print "-" * 60

    print
    s = summary
    if summary['Pass'] == summary['Total']:
        print "All tests ran without problems :)"
    else:
        print s['Pass'], "out of", s['Total'], "tests ran without problems. There were", s['Errors']+s['Failures'], "fails or errors"
    print
    print "=" * 60
