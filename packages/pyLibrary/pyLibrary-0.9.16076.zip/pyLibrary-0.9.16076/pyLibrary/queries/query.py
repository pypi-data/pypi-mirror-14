# encoding: utf-8
#
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Author: Kyle Lahnakoski (kyle@lahnakoski.com)
#
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from collections import Mapping

from pyLibrary.collections import AND
from pyLibrary.debugs.logs import Log
from pyLibrary.dot import coalesce, Null
from pyLibrary.dot import wrap, unwrap, listwrap
from pyLibrary.dot.dicts import Dict
from pyLibrary.dot.lists import DictList
from pyLibrary.maths import Math
from pyLibrary.queries import wrap_from, Schema
from pyLibrary.queries.containers import Container
from pyLibrary.queries.dimensions import Dimension
from pyLibrary.queries.domains import Domain, is_keyword
from pyLibrary.queries.expressions import TRUE_FILTER, simplify_esfilter, query_get_all_vars, jx_expression, TrueOp

DEFAULT_LIMIT = 10
MAX_LIMIT = 50000

_jx = None
_Column = None


def _late_import():
    global _jx
    global _Column

    from pyLibrary.queries.meta import Column as _Column
    from pyLibrary.queries import jx as _jx

    _ = _jx
    _ = _Column


class Query(object):
    __slots__ = ["frum", "select", "edges", "groupby", "where", "window", "sort", "limit", "having", "format", "isLean"]

    def __new__(cls, query, schema=None):
        if isinstance(query, Query):
            return query
        output = object.__new__(cls)
        for s in Query.__slots__:
            setattr(output, s, None)
        return output

    def __init__(self, query, schema=None):
        """
        NORMALIZE QUERY SO IT CAN STILL BE JSON
        """
        if isinstance(query, Query) or query == None:
            return

        object.__init__(self)
        query = wrap(query)

        self.format = query.format
        self.frum = wrap_from(query["from"], schema=schema)
        if not schema and isinstance(self.frum, Schema):
            schema = self.frum

        select = query.select
        if isinstance(select, list):
            names = set()
            new_select = []
            for s in select:
                ns = _normalize_select(s, schema=schema)
                if ns.name in names:
                    Log.error("two select have the same name")
                names.add(ns.name)
                new_select.append(unwrap(ns))
            self.select = wrap(new_select)
        elif select:
            self.select = _normalize_select(select, schema=schema)
        else:
            if query.edges or query.groupby:
                self.select = Dict(name="count", value=".", aggregate="count", default=0)
            else:
                self.select = Dict(name=".", value=".", aggregate="none")

        if query.groupby and query.edges:
            Log.error("You can not use both the `groupby` and `edges` clauses in the same query!")
        elif query.edges:
            self.edges = _normalize_edges(query.edges, schema=schema)
            self.groupby = None
        elif query.groupby:
            self.edges = None
            self.groupby = _normalize_groupby(query.groupby, schema=schema)
        else:
            self.edges = []
            self.groupby = None

        self.where = _normalize_where(query.where, schema=schema)
        self.window = [_normalize_window(w) for w in listwrap(query.window)]
        self.having = None
        self.sort = _normalize_sort(query.sort)
        self.limit = Math.min(MAX_LIMIT, coalesce(query.limit, DEFAULT_LIMIT))
        if not Math.is_integer(self.limit) or self.limit < 0:
            Log.error("Expecting limit >= 0")

        self.isLean = query.isLean


        # DEPTH ANALYSIS - LOOK FOR COLUMN REFERENCES THAT MAY BE DEEPER THAN
        # THE from SOURCE IS.
        # TODO: IGNORE REACHING INTO THE NON-NESTED TYPES
        if isinstance(self.frum, list):
            if not _jx:
                _late_import()
            columns = _jx.get_columns(self.frum)
        elif isinstance(self.frum, Container):
            try:
                columns = self.frum.get_columns(table_name=self.frum.name)
            except Exception, e:
                Log.error("Problem", cause=e)
        else:
            columns = []

        if self.edges or self.groupby:
            query_path = coalesce(self.frum.query_path, ".")
            vars = query_get_all_vars(self, exclude_where=True)  # WE WILL EXCLUDE where VARIABLES
            for c in columns:
                if c.name in vars and not query_path.startswith(coalesce(listwrap(c.nested_path)[0], "")):
                    Log.error("This query, with variable {{var_name}} is too deep", var_name=c.name)

    @property
    def columns(self):
        return listwrap(self.select) + coalesce(self.edges, self.groupby)

    @property
    def query_path(self):
        return "."

    def __getitem__(self, item):
        if item == "from":
            return self.frum
        return Dict.__getitem__(self, item)

    def copy(self):
        output = object.__new__(Query)
        for s in Query.__slots__:
            setattr(output, s, getattr(self, s))
        return output

    def as_dict(self):
        output = wrap({s: getattr(self, s) for s in Query.__slots__})
        return output


