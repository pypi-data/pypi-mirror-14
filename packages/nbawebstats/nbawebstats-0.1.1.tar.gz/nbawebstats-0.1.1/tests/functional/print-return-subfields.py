#!/usr/bin/env python

import sys
import pickle

def print_request(rname, rdata):
    print(rname)
    try:
        for fname, fdata in rdata['response'].items():
            print("    " + fname + ":")
            if fdata:
                for subfield in fdata[0]:
                    print("        " + subfield)
    except:
        pass


if __name__ == "__main__":
    with open('test-results.pickle', 'rb') as f:
        a = pickle.load(f)

    if len(sys.argv) == 2:
        rname = sys.argv[1]
        print_request(rname, a[rname])
    elif len(sys.argv) > 2:
        for rname in sys.argv[1:]:
            print("")
            print_request(rname, a[rname])
    else:
        for rname, rdata in sorted(list(a.items())):
            print("")
            print_request(rname, rdata)
