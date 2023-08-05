from copy import deepcopy, copy
from collections import namedtuple
from datetime import timedelta, datetime
import json
import logging
from six import string_types
import sqlparse
import requests

from dateutil.parser import parse
from flask import flash
from flask.ext.appbuilder import Model
from flask.ext.appbuilder.models.mixins import AuditMixin
import pandas as pd
from pydruid import client
from pydruid.utils.filters import Dimension, Filter

import sqlalchemy as sqla
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Text, Boolean, DateTime,
    Table, create_engine, MetaData, desc, select, and_, func)
from sqlalchemy.engine import reflection
from sqlalchemy.orm import relationship
from sqlalchemy.sql import table, literal_column, text, column
from sqlalchemy.sql.elements import ColumnClause
from sqlalchemy_utils import EncryptedType

from panoramix import app, db, get_session, utils
from panoramix.viz import viz_types
from sqlalchemy.ext.declarative import declared_attr

config = app.config

QueryResult = namedtuple('namedtuple', ['df', 'query', 'duration'])


class AuditMixinNullable(AuditMixin):
    @declared_attr
    def created_by_fk(cls):
        return Column(Integer, ForeignKey('ab_user.id'),
                      default=cls.get_user_id, nullable=True)
    @declared_attr
    def changed_by_fk(cls):
        return Column(Integer, ForeignKey('ab_user.id'),
            default=cls.get_user_id, onupdate=cls.get_user_id, nullable=True)
    @property
    def created_by_(self):
        return '{}'.format(self.created_by or '')
    @property
    def changed_by_(self):
        return '{}'.format(self.changed_by or '')


class Url(Model, AuditMixinNullable):
    """Used for the short url feature"""
    __tablename__ = 'url'
    id = Column(Integer, primary_key=True)
    url = Column(Text)


class CssTemplate(Model, AuditMixinNullable):
    """CSS templates for dashboards"""
    __tablename__ = 'css_templates'
    id = Column(Integer, primary_key=True)
    template_name = Column(String(250))
    css = Column(Text, default='')


class Slice(Model, AuditMixinNullable):
    """A slice is essentially a report or a view on data"""
    __tablename__ = 'slices'
    id = Column(Integer, primary_key=True)
    slice_name = Column(String(250))
    druid_datasource_id = Column(Integer, ForeignKey('datasources.id'))
    table_id = Column(Integer, ForeignKey('tables.id'))
    datasource_type = Column(String(200))
    datasource_name = Column(String(2000))
    viz_type = Column(String(250))
    params = Column(Text)
    description = Column(Text)

    table = relationship(
        'SqlaTable', foreign_keys=[table_id], backref='slices')
    druid_datasource = relationship(
        'DruidDatasource', foreign_keys=[druid_datasource_id], backref='slices')

    def __repr__(self):
        return self.slice_name

    @property
    def datasource(self):
        return self.table or self.druid_datasource

    @property
    def datasource_link(self):
        if self.table:
            return self.table.link
        elif self.druid_datasource:
            return self.druid_datasource.link

    @property
    @utils.memoized
    def viz(self):
        d = json.loads(self.params)
        viz = viz_types[self.viz_type](
            self.datasource,
            form_data=d)
        return viz

    @property
    def description_markeddown(self):
        return utils.markdown(self.description)

    @property
    def datasource_id(self):
        return self.table_id or self.druid_datasource_id

    @property
    def data(self):
        d = self.viz.data
        d['slice_id'] = self.id
        return d

    @property
    def json_data(self):
        return json.dumps(self.data)

    @property
    def slice_url(self):
        try:
            slice_params = json.loads(self.params)
        except Exception as e:
            logging.exception(e)
            slice_params = {}
        slice_params['slice_id'] = self.id
        slice_params['slice_name'] = self.slice_name
        from werkzeug.urls import Href
        href = Href(
            "/panoramix/explore/{self.datasource_type}/"
            "{self.datasource_id}/".format(self=self))
        return href(slice_params)

    @property
    def edit_url(self):
        return "/slicemodelview/edit/{}".format(self.id)

    @property
    def slice_link(self):
        url = self.slice_url
        return '<a href="{url}">{self.slice_name}</a>'.format(
            url=url, self=self)

    @property
    def js_files(self):
        return viz_types[self.viz_type].js_files

    @property
    def css_files(self):
        return viz_types[self.viz_type].css_files

    def get_viz(self):
        pass