canonical_aggregates = wrap({
    "count": {"name": "count", "default": 0},
    "min": {"name": "minimum"},
    "max": {"name": "maximum"},
    "add": {"name": "sum"},
    "avg": {"name": "average"},
    "mean": {"name": "average"},
})


def _normalize_selects(selects, schema=None):
    if isinstance(selects, list):
        output = wrap([_normalize_select(s, schema=schema) for s in selects])

        exists = set()
        for s in output:
            if s.name in exists:
                Log.error("{{name}} has already been defined",  name= s.name)
            exists.add(s.name)
        return output
    else:
        return _normalize_select(selects, schema=schema)


def _normalize_select(select, schema=None):
    if not _Column:
        _late_import()

    if isinstance(select, basestring):
        select = select.rstrip(".")
        if not select:
            return Dict(
                name=".",
                value="*",
                aggregate="none"
            )
        if select == "*":
            return Dict(
                name=".",
                value="*",
                aggregate="none"
            )

        if schema:
            s = schema.get_column(select)
            if s:
                if isinstance(s, _Column):
                    return Dict(
                        name=select,
                        value=select,
                        aggregate="none"
                    )
                else:
                    #EXPECTING DIMENSION
                    return s.getSelect()

        if select.endswith(".*"):
            name = select[:-2]
        else:
            name = select

        return Dict(
            name=name,
            value=select,
            aggregate="none"
        )
    else:
        select = wrap(select)
        output = select.copy()
        if not select.value:
            output.value = "."
            output.name = coalesce(select.name, select.aggregate)
        elif isinstance(select.value, basestring):
            if select.value == ".":
                output.name = coalesce(select.name, select.aggregate)
            else:
                output.name = coalesce(select.name, select.value, select.aggregate)
        elif not output.name:
            Log.error("Must give name to each column in select clause")

        if not output.name:
            Log.error("expecting select to have a name: {{select}}",  select= select)
        if output.name.endswith(".*"):
            output.name = output.name[:-2]

        output.aggregate = coalesce(canonical_aggregates[select.aggregate].name, select.aggregate, "none")
        output.default = coalesce(select.default, canonical_aggregates[output.aggregate].default)
        return output



def _normalize_edges(edges, schema=None):
    return [_normalize_edge(e, schema=schema) for e in listwrap(edges)]


def _normalize_edge(edge, schema=None):
    if not _Column:
        _late_import()

    if isinstance(edge, basestring):
        if schema:
            e = schema[edge]
            if e:
                if isinstance(e, _Column):
                    return Dict(
                        name=edge,
                        value=edge,
                        allowNulls=True,
                        domain=_normalize_domain(schema=schema)
                    )
                elif isinstance(e.fields, list) and len(e.fields) == 1:
                    return Dict(
                        name=e.name,
                        value=e.fields[0],
                        allowNulls=True,
                        domain=e.getDomain()
                    )
                else:
                    return Dict(
                        name=e.name,
                        allowNulls=True,
                        domain=e.getDomain()
                    )
        return Dict(
            name=edge,
            value=edge,
            allowNulls=True,
            domain=_normalize_domain(schema=schema)
        )
    else:
        edge = wrap(edge)
        if not edge.name and not isinstance(edge.value, basestring):
            Log.error("You must name compound edges: {{edge}}", edge=edge)

        if isinstance(edge.value, (list, set)) and not edge.domain:
            # COMPLEX EDGE IS SHORT HAND
            domain = _normalize_domain(schema=schema)
            domain.dimension = Dict(fields=edge.value)

            return Dict(
                name=edge.name,
                allowNulls=bool(coalesce(edge.allowNulls, True)),
                domain=domain
            )

        domain = _normalize_domain(edge.domain, schema=schema)
        return Dict(
            name=coalesce(edge.name, edge.value),
            value=edge.value,
            range=edge.range,
            allowNulls=bool(coalesce(edge.allowNulls, True)),
            domain=domain
        )


