#!/usr/bin/env python3
""" Defines `index_range` simple helper function """

import csv
import math
from typing import List


def index_range(page, page_size):
    """ Finds indices for a specific page knowing the page size """
    return (page - 1) * page_size, page * page_size


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """ Gets the page from `Popular_Baby_Names.csv` file """
        assert type(page) is int and type(page_size) is int
        assert page > 0 and page_size > 0
        indices = index_range(page, page_size)
        data = []
        with open('Popular_Baby_Names.csv', 'r') as csvFile:
            csv_reader = csv.reader(csvFile)
            i = -1
            for row in csv_reader:
                if indices[0] <= i < indices[1]:
                    data.append(row)
                i += 1
        return data
