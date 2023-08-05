# -*- coding: utf-8 -*-
from math import ceil
from watson.common import imports


def _table_attr(obj, attr):
    return '{}.{}'.format(obj.__tablename__, attr)


class Page(object):
    """A single page object that is returned from the paginator.

    Provides the ability to automatically generate a query string.
    """
    id = None
    query_string_key = 'page'
    __parts = None

    def __init__(self, id):
        self.id = id
        self._parts[self.query_string_key] = self.id

    @property
    def query_string(self):
        parts = ['{}={}'.format(key, value)
                 for key, value in self._parts.items()]
        return '?{}'.format('&amp;'.join(parts))

    def append(self, **kwargs):
        if 'page' in kwargs:
            del kwargs['page']
        self._parts.update(**kwargs)
        return self

    # internal
    @property
    def _parts(self):
        if not self.__parts:
            self.__parts = {}
        return self.__parts

    def __str__(self):
        return self.query_string


class Pagination(object):
    """Provides simple pagination for query results.

    Attributes:
        query (Query): The SQLAlchemy query to be paginated
        page (int): The page to be displayed
        limit (int): The maximum number of results to be displayed on a page
        total (int): The total number of results
        items (list): The items returned from the query

    Example:

    .. code-block:: python

        # within controller
        query = session.query(Model)
        paginator = Pagination(query, limit=50)

        # within view
        {% for item in paginator %}
        {% endfor %}
        <div class="pagination">
        {% for page in paginator.iter_pages() %}
            {% if page == paginator.page %}
            <a href="{{ page }}" class="current">{{ page.id }}</a>
            {% else %}
            <a href="{{ page }}">{{ page.id }}</a>
            {% endif %}
        {% endfor %}
        </div>
    """
    query = None
    page = None
    limit = None
    total = None
    items = None
    _cached_next = None
    _cached_previous = None

    def __init__(self, query, page=1, limit=20):
        """Initialize the paginator and set some default values.
        """
        self.query = query
        self.page = page
        self.limit = limit
        self.__prepare()

    @property
    def has_previous(self):
        """Return whether or not there are previous pages from the currently
        displayed page.

        Returns:
            boolean
        """
        return self.page > 1

    @property
    def previous(self):
        """Return the previous page object if the page exists.

        Returns:
            Page
        """
        if self.has_previous:
            previous_id = self.page - 1
            if self._cached_previous and self._cached_previous.id == previous_id:
                return self._cached_previous
            self._cached_previous = Page(previous_id)
            return self._cached_previous

    @property
    def has_next(self):
        """Return whether or not there are more pages from the currently
        displayed page.

        Returns:
            boolean
        """
        return self.page < self.pages

    @property
    def next(self):
        """Return the next page object if another page exists.

        Returns:
            Page
        """
        if self.has_next:
            next_id = self.page + 1
            if self._cached_next and self._cached_next.id == next_id:
                return self._cached_next
            self._cached_next = Page(next_id)
            return self._cached_next

    @property
    def pages(self):
        """The total amount of pages to be displayed based on the number of
        results and the limit being displayed.

        Returns:
            int
        """
        if not self.limit:
            return 0  # pragma: no cover
        else:
            return int(ceil(self.total / float(self.limit)))

    def iter_pages(self):
        """An iterable containing the number of pages to be displayed.

        Example:

        .. code-block:: python

            {% for page in paginator.iter_pages() %}{% endfor %}
        """
        for num in range(1, self.pages + 1):
            yield Page(num)

    # Internals

    def __bool__(self):
        return True if self.items else False

    def __iter__(self):
        for result in self.items:
            yield result

    def __prepare(self):
        self.items = self.query.limit(self.limit).offset(
            (self.page - 1) * self.limit).all()
        self.total = 1
        if not self.items and self.page != 1:
            self.total = 0
        if self.page == 1 and len(self.items) < self.limit:
            self.total = len(self.items)
        else:
            self.total = self.query.order_by(None).count()

    def __repr__(self):
        return '<{0} page:{1} limit:{2} total:{3} pages:{4}>'.format(
            imports.get_qualified_name(self),
            self.page, self.limit, self.total, self.pages)