dashboard_slices = Table('dashboard_slices', Model.metadata,
    Column('id', Integer, primary_key=True),
    Column('dashboard_id', Integer, ForeignKey('dashboards.id')),
    Column('slice_id', Integer, ForeignKey('slices.id')),
)


class Dashboard(Model, AuditMixinNullable):
    """A dash to slash"""
    __tablename__ = 'dashboards'
    id = Column(Integer, primary_key=True)
    dashboard_title = Column(String(500))
    position_json = Column(Text)
    description = Column(Text)
    css = Column(Text)
    json_metadata = Column(Text)
    slug = Column(String(255), unique=True)
    slices = relationship(
        'Slice', secondary=dashboard_slices, backref='dashboards')

    def __repr__(self):
        return self.dashboard_title

    @property
    def url(self):
        return "/panoramix/dashboard/{}/".format(self.slug or self.id)

    @property
    def metadata_dejson(self):
        if self.json_metadata:
            return json.loads(self.json_metadata)
        else:
            return {}

    def dashboard_link(self):
        return '<a href="{self.url}">{self.dashboard_title}</a>'.format(self=self)

    @property
    def js_files(self):
        l = []
        for o in self.slices:
            l += [f for f in o.js_files if f not in l]
        return l

    @property
    def css_files(self):
        l = []
        for o in self.slices:
            l += o.css_files
        return list(set(l))

    @property
    def json_data(self):
        d = {
            'id': self.id,
            'metadata': self.metadata_dejson,
            'dashboard_title': self.dashboard_title,
            'slug': self.slug,
            'slices': [slc.data for slc in self.slices],
        }
        return json.dumps(d)


class Queryable(object):
    @property
    def column_names(self):
        return sorted([c.column_name for c in self.columns])

    @property
    def main_dttm_col(self):
        return "timestamp"

    @property
    def groupby_column_names(self):
        return sorted([c.column_name for c in self.columns if c.groupby])

    @property
    def filterable_column_names(self):
        return sorted([c.column_name for c in self.columns if c.filterable])

    @property
    def dttm_cols(self):
        return []


class Database(Model, AuditMixinNullable):
    __tablename__ = 'dbs'
    id = Column(Integer, primary_key=True)
    database_name = Column(String(250), unique=True)
    sqlalchemy_uri = Column(String(1024))
    password = Column(EncryptedType(String(1024), config.get('SECRET_KEY')))

    def __repr__(self):
        return self.database_name

    def get_sqla_engine(self):
        return create_engine(self.sqlalchemy_uri_decrypted)

    def safe_sqlalchemy_uri(self):
        return self.sqlalchemy_uri

    def get_table(self, table_name):
        meta = MetaData()
        return Table(
            table_name, meta,
            autoload=True,
            autoload_with=self.get_sqla_engine())

    def get_columns(self, table_name):
        engine = self.get_sqla_engine()
        insp = reflection.Inspector.from_engine(engine)
        return insp.get_columns(table_name)

    @property
    def sqlalchemy_uri_decrypted(self):
        conn = sqla.engine.url.make_url(self.sqlalchemy_uri)
        conn.password = self.password
        return str(conn)

    @property
    def sql_url(self):
        return '/panoramix/sql/{}/'.format(self.id)

    @property
    def sql_link(self):
        return '<a href="{}">SQL</a>'.format(self.sql_url)


