from flask import request

DEFAULT_PAGE_INDEX = 1
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

def get_pagination_data():
    page_index = request.args.get("page", DEFAULT_PAGE_INDEX, type=int)
    page_size = min(request.args.get("page_size", DEFAULT_PAGE_SIZE, type=int), MAX_PAGE_SIZE)

    return page_index, page_size