def _normalize_groupby(groupby, schema=None):
    if groupby == None:
        return None
    return [_normalize_group(e, schema=schema) for e in listwrap(groupby)]


def _normalize_group(edge, schema=None):
    if isinstance(edge, basestring):
        return wrap({
            "name": edge,
            "value": edge,
            "allowNulls": True,
            "domain": {"type": "default"}
        })
    else:
        edge = wrap(edge)
        if (edge.domain and edge.domain.type != "default") or edge.allowNulls != None:
            Log.error("groupby does not accept complicated domains")

        if not edge.name and not isinstance(edge.value, basestring):
            Log.error("You must name compound edges: {{edge}}",  edge= edge)

        return wrap({
            "name": coalesce(edge.name, edge.value),
            "value": edge.value,
            "allowNulls": True,
            "domain": {"type": "default"}
        })


def _normalize_domain(domain=None, schema=None):
    if not domain:
        return Domain(type="default")
    elif isinstance(domain, Dimension):
        return domain.getDomain()
    elif schema and isinstance(domain, basestring) and schema[domain]:
        return schema[domain].getDomain()
    elif isinstance(domain, Domain):
        return domain

    if not domain.name:
        domain = domain.copy()
        domain.name = domain.type

    domain.partitions = listwrap(domain.partitions)

    return Domain(**domain)


def _normalize_window(window, schema=None):
    return Dict(
        name=coalesce(window.name, window.value),
        value=window.value,
        edges=[_normalize_edge(e, schema) for e in listwrap(window.edges)],
        sort=_normalize_sort(window.sort),
        aggregate=window.aggregate,
        range=_normalize_range(window.range),
        where=_normalize_where(window.where, schema=schema)
    )


def _normalize_range(range):
    if range == None:
        return None

    return Dict(
        min=range.min,
        max=range.max
    )


def _normalize_where(where, schema=None):
    if where == None:
        return TrueOp()
    return jx_expression(where)


def _map_term_using_schema(master, path, term, schema_edges):
    """
    IF THE WHERE CLAUSE REFERS TO FIELDS IN THE SCHEMA, THEN EXPAND THEM
    """
    output = DictList()
    for k, v in term.items():
        dimension = schema_edges[k]
        if isinstance(dimension, Dimension):
            domain = dimension.getDomain()
            if dimension.fields:
                if isinstance(dimension.fields, Mapping):
                    # EXPECTING A TUPLE
                    for local_field, es_field in dimension.fields.items():
                        local_value = v[local_field]
                        if local_value == None:
                            output.append({"missing": {"field": es_field}})
                        else:
                            output.append({"term": {es_field: local_value}})
                    continue

                if len(dimension.fields) == 1 and is_keyword(dimension.fields[0]):
                    # SIMPLE SINGLE-VALUED FIELD
                    if domain.getPartByKey(v) is domain.NULL:
                        output.append({"missing": {"field": dimension.fields[0]}})
                    else:
                        output.append({"term": {dimension.fields[0]: v}})
                    continue

                if AND(is_keyword(f) for f in dimension.fields):
                    # EXPECTING A TUPLE
                    if not isinstance(v, tuple):
                        Log.error("expecing {{name}}={{value}} to be a tuple",  name= k,  value= v)
                    for i, f in enumerate(dimension.fields):
                        vv = v[i]
                        if vv == None:
                            output.append({"missing": {"field": f}})
                        else:
                            output.append({"term": {f: vv}})
                    continue
            if len(dimension.fields) == 1 and is_keyword(dimension.fields[0]):
                if domain.getPartByKey(v) is domain.NULL:
                    output.append({"missing": {"field": dimension.fields[0]}})
                else:
                    output.append({"term": {dimension.fields[0]: v}})
                continue
            if domain.partitions:
                part = domain.getPartByKey(v)
                if part is domain.NULL or not part.esfilter:
                    Log.error("not expected to get NULL")
                output.append(part.esfilter)
                continue
            else:
                Log.error("not expected")
        elif isinstance(v, Mapping):
            sub = _map_term_using_schema(master, path + [k], v, schema_edges[k])
            output.append(sub)
            continue

        output.append({"term": {k: v}})
    return {"and": output}


