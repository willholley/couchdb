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

import copy
import mango
import unittest

DOCS = [
    {
        "_id": "1",
        "name": "Jimi"
    },
    {
        "_id": "2",
        "name": {"forename":"Eddie"}
    },
    {
        "_id": "3",
        "name": None
    },
    {
        "_id": "4",
        "name": 1
    },
    {
        "_id": "5",
        "forename": "Sam"
    }
]

class MultiValueFieldDocsNoIndexes(mango.DbPerClass):
    def setUp(self):
        self.db.recreate()
        self.db.save_docs(copy.deepcopy(DOCS))


class MultiValueFieldTests:

    def test_can_query_all_docs_with_name(self):
        docs = self.db.find({"name": {"$exists": True}})
        self.assertEqual(len(docs), 4)
        for d in docs:
            self.assertIn("name", d)

    def test_can_query_all_docs_with_name_subfield(self):
        docs = self.db.find({"name.forename": {"$exists": True}})
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0]["_id"], "2")

    def test_can_query_all_docs_with_name_range(self):
        docs = self.db.find({"name": {"$gte": 0}})
        # expect to include "Jimi", 1 and {"forename":"Eddie"}
        self.assertEqual(len(docs), 3)
        for d in docs:
            self.assertIn("name", d)



# class MultiValueFieldJSONTests(MultiValueFieldDocsNoIndexes, MultiValueFieldTests):
#     pass

# @unittest.skipUnless(mango.has_text_service(), "requires text service")
# class MultiValueFieldTextTests(MultiValueFieldDocsNoIndexes, OperatorTests):
#     pass


class MultiValueFieldAllDocsTests(MultiValueFieldDocsNoIndexes, MultiValueFieldTests):
    pass