class SqlaTable(Model, Queryable, AuditMixinNullable):
    type = "table"

    __tablename__ = 'tables'
    id = Column(Integer, primary_key=True)
    table_name = Column(String(250), unique=True)
    main_dttm_col = Column(String(250))
    description = Column(Text)
    default_endpoint = Column(Text)
    database_id = Column(Integer, ForeignKey('dbs.id'), nullable=False)
    is_featured = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('ab_user.id'))
    owner = relationship('User', backref='tables', foreign_keys=[user_id])
    database = relationship(
        'Database', backref='tables', foreign_keys=[database_id])
    offset = Column(Integer, default=0)

    baselink = "tablemodelview"

    def __repr__(self):
        return self.table_name

    @property
    def description_markeddown(self):
        return utils.markdown(self.description)

    @property
    def url(self):
        return '/tablemodelview/edit/{}'.format(self.id)

    @property
    def link(self):
        return '<a href="{self.url}">{self.table_name}</a>'.format(**locals())

    @property
    def perm(self):
        return (
            "[{self.database}].[{self.table_name}]"
            "(id:{self.id})").format(self=self)

    @property
    def full_name(self):
        return "[{self.database}].[{self.table_name}]".format(self=self)

    @property
    def dttm_cols(self):
        l = [c.column_name for c in self.columns if c.is_dttm]
        if self.main_dttm_col not in l:
            l.append(self.main_dttm_col)
        return l

    @property
    def html(self):
        t = ((c.column_name, c.type) for c in self.columns)
        df = pd.DataFrame(t)
        df.columns = ['field', 'type']
        return df.to_html(
            index=False,
            classes=(
                "dataframe table table-striped table-bordered "
                "table-condensed"))

    @property
    def name(self):
        return self.table_name

    @property
    def table_link(self):
        url = "/panoramix/explore/{self.type}/{self.id}/".format(self=self)
        return '<a href="{url}">{self.table_name}</a>'.format(
            url=url, self=self)

    @property
    def metrics_combo(self):
        return sorted(
            [
                (m.metric_name, m.verbose_name or m.metric_name)
                for m in self.metrics],
            key=lambda x: x[1])

    @property
    def sql_url(self):
        return self.database.sql_url + "?table_name=" + str(self.table_name)

    @property
    def sql_link(self):
        return '<a href="{}">SQL</a>'.format(self.sql_url)

    def query(
            self, groupby, metrics,
            granularity,
            from_dttm, to_dttm,
            limit_spec=None,
            filter=None,
            is_timeseries=True,
            timeseries_limit=15, row_limit=None,
            inner_from_dttm=None, inner_to_dttm=None,
            extras=None,
            columns=None):

        # For backward compatibility
        if granularity not in self.dttm_cols:
            granularity = self.main_dttm_col

        cols = {col.column_name: col for col in self.columns}
        qry_start_dttm = datetime.now()
        if not self.main_dttm_col:
            raise Exception(
                "Datetime column not provided as part table configuration")
        dttm_expr = cols[granularity].expression
        if dttm_expr:
            timestamp = literal_column(dttm_expr).label('timestamp')
        else:
            timestamp = literal_column(granularity).label('timestamp')
        metrics_exprs = [
            literal_column(m.expression).label(m.metric_name)
            for m in self.metrics if m.metric_name in metrics]

        if metrics:
            main_metric_expr = literal_column([
                m.expression for m in self.metrics
                if m.metric_name == metrics[0]][0])
        else:
            main_metric_expr = literal_column("COUNT(*)")

        select_exprs = []
        groupby_exprs = []

        if groupby:
            select_exprs = []
            inner_select_exprs = []
            inner_groupby_exprs = []
            for s in groupby:
                col = cols[s]
                expr = col.expression
                if expr:
                    outer = literal_column(expr).label(s)
                    inner = literal_column(expr).label('__' + s)
                else:
                    outer = column(s).label(s)
                    inner = column(s).label('__' + s)

                groupby_exprs.append(outer)
                select_exprs.append(outer)
                inner_groupby_exprs.append(inner)
                inner_select_exprs.append(inner)
        elif columns:
            for s in columns:
                select_exprs.append(s)
            metrics_exprs = []

        if is_timeseries:
            select_exprs += [timestamp]
            groupby_exprs += [timestamp]

        select_exprs += metrics_exprs
        qry = select(select_exprs)
        from_clause = table(self.table_name)
        if not columns:
            qry = qry.group_by(*groupby_exprs)

        tf = '%Y-%m-%d %H:%M:%S.%f'
        time_filter = [
            timestamp >= from_dttm.strftime(tf),
            timestamp <= to_dttm.strftime(tf),
        ]
        inner_time_filter = copy(time_filter)
        if inner_from_dttm:
            inner_time_filter[0] = timestamp >= inner_from_dttm.strftime(tf)
        if inner_to_dttm:
            inner_time_filter[1] = timestamp <= inner_to_dttm.strftime(tf)
        where_clause_and = []
        having_clause_and = []
        for col, op, eq in filter:
            col_obj = cols[col]
            if op in ('in', 'not in'):
                values = eq.split(",")
                if col_obj.expression:
                    cond = ColumnClause(
                        col_obj.expression, is_literal=True).in_(values)
                else:
                    cond = column(col).in_(values)
                if op == 'not in':
                    cond = ~cond
                where_clause_and.append(cond)
        if extras and 'where' in extras:
            where_clause_and += [text(extras['where'])]
        if extras and 'having' in extras:
            having_clause_and += [text(extras['having'])]
        qry = qry.where(and_(*(time_filter + where_clause_and)))
        qry = qry.having(and_(*having_clause_and))
        if groupby:
            qry = qry.order_by(desc(main_metric_expr))
        qry = qry.limit(row_limit)

        if timeseries_limit and groupby:
            subq = select(inner_select_exprs)
            subq = subq.select_from(table(self.table_name))
            subq = subq.where(and_(*(where_clause_and + inner_time_filter)))
            subq = subq.group_by(*inner_groupby_exprs)
            subq = subq.order_by(desc(main_metric_expr))
            subq = subq.limit(timeseries_limit)
            on_clause = []
            for i, gb in enumerate(groupby):
                on_clause.append(
                    groupby_exprs[i] == column("__" + gb))

            from_clause = from_clause.join(subq.alias(), and_(*on_clause))

        qry = qry.select_from(from_clause)

        engine = self.database.get_sqla_engine()
        sql = "{}".format(
            qry.compile(engine, compile_kwargs={"literal_binds": True}))
        df = pd.read_sql_query(
            sql=sql,
            con=engine
        )
        sql = sqlparse.format(sql, reindent=True)
        return QueryResult(
            df=df, duration=datetime.now() - qry_start_dttm, query=sql)

    def fetch_metadata(self):
        table = self.database.get_table(self.table_name)
        try:
            table = self.database.get_table(self.table_name)
        except Exception as e:
            flash(str(e))
            flash(
                "Table doesn't seem to exist in the specified database, "
                "couldn't fetch column information", "danger")
            return

        TC = TableColumn
        M = SqlMetric
        metrics = []
        any_date_col = None
        for col in table.columns:
            try:
                datatype = str(col.type)
            except Exception as e:
                datatype = "UNKNOWN"
            dbcol = (
                db.session
                .query(TC)
                .filter(TC.table == self)
                .filter(TC.column_name == col.name)
                .first()
            )
            db.session.flush()
            if not dbcol:
                dbcol = TableColumn(column_name=col.name)

                if (
                        str(datatype).startswith('VARCHAR') or
                        str(datatype).startswith('STRING')):
                    dbcol.groupby = True
                    dbcol.filterable = True
                elif str(datatype).upper() in ('DOUBLE', 'FLOAT', 'INT', 'BIGINT'):
                    dbcol.sum = True
            db.session.merge(self)
            self.columns.append(dbcol)

            if not any_date_col and 'date' in datatype.lower():
                any_date_col = col.name

            quoted = "{}".format(
                column(dbcol.column_name).compile(dialect=db.engine.dialect))
            if dbcol.sum:
                metrics.append(M(
                    metric_name='sum__' + dbcol.column_name,
                    verbose_name='sum__' + dbcol.column_name,
                    metric_type='sum',
                    expression="SUM({})".format(quoted)
                ))
            if dbcol.max:
                metrics.append(M(
                    metric_name='max__' + dbcol.column_name,
                    verbose_name='max__' + dbcol.column_name,
                    metric_type='max',
                    expression="MAX({})".format(quoted)
                ))
            if dbcol.min:
                metrics.append(M(
                    metric_name='min__' + dbcol.column_name,
                    verbose_name='min__' + dbcol.column_name,
                    metric_type='min',
                    expression="MIN({})".format(quoted)
                ))
            if dbcol.count_distinct:
                metrics.append(M(
                    metric_name='count_distinct__' + dbcol.column_name,
                    verbose_name='count_distinct__' + dbcol.column_name,
                    metric_type='count_distinct',
                    expression="COUNT(DISTINCT {})".format(quoted)
                ))
            dbcol.type = datatype
            db.session.merge(self)
            db.session.commit()

        metrics.append(M(
            metric_name='count',
            verbose_name='COUNT(*)',
            metric_type='count',
            expression="COUNT(*)"
        ))
        for metric in metrics:
            m = (
                db.session.query(M)
                .filter(M.metric_name == metric.metric_name)
                .filter(M.table_id == self.id)
                .first()
            )
            metric.table_id = self.id
            if not m:
                db.session.add(metric)
                db.session.commit()
        if not self.main_dttm_col:
            self.main_dttm_col = any_date_col


