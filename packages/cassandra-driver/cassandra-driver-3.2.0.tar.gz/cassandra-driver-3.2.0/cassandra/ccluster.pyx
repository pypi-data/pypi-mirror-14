# Copyright 2013-2016 DataStax, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

cimport ccluster

cdef class CCluster:
    cdef ccluster.CassCluster* _cluster
    cdef ccluster.CassSession* _session

    def __cinit__(self):
        self._cluster = cass_cluster_new()
        cass_cluster_set_contact_points(self._cluster, "127.0.0.1")
        self._session = cass_session_new()

        cdef ccluster.CassFuture* future = cass_session_connect_keyspace(self._session, self._cluster, "testkeyspace")

        cass_future_wait(future)
        rc = cass_future_error_code(future);
        if rc != CASS_OK:
            print('error')
        else:
            print('all good bro, connected to cluster')

    cpdef execute(self, const char* query):
        cdef ccluster.CassStatement* statement
        with nogil:
            statement = cass_statement_new(query, 0)
            future = cass_session_execute(self._session, statement)
            cass_future_wait(future)

            rc = cass_future_error_code(future)
        if rc != CASS_OK:
            print('error: {0}'.format(rc))



# cdef class PyCluster:
