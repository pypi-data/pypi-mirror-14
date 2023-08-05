from __future__ import absolute_import


class Paginator(object):
    """The class for pagination.

    This class supports the following two keywords in query parameter:

    Keyword  | Default
    -------- | -------
    page     | 1
    per_page | 10

    You may want to specify `page` and `per_page` explicitly:

        /users?page=2&per_page=10
    """

    #: The number of items per page
    per_page = 10

    def get_args(self, query_params):
        PAGE = 1
        PER_PAGE = self.per_page

        try:
            page = int(query_params.pop('page', None))
            if page < 1:
                page = PAGE
        except Exception:
            page = PAGE

        try:
            per_page = int(query_params.pop('per_page', None))
            if per_page < 1:
                per_page = PER_PAGE
        except Exception:
            per_page = PER_PAGE

        return page, per_page

    def make_headers(self, uri, page, per_page, count):
        """Make GitHub-style pagination headers."""
        headers = {}

        div, mod = divmod(count, per_page)
        page_count = div + int(mod > 0)

        links = []

        def add_link(page, per_page, rel):
            args = (uri, page, per_page, rel)
            links.append('<%s?page=%s&per_page=%s>; rel="%s"' % args)

        def add_prev_link():
            add_link(page - 1, per_page, 'prev')

        def add_next_link():
            add_link(page + 1, per_page, 'next')

        def add_first_link():
            add_link(1, per_page, 'first')

        def add_last_link():
            add_link(page_count, per_page, 'last')

        # fill `Link` headers
        if page_count > 0 and page != page_count:
            if page == 1:
                add_next_link()
                add_last_link()
            elif page < page_count:
                add_prev_link()
                add_next_link()
                add_first_link()
                add_last_link()
            elif page == page_count:
                add_prev_link()
                add_first_link()
            else:
                add_link(page_count, per_page, 'prev')
                add_first_link()
                add_last_link()

            headers.update({'Link': ', '.join(links)})

        # fill `X-Pagination-Info` headers
        args = (page, per_page, count)
        headers.update({
            'X-Pagination-Info': 'page=%s, per-page=%s, count=%s' % args
        })

        return headers
