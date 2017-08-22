# -*- coding: latin-1 -*-
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.


import mango


class ExecutionStatsTests(mango.UserDocsTests):

    def test_simple_json_index(self):
        resp = self.db.find({"age": {"$lt": 35}}, return_raw=True, executionStats=True)
        assert len(resp["docs"]) == 3
        assert resp["execution_stats"]["total_keys_examined"] == 0
        assert resp["execution_stats"]["total_docs_examined"] == 3
        assert resp["execution_stats"]["total_quorum_docs_examined"] == 0
        assert resp["execution_stats"]["results_returned"] == 3

    def test_no_execution_stats(self):
        resp = self.db.find({"age": {"$lt": 35}}, return_raw=True, executionStats=False)
        assert "execution_stats" not in resp

    def test_quorum_json_index(self):
        resp = self.db.find({"age": {"$lt": 35}}, return_raw=True, r=3, executionStats=True)
        assert len(resp["docs"]) == 3
        assert resp["execution_stats"]["total_keys_examined"] == 0
        assert resp["execution_stats"]["total_docs_examined"] == 0
        assert resp["execution_stats"]["total_quorum_docs_examined"] == 3
        assert resp["execution_stats"]["results_returned"] == 3
