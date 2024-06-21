#!/usr/bin/env python3
""" Defines `index_range` simple helper function """


def index_range(page, page_size):
    """ Finds indices for a specific page knowing the page size """
    return (page - 1) * page_size, page * page_size
