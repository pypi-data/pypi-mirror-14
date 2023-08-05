"""
WSQL
====
An asynchronous DB API v2.0 compatible interface to MySQL
---------------------------------------------------------

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "@bg"

try:
    from _case import DatabaseTestCase
    import _wsql_context
except ImportError:  # pragma: no cover
    from ._case import DatabaseTestCase
    from . import _wsql_context

from unittest import TestCase
from wsql import exceptions
from wsql.cluster import ConnectionPool, Upstream, transaction, retryable, Cluster, connect
from wsql.cluster.upstream import ServerInfo, Connection
from wsql.cluster import _parser


class DummyLogger:
    @staticmethod
    def error(msg, *args, **kwargs):
        pass


class TestServerInfo(TestCase):
    def test_to_str(self):
        srv_info = ServerInfo(host='localhost', port=3306)
        self.assertEqual('localhost:3306', str(srv_info))
        srv_info = ServerInfo(socket_name='/var/tmp/socket.sock')
        self.assertEqual('/var/tmp/socket.sock', str(srv_info))


class TestCluster(DatabaseTestCase):
    def make_upstream(self, servers):
        """abstract method to create a upstream"""
        return Upstream(servers, DummyLogger, loop=self._context.loop, **self._context.connect_kwargs)

    def make_pool(self, upstream, timeout):
        """abstract method to create connection pool"""
        return ConnectionPool(upstream, timeout=timeout, loop=self._context.loop)

    def get_insert_query(self, table, error=None):  # pragma: no cover
        """
        get the query query
        :param table: the temporary table name
        :param error: error, that should be raised if specified
        :return: the query, that run query logic
        """
        raise NotImplementedError

    def wrap_query(self, query):  # pragma: no cover
        """
        make a new query around specified
        :param query: the query to wrap
        :return: wrapped query
        """
        raise NotImplementedError

    def make_exception_query(self, retry_count):  # pragma: no cover
        """create query with retry_count"""
        raise NotImplementedError

    def count_calls(self, func):
        def wrapper(*args, **kwargs):
            wrapper.call_count += 1
            return func(*args, **kwargs)

        wrapper.call_count = 0
        return wrapper

    def test_next(self):
        """test next method of Upstream"""
        kwargs2 = self._context.connect_kwargs.copy()
        kwargs2['port'] = 1
        upstream = self.make_upstream([kwargs2, self._context.connect_kwargs])
        connection = self._context.wait(next(upstream))
        connection2 = self._context.wait(next(upstream))
        self.assertIs(self._context.connect_kwargs['host'], connection.meta.kwargs['host'])
        self.assertIs(self._context.connect_kwargs['host'], connection2.meta.kwargs['host'])
        self.assertTrue((x.penalty > 0 for x in upstream._servers))

    def test_no_connections(self):
        """test case when there is no online servers more"""
        kwargs2 = self._context.connect_kwargs.copy()
        kwargs2['port'] = 1
        upstream = self.make_upstream([kwargs2])
        with self.assertRaises(RuntimeError):
            self._context.wait(next(upstream))

    def test_invalidate(self):
        """test invalidate method of Upstream"""
        upstream = self.make_upstream([self._context.connect_kwargs])
        connection = self._context.wait(next(upstream))
        upstream.invalidate(connection)
        self.assertGreater(connection.meta.penalty, 0)
        connection.meta.penalty = 0
        upstream.invalidate(connection.meta)
        self.assertGreater(connection.meta.penalty, 0)
        self.assertGreater(upstream._servers[0].penalty, 0)
        self.assertRaises(ValueError, upstream.invalidate, 1)

    def test_acquire(self):
        """test _acquire method of ConnectionPoolAsync"""
        connections = []
        pool_size = 3
        timeout = 0.1

        pool = self.make_pool(self.make_upstream([{'count': pool_size}]), timeout)

        for i in range(pool_size):
            connection = self._context.wait(pool._acquire())
            self.assertIsNotNone(connection)
            connections.append(connection)
            self.assertEqual(pool_size - i - 1, pool._reserve)
        self.assertEqual(pool_size, len(connections))

    def test_release(self):
        """test _release method of ConnectionPoolAsync"""
        pool_size = 3
        timeout = 0.1

        pool = self.make_pool(self.make_upstream([{"count": pool_size}]), timeout)
        connection = self._context.wait(pool._acquire())
        self.assertIsNotNone(connection)
        self.assertEqual(0, pool._queue.qsize())
        pool._release(connection)
        self.assertEqual(1, pool._queue.qsize())

    def test_release_closed_connection(self):
        """test _release method of ConnectionPoolAsync in case if connection closed"""
        pool_size = 3
        timeout = 0.1

        pool = self.make_pool(self.make_upstream([{"count": pool_size}]), timeout)
        connection = self._context.wait(pool._acquire())
        self.assertIsNotNone(connection)
        self.assertEqual(0, pool._queue.qsize())
        connection.connection().close()
        pool._release(connection)
        self.assertEqual(0, pool._queue.qsize())
        self.assertEqual(pool_size, pool._reserve)

    def test_acquire_if_no_free(self):
        """test _acquire method of ConnectionPoolAsync if there is no free connections"""
        connections = []
        pool_size = 3
        timeout = 0.1

        pool = self.make_pool(self.make_upstream([{"count": pool_size}]), timeout)

        for i in range(pool_size):
            connection = self._context.wait(pool._acquire())
            self.assertIsNotNone(connection)
            connections.append(connection)
            self.assertEqual(pool_size - i - 1, pool._reserve)
        self.assertEqual(0, pool._reserve)
        self.assertTrue(pool._queue.empty())
        self.assertRaises(pool.TimeoutError, self._context.call_and_wait, pool._acquire)

    def test_connection_pool_execute(self):
        """test _release method of ConnectionPoolAsync"""
        pool_size = 3
        timeout = 0.1
        pool = self.make_pool(self.make_upstream([{"count": pool_size}]), timeout)
        connection = self._context.wait(pool.execute(self._context.decorator(lambda x: x)))
        self.assertIsNotNone(connection)

    def test_transaction_rollback(self):
        """test transaction rollback"""
        table = self._create_table(('name VARCHAR(10)',), None)

        connection_holder = Connection(self._context.make_connection())
        query = self.get_insert_query(table, Exception('rollback expected!'))
        self.assertRaisesRegex(Exception, 'rollback expected!',
                               self._context.call_and_wait, connection_holder.execute, transaction(query))

        cursor = self._context.cursor()
        self._context.wait(cursor.execute("SELECT * FROM %s" % table))
        self.assertEqual([], cursor.fetchall())

    def test_commit(self):
        """test transaction commit"""
        table = self._create_table(('name VARCHAR(10)',), None)

        connection = Connection(self._context.make_connection())
        query = self.get_insert_query(table)
        self.assertIs(self._context.wait(connection.execute(transaction(query))), True)

        self._context.wait(connection.rollback())
        cursor = self._context.cursor()
        self._context.wait(cursor.execute("SELECT * FROM %s" % table))
        self.assertEqual([('Evelina',)], cursor.fetchall())

    def test_recursive_transaction(self):
        """test recursive transaction"""
        table = self._create_table(('name VARCHAR(10)',), None)

        connection_holder = Connection(self._context.make_connection())
        query = transaction(self.get_insert_query(table))
        connection_holder.commit = self.count_calls(connection_holder.commit)
        connection_holder.commit.call_count = 0
        self._context.wait(connection_holder.execute(transaction(query)))
        self.assertEqual(1, connection_holder.commit.call_count)

    def test_retries(self):
        """test retries"""
        retry_count = 3
        delay = 0.1

        connection = retryable(Connection(self._context.make_connection()), retry_count, delay)
        query = self.make_exception_query(retry_count - 1)
        self._context.wait(connection.execute(query))

        self.assertEqual(retry_count - 1, query.call_count)
        query = self.make_exception_query(retry_count + 1)
        self.assertRaises(Exception, self._context.call_and_wait, connection.execute, query)

    def test_cluster(self):
        """ test commutator """
        read_connection = Connection(self._context.make_connection())
        write_connection = Connection(self._context.make_connection())
        read_connection.readonly = True
        write_connection.readonly = False
        read_query = self.wrap_query(lambda x: self.assertTrue(x.readonly))
        write_query = transaction(self.wrap_query(lambda x: self.assertFalse(x.readonly)))

        cluster = Cluster(master=write_connection, slave=read_connection)
        self._context.wait(cluster.execute(read_query))
        self._context.wait(cluster.execute(write_query))

        cluster = Cluster(master=None, slave=read_connection)
        self.assertRaisesRegex(Exception, "the operation is not permitted on read-only cluster", cluster.execute, write_query)

    def test_connect(self):
        """test connect to the cluster"""
        connection_args = {"master": "localhost:3306#2,localhost#4", "slave": "localhost:3306#2", "database": "test"}
        connection = connect(connection_args, loop=self._context.loop)
        self.assertIsInstance(connection, Cluster)
        self.assertEqual(6, len(connection._cluster[1]._connection._upstream))
        self.assertEqual(2, len(connection._cluster[0]._connection._upstream))
        connection_args = {"slave": "localhost:3306#2", "database": "test"}
        self.assertIsInstance(connect(connection_args, loop=self._context.loop), Cluster)
        connection_args = {"master": "localhost:3306#2,localhost#4", "database": "test"}
        self.assertFalse(isinstance(connect(connection_args, loop=self._context.loop), Cluster))
        connection_args = {}
        self.assertFalse(isinstance(connect(connection_args, loop=self._context.loop), Cluster))
        connection_args = "master=localhost:3306#2,localhost#4;slave=localhost:3306#2;database=test;"
        connection = connect(connection_args, loop=self._context.loop)
        self.assertIsInstance(connection, Cluster)
        self.assertEqual(6, len(connection._cluster[1]._connection._upstream))
        self.assertEqual(2, len(connection._cluster[0]._connection._upstream))
        # test real connect
        connection_args = {"master": "%(host)s" % _wsql_context.Configuration.connect_kwargs}
        connection_args.update(_wsql_context.Configuration.connect_kwargs)
        connection = connect(connection_args, loop=self._context.loop)
        connection.execute(self.wrap_query(lambda x: None))


class TestClusterSync(TestCluster):
    @classmethod
    def get_context(cls):
        return _wsql_context.Context(_wsql_context.Configuration())

    def get_insert_query(self, table, error=None):
        def query(connection):
            cursor = self._context.wrap(connection.cursor())
            try:
                cursor.execute('INSERT INTO `%s` VALUES(\'%s\');' % (table, 'Evelina'))
            finally:
                cursor.close()

            if error:
                raise error
            return True

        return query

    def wrap_query(self, query):
        """
        make a new query around specified
        :param query: the query to wrap
        :return: wrapped query
        """
        return query

    def make_exception_query(self, retry_count):
        def query(_):
            query.call_count += 1
            if query.call_count < retry_count:
                exc = self._context.errors.Error(self._context.constants.CR_SERVER_LOST, "connection lost")
                exc.code = self._context.constants.CR_SERVER_LOST
                raise exc
            return None
        query.call_count = 0
        return query


class TestClusterAsync(TestCluster):
    @classmethod
    def get_context(cls):
        return _wsql_context.Context(_wsql_context.ConfigurationAsync())

    def get_insert_query(self, table, error=None):
        @self._context.decorator
        def query(connection):
            cursor = connection.cursor()
            try:
                yield from cursor.execute('INSERT INTO %s VALUES (\'%s\')' % (table, 'Evelina'))
            finally:
                yield from cursor.close()

            if error:
                raise error
            return True

        return query

    def wrap_query(self, query):
        """
        make a new query around specified
        :param query: the query to wrap
        :return: wrapped query
        """
        @self._context.decorator
        def wrapper(connection):
            if self._context.iscoroutine(query):  # pragma: no cover
                return (yield from query(connection))
            return query(connection)
        return wrapper

    def make_exception_query(self, retry_count):
        @self._context.decorator
        def query(_):
            query.call_count += 1
            if query.call_count < retry_count:
                exc = self._context.errors.Error(self._context.constants.CR_SERVER_LOST, "connection lost")
                exc.code = self._context.constants.CR_SERVER_LOST
                raise exc
            return None
        query.call_count = 0
        return query

del TestCluster


class TestException(TestCase):
    """
    test user exceptions
    """
    class TestError(exceptions.UserError):
        pass

    def test_handle_error(self):
        """test handle_error method"""

        self.assertRaisesRegex(self.TestError, "(1, 'this is test error')", exceptions.handle_error, self, exceptions.UserError(1, "TestError; this is test error"))
        self.assertRaisesRegex(exceptions.UserError, "(1, 'Test2Error; this is test error')", exceptions.handle_error, self, exceptions.UserError(1, "Test2Error; this is test error"))
        self.assertRaisesRegex(
            exceptions.UserError, "(1, 'this is test error')", exceptions.handle_error, self, exceptions.UserError(1, "this is test error"))
        self.assertRaisesRegex(ValueError, "this is test error", exceptions.handle_error, self, ValueError("this is test error"))


class TestParsers(TestCase):
    def test_connection_parser(self):
        """test parser of connection string"""
        args = _parser.parse_connection_string("database=test;master=localhost:3306#2,localhost#4")
        self.assertEqual({"database": "test", "master": "localhost:3306#2,localhost#4"}, args)

        args2 = _parser.parse_connection_string(args)
        self.assertEqual(args, args2)

        self.assertRaises(ValueError, _parser.parse_connection_string, ["database=test;master=localhost:3306#2,localhost#4"])

    def test_uri_parser(self):
        """test parse uri"""
        result = _parser.uri_parser(lambda x: list(x))("mysql://localhost:3306#2,127.0.0.1#4")
        self.assertEqual(
            [
                {"scheme": "mysql", "host": "localhost", "port": "3306", "count": "2"},
                {"scheme": None, "port": None, "host": "127.0.0.1", "count": "4"}
            ],
            result
        )
        result = _parser.uri_parser(lambda x: list(x))("a-b_c123.13.domen.com:3306#1")
        self.assertEqual(
            [{"scheme": None, "host": "a-b_c123.13.domen.com", "port": "3306", "count": "1"}],
            result
        )
