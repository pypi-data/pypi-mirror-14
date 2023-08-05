# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02D111-1307, USA.

"""Query parser."""

import pypeg2
from elasticsearch.helpers import scan
from flask import current_app
from invenio_query_parser.walkers.match_unit import MatchUnit
from invenio_search import Query as SearchQuery
from invenio_search import current_search_client
from invenio_search.walkers.elasticsearch import ElasticSearchDSL
from werkzeug.utils import cached_property

from .utils import parser, query_walkers


class Query(SearchQuery):
    """Query object."""

    @cached_property
    def query(self):
        """Parse query string using given grammar."""
        tree = pypeg2.parse(self._query, parser(), whitespace='')
        for walker in query_walkers():
            tree = tree.accept(walker)
        return tree

    def match(self, record):
        """Return True if record match the query."""
        return self.query.accept(MatchUnit(record))


def get_affected_records(spec=None, search_pattern=None):
    """Get list of affected records."""
    # spec       pattern    query
    # ---------- ---------- -------
    # None       None       None
    # None       Y          Y
    # X          None       X
    # X          ''         X
    # X          Y          X OR Y

    if spec is None and search_pattern is None:
        raise StopIteration
    elif spec is None:
        query = search_pattern
    elif search_pattern is None or search_pattern == '':
        query = '_oai.sets:"{0}"'.format(spec)
    else:
        query = '_oai.sets:"{0}" OR {1}'.format(spec, search_pattern)

    body = {'query': Query(query).query.accept(ElasticSearchDSL())}

    response = scan(
        client=current_search_client,
        index=current_app.config['OAISERVER_RECORD_INDEX'],
        query=body,
    )

    for result in response:
        yield result['_id']


def get_records(**kwargs):
    """Get records."""
    page_ = kwargs.get('resumptionToken', {}).get('page', 1)
    size_ = current_app.config['OAISERVER_PAGE_SIZE']
    scroll = current_app.config['OAISERVER_RESUMPTION_TOKEN_EXPIRE_TIME']
    scroll_id = kwargs.get('resumptionToken', {}).get('scroll_id')

    if scroll_id is None:
        query = Query()

        body = {'must': [{'exists': {'field': '_oai.id'}}]}
        if 'set' in kwargs:
            body['must'].append({'match': {'_oai.sets': kwargs['set']}})

        time_range = {}
        if 'from_' in kwargs:
            time_range['gte'] = kwargs['from_']
        if 'until' in kwargs:
            time_range['lte'] = kwargs['until']
        if time_range:
            body['filter'] = [{'range': {'_oai.updated': time_range}}]

        if body:
            query.body = {'query': {'bool': body}}

        response = current_search_client.search(
            index=current_app.config['OAISERVER_RECORD_INDEX'],
            body=query.body,
            from_=(page_-1)*size_,
            size=size_,
            scroll='{0}s'.format(scroll),
            version=True,
        )
    else:
        response = current_search_client.scroll(
            scroll_id=scroll_id,
            scroll='{0}s'.format(scroll),
        )

    class Pagination(object):
        """Dummy pagination class."""

        page = page_
        per_page = size_

        def __init__(self, response):
            """Initilize pagination."""
            self.response = response
            self.total = response['hits']['total']
            self._scroll_id = response.get('_scroll_id')

            # clean descriptor on last page
            if not self.has_next:
                current_search_client.clear_scroll(
                    scroll_id=self._scroll_id
                )
                self._scroll_id = None

        @cached_property
        def has_next(self):
            """Return True if there is next page."""
            return self.page * self.per_page <= self.total

        @cached_property
        def next_num(self):
            """Return next page number."""
            return self.page + 1 if self.has_next else None

        @property
        def items(self):
            """Return iterator."""
            from datetime import datetime
            for result in self.response['hits']['hits']:
                if '_oai' in result['_source']:
                    yield {
                        'id': result['_id'],
                        'json': result,
                        'updated': datetime.strptime(
                            result['_source']['_oai']['updated'],
                            '%Y-%m-%dT%H:%M:%SZ'
                        ),
                    }

    return Pagination(response)