class SqlMetric(Model, AuditMixinNullable):
    __tablename__ = 'sql_metrics'
    id = Column(Integer, primary_key=True)
    metric_name = Column(String(512))
    verbose_name = Column(String(1024))
    metric_type = Column(String(32))
    table_id = Column(Integer, ForeignKey('tables.id'))
    table = relationship(
        'SqlaTable', backref='metrics', foreign_keys=[table_id])
    expression = Column(Text)
    description = Column(Text)


class TableColumn(Model, AuditMixinNullable):
    __tablename__ = 'table_columns'
    id = Column(Integer, primary_key=True)
    table_id = Column(Integer, ForeignKey('tables.id'))
    table = relationship(
        'SqlaTable', backref='columns', foreign_keys=[table_id])
    column_name = Column(String(256))
    is_dttm = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    type = Column(String(32), default='')
    groupby = Column(Boolean, default=False)
    count_distinct = Column(Boolean, default=False)
    sum = Column(Boolean, default=False)
    max = Column(Boolean, default=False)
    min = Column(Boolean, default=False)
    filterable = Column(Boolean, default=False)
    expression = Column(Text, default='')
    description = Column(Text, default='')

    def __repr__(self):
        return self.column_name

    @property
    def isnum(self):
        return self.type in ('LONG', 'DOUBLE', 'FLOAT')


