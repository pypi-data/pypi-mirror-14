#!/usr/bin/env python

import collections

# Create a namedtuple that will be used to pass the results of a SD API call
# around our helper object.
API_Result = collections.namedtuple(
    'API_Results', ['status', 'message', 'data'])

if __name__ == "__main__":
    print("Do not run this script directly, it must be imported.")
