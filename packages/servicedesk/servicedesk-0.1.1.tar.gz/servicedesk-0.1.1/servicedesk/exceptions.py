#!/usr/bin/env python


class InvalidApiKeyError(Exception):
    pass


class InvalidTaskError(Exception):
    pass


class InvalidRequestFilterError(Exception):
    pass

if __name__ == "__main__":
    print("Do not run this script directly, it must be imported.")