class DruidCluster(Model, AuditMixinNullable):
    __tablename__ = 'clusters'
    id = Column(Integer, primary_key=True)
    cluster_name = Column(String(250), unique=True)
    coordinator_host = Column(String(256))
    coordinator_port = Column(Integer)
    coordinator_endpoint = Column(
        String(256), default='druid/coordinator/v1/metadata')
    broker_host = Column(String(256))
    broker_port = Column(Integer)
    broker_endpoint = Column(String(256), default='druid/v2')
    metadata_last_refreshed = Column(DateTime)

    def __repr__(self):
        return self.cluster_name

    def get_pydruid_client(self):
        cli = client.PyDruid(
            "http://{0}:{1}/".format(self.broker_host, self.broker_port),
            self.broker_endpoint)
        return cli

    def refresh_datasources(self):
        endpoint = (
            "http://{self.coordinator_host}:{self.coordinator_port}/"
            "{self.coordinator_endpoint}/datasources"
        ).format(self=self)

        datasources = json.loads(requests.get(endpoint).text)
        for datasource in datasources:
            DruidDatasource.sync_to_db(datasource, self)


class DruidDatasource(Model, AuditMixinNullable, Queryable):
    type = "druid"

    baselink = "datasourcemodelview"

    __tablename__ = 'datasources'
    id = Column(Integer, primary_key=True)
    datasource_name = Column(String(250), unique=True)
    is_featured = Column(Boolean, default=False)
    is_hidden = Column(Boolean, default=False)
    description = Column(Text)
    default_endpoint = Column(Text)
    user_id = Column(Integer, ForeignKey('ab_user.id'))
    owner = relationship('User', backref='datasources', foreign_keys=[user_id])
    cluster_name = Column(
        String(250), ForeignKey('clusters.cluster_name'))
    cluster = relationship(
        'DruidCluster', backref='datasources', foreign_keys=[cluster_name])
    offset = Column(Integer, default=0)

    @property
    def metrics_combo(self):
        return sorted(
            [(m.metric_name, m.verbose_name) for m in self.metrics],
            key=lambda x: x[1])

    @property
    def name(self):
        return self.datasource_name

    @property
    def perm(self):
        return (
            "[{self.cluster_name}].[{self.datasource_name}]"
            "(id:{self.id})").format(self=self)

    @property
    def url(self):
        return '/datasourcemodelview/edit/{}'.format(self.id)

    @property
    def link(self):
        return (
            '<a href="{self.url}">'
            '{self.datasource_name}</a>').format(**locals())

    @property
    def full_name(self):
        return (
            "[{self.cluster_name}]."
            "[{self.datasource_name}]").format(self=self)

    def __repr__(self):
        return self.datasource_name

    @property
    def datasource_link(self):
        url = "/panoramix/explore/{self.type}/{self.id}/".format(self=self)
        return '<a href="{url}">{self.datasource_name}</a>'.format(
            url=url, self=self)

    def get_metric_obj(self, metric_name):
        return [
            m.json_obj for m in self.metrics
            if m.metric_name == metric_name
        ][0]

    def latest_metadata(self):
        client = self.cluster.get_pydruid_client()
        results = client.time_boundary(datasource=self.datasource_name)
        if not results:
            return
        max_time = results[0]['result']['maxTime']
        max_time = parse(max_time)
        intervals = (max_time - timedelta(seconds=1)).isoformat() + '/'
        intervals += (max_time + timedelta(seconds=1)).isoformat()
        segment_metadata = client.segment_metadata(
            datasource=self.datasource_name,
            intervals=intervals)
        if segment_metadata:
            return segment_metadata[-1]['columns']

    def generate_metrics(self):
        for col in self.columns:
            col.generate_metrics()

    @classmethod
    def sync_to_db(cls, name, cluster):
        print("Syncing Druid datasource [{}]".format(name))
        session = get_session()
        datasource = session.query(cls).filter_by(datasource_name=name).first()
        if not datasource:
            datasource = cls(datasource_name=name)
            session.add(datasource)
            flash("Adding new datasource [{}]".format(name), "success")
        else:
            flash("Refreshing datasource [{}]".format(name), "info")
        datasource.cluster = cluster

        cols = datasource.latest_metadata()
        if not cols:
            return
        for col in cols:
            col_obj = (
                session
                .query(DruidColumn)
                .filter_by(datasource_name=name, column_name=col)
                .first()
            )
            datatype = cols[col]['type']
            if not col_obj:
                col_obj = DruidColumn(datasource_name=name, column_name=col)
                session.add(col_obj)
            if datatype == "STRING":
                col_obj.groupby = True
                col_obj.filterable = True
            if col_obj:
                col_obj.type = cols[col]['type']
            col_obj.datasource = datasource
            col_obj.generate_metrics()

    def query(
            self, groupby, metrics,
            granularity,
            from_dttm, to_dttm,
            limit_spec=None,
            filter=None,
            is_timeseries=True,
            timeseries_limit=None,
            row_limit=None,
            inner_from_dttm=None, inner_to_dttm=None,
            extras=None,
            select=None):
        qry_start_dttm = datetime.now()

        inner_from_dttm = inner_from_dttm or from_dttm
        inner_to_dttm = inner_to_dttm or to_dttm

        # add tzinfo to native datetime with config
        from_dttm = from_dttm.replace(tzinfo=config.get("DRUID_TZ"))
        to_dttm = to_dttm.replace(tzinfo=config.get("DRUID_TZ"))

        query_str = ""
        aggregations = {
            m.metric_name: m.json_obj
            for m in self.metrics if m.metric_name in metrics
        }
        granularity = granularity or "all"
        if granularity != "all":
            granularity = utils.parse_human_timedelta(
                granularity).total_seconds() * 1000
        if not isinstance(granularity, string_types):
            granularity = {"type": "duration", "duration": granularity}

        qry = dict(
            datasource=self.datasource_name,
            dimensions=groupby,
            aggregations=aggregations,
            granularity=granularity,
            intervals=from_dttm.isoformat() + '/' + to_dttm.isoformat(),
        )
        filters = None
        for col, op, eq in filter:
            cond = None
            if op == '==':
                cond = Dimension(col) == eq
            elif op == '!=':
                cond = ~(Dimension(col) == eq)
            elif op in ('in', 'not in'):
                fields = []
                splitted = eq.split(',')
                if len(splitted) > 1:
                    for s in eq.split(','):
                        s = s.strip()
                        fields.append(Filter.build_filter(Dimension(col) == s))
                    cond = Filter(type="or", fields=fields)
                else:
                    cond = Dimension(col) == eq
                if op == 'not in':
                    cond = ~cond
            if filters:
                filters = Filter(type="and", fields=[
                    Filter.build_filter(cond),
                    Filter.build_filter(filters)
                ])
            else:
                filters = cond

        if filters:
            qry['filter'] = filters

        client = self.cluster.get_pydruid_client()
        orig_filters = filters
        if timeseries_limit and is_timeseries:
            # Limit on the number of timeseries, doing a two-phases query
            pre_qry = deepcopy(qry)
            pre_qry['granularity'] = "all"
            pre_qry['limit_spec'] = {
                "type": "default",
                "limit": timeseries_limit,
                'intervals': inner_from_dttm.isoformat() + '/' + inner_to_dttm.isoformat(),
                "columns": [{
                    "dimension": metrics[0] if metrics else self.metrics[0],
                    "direction": "descending",
                }],
            }
            client.groupby(**pre_qry)
            query_str += "// Two phase query\n// Phase 1\n"
            query_str += json.dumps(client.query_dict, indent=2) + "\n"
            query_str += "//\nPhase 2 (built based on phase one's results)\n"
            df = client.export_pandas()
            if df is not None and not df.empty:
                dims = qry['dimensions']
                filters = []
                for index, row in df.iterrows():
                    fields = []
                    for dim in dims:
                        f = Filter.build_filter(Dimension(dim) == row[dim])
                        fields.append(f)
                    if len(fields) > 1:
                        filt = Filter(type="and", fields=fields)
                        filters.append(Filter.build_filter(filt))
                    elif fields:
                        filters.append(fields[0])

                if filters:
                    ff = Filter(type="or", fields=filters)
                    if not orig_filters:
                        qry['filter'] = ff
                    else:
                        qry['filter'] = Filter(type="and", fields=[
                            Filter.build_filter(ff),
                            Filter.build_filter(orig_filters)])
                qry['limit_spec'] = None
        if row_limit:
            qry['limit_spec'] = {
                "type": "default",
                "limit": row_limit,
                "columns": [{
                    "dimension": metrics[0] if metrics else self.metrics[0],
                    "direction": "descending",
                }],
            }
        client.groupby(**qry)
        query_str += json.dumps(client.query_dict, indent=2)
        df = client.export_pandas()
        if df is None or df.size == 0:
            raise Exception("No data was returned.")

        if (
                not is_timeseries and
                granularity == "all" and
                'timestamp' in df.columns):
            del df['timestamp']

        # Reordering columns
        cols = []
        if 'timestamp' in df.columns:
            cols += ['timestamp']
        cols += [col for col in groupby if col in df.columns]
        cols += [col for col in metrics if col in df.columns]
        cols += [col for col in df.columns if col not in cols]
        df = df[cols]
        return QueryResult(
            df=df,
            query=query_str,
            duration=datetime.now() - qry_start_dttm)