# def _move_nested_term(master, where, schema):
#     """
#     THE WHERE CLAUSE CAN CONTAIN NESTED PROPERTY REFERENCES, THESE MUST BE MOVED
#     TO A NESTED FILTER
#     """
#     items = where.term.items()
#     if len(items) != 1:
#         Log.error("Expecting only one term")
#     k, v = items[0]
#     nested_path = _get_nested_path(k, schema)
#     if nested_path:
#         return {"nested": {
#             "path": nested_path,
#             "query": {"filtered": {
#                 "query": {"match_all": {}},
#                 "filter": {"and": [
#                     {"term": {k: v}}
#                 ]}
#             }}
#         }}
#     return where


# def _get_nested_path(field, schema):
#     if is_keyword(field):
#         field = join_field([schema.es.alias] + split_field(field))
#         for i, f in reverse(enumerate(split_field(field))):
#             path = join_field(split_field(field)[0:i + 1:])
#             if path in INDEX_CACHE:
#                 return unwraplist(join_field(split_field(path)[1::]))
#     return None
#

def _where_terms(master, where, schema):
    """
    USE THE SCHEMA TO CONVERT DIMENSION NAMES TO ES FILTERS
    master - TOP LEVEL WHERE (FOR PLACING NESTED FILTERS)
    """
    if isinstance(where, Mapping):
        if where.term:
            # MAP TERM
            try:
                output = _map_term_using_schema(master, [], where.term, schema.edges)
                return output
            except Exception, e:
                Log.error("programmer problem?", e)
        elif where.terms:
            # MAP TERM
            output = DictList()
            for k, v in where.terms.items():
                if not isinstance(v, (list, set)):
                    Log.error("terms filter expects list of values")
                edge = schema.edges[k]
                if not edge:
                    output.append({"terms": {k: v}})
                else:
                    if isinstance(edge, basestring):
                        # DIRECT FIELD REFERENCE
                        return {"terms": {edge: v}}
                    try:
                        domain = edge.getDomain()
                    except Exception, e:
                        Log.error("programmer error", e)
                    fields = domain.dimension.fields
                    if isinstance(fields, Mapping):
                        or_agg = []
                        for vv in v:
                            and_agg = []
                            for local_field, es_field in fields.items():
                                vvv = vv[local_field]
                                if vvv != None:
                                    and_agg.append({"term": {es_field: vvv}})
                            or_agg.append({"and": and_agg})
                        output.append({"or": or_agg})
                    elif isinstance(fields, list) and len(fields) == 1 and is_keyword(fields[0]):
                        output.append({"terms": {fields[0]: v}})
                    elif domain.partitions:
                        output.append({"or": [domain.getPartByKey(vv).esfilter for vv in v]})
            return {"and": output}
        elif where["or"]:
            return {"or": [unwrap(_where_terms(master, vv, schema)) for vv in where["or"]]}
        elif where["and"]:
            return {"and": [unwrap(_where_terms(master, vv, schema)) for vv in where["and"]]}
        elif where["not"]:
            return {"not": unwrap(_where_terms(master, where["not"], schema))}
    return where


def _normalize_sort(sort=None):
    """
    CONVERT SORT PARAMETERS TO A NORMAL FORM SO EASIER TO USE
    """

    if not sort:
        return DictList.EMPTY

    output = DictList()
    for s in listwrap(sort):
        if isinstance(s, basestring) or Math.is_integer(s):
            output.append({"value": s, "sort": 1})
        elif list(set(s.values()))[0] == "desc" and not s.sort and not s.value:
            for v, d in s.items():
                output.append({"value": v, "sort": -1})
        else:
            output.append({"value": coalesce(s.value, s.field), "sort": coalesce(sort_direction[s.sort], 1)})
    return wrap(output)


sort_direction = {
    "asc": 1,
    "desc": -1,
    "none": 0,
    1: 1,
    0: 0,
    -1: -1,
    None: 1,
    Null: 1
}

