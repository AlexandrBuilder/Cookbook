def pagination(page, per_page):
    limit = per_page
    offset = limit * (page - 1)
    return offset, limit