class Log(Model):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    action = Column(String(512))
    user_id = Column(Integer, ForeignKey('ab_user.id'))
    dashboard_id = Column(Integer)
    slice_id = Column(Integer)
    user_id = Column(Integer, ForeignKey('ab_user.id'))
    json = Column(Text)
    user = relationship('User', backref='logs', foreign_keys=[user_id])
    dttm = Column(DateTime, default=func.now())


class DruidMetric(Model):
    __tablename__ = 'metrics'
    id = Column(Integer, primary_key=True)
    metric_name = Column(String(512))
    verbose_name = Column(String(1024))
    metric_type = Column(String(32))
    datasource_name = Column(
        String(250),
        ForeignKey('datasources.datasource_name'))
    datasource = relationship('DruidDatasource', backref='metrics')
    json = Column(Text)
    description = Column(Text)

    @property
    def json_obj(self):
        try:
            obj = json.loads(self.json)
        except Exception:
            obj = {}
        return obj


class DruidColumn(Model):
    __tablename__ = 'columns'
    id = Column(Integer, primary_key=True)
    datasource_name = Column(
        String(250),
        ForeignKey('datasources.datasource_name'))
    datasource = relationship('DruidDatasource', backref='columns')
    column_name = Column(String(256))
    is_active = Column(Boolean, default=True)
    type = Column(String(32))
    groupby = Column(Boolean, default=False)
    count_distinct = Column(Boolean, default=False)
    sum = Column(Boolean, default=False)
    max = Column(Boolean, default=False)
    min = Column(Boolean, default=False)
    filterable = Column(Boolean, default=False)
    description = Column(Text)

    def __repr__(self):
        return self.column_name

    @property
    def isnum(self):
        return self.type in ('LONG', 'DOUBLE', 'FLOAT')

    def generate_metrics(self):
        M = DruidMetric
        metrics = []
        metrics.append(DruidMetric(
            metric_name='count',
            verbose_name='COUNT(*)',
            metric_type='count',
            json=json.dumps({'type': 'count', 'name': 'count'})
        ))
        # Somehow we need to reassign this for UDAFs
        if self.type in ('DOUBLE', 'FLOAT'):
            corrected_type = 'DOUBLE'
        else:
            corrected_type = self.type

        if self.sum and self.isnum:
            mt = corrected_type.lower() + 'Sum'
            name = 'sum__' + self.column_name
            metrics.append(DruidMetric(
                metric_name=name,
                metric_type='sum',
                verbose_name='SUM({})'.format(self.column_name),
                json=json.dumps({
                    'type': mt, 'name': name, 'fieldName': self.column_name})
            ))
        if self.min and self.isnum:
            mt = corrected_type.lower() + 'Min'
            name = 'min__' + self.column_name
            metrics.append(DruidMetric(
                metric_name=name,
                metric_type='min',
                verbose_name='MIN({})'.format(self.column_name),
                json=json.dumps({
                    'type': mt, 'name': name, 'fieldName': self.column_name})
            ))
        if self.max and self.isnum:
            mt = corrected_type.lower() + 'Max'
            name = 'max__' + self.column_name
            metrics.append(DruidMetric(
                metric_name=name,
                metric_type='max',
                verbose_name='MAX({})'.format(self.column_name),
                json=json.dumps({
                    'type': mt, 'name': name, 'fieldName': self.column_name})
            ))
        if self.count_distinct:
            mt = 'count_distinct'
            name = 'count_distinct__' + self.column_name
            metrics.append(DruidMetric(
                metric_name=name,
                verbose_name='COUNT(DISTINCT {})'.format(self.column_name),
                metric_type='count_distinct',
                json=json.dumps({
                    'type': 'cardinality',
                    'name': name,
                    'fieldNames': [self.column_name]})
            ))
        session = get_session()
        for metric in metrics:
            m = (
                session.query(M)
                .filter(M.metric_name == metric.metric_name)
                .filter(M.datasource_name == self.datasource_name)
                .filter(DruidCluster.cluster_name == self.datasource.cluster_name)
                .first()
            )
            metric.datasource_name = self.datasource_name
            if not m:
                session.add(metric)
                session.commit()
