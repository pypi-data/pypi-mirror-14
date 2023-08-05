###############################################################################
#
#   Copyright: (c) 2015 Carlo Sbraccia
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
###############################################################################

from onyx.core.database.objdb_api import AddObj, GetObj, DelObj
from onyx.core.depgraph.graph import CreateNode, GraphNode
from onyx.core.depgraph.graph import GraphNodeSettable, GraphNodeCalc
from onyx.core.depgraph.test import ufo_testcls
from onyx.core.utils.unittest import OnyxTestCase
from onyx.core import database as onyx_db

import unittest
import copy
import types


class TestGraphScopes(OnyxTestCase):
    def setUp(self):
        super().setUp()
        self.test_obj = AddObj(ufo_testcls.TestCls0(Name="testobj"))
        self.test_obj_name = self.test_obj.Name

    def tearDown(self):
        DelObj(self.test_obj_name)
        super().tearDown()

    def test_references(self):
        # --- here we check that the object reference contained in each node
        #     is consistent with what is in the cache of the database client
        #     and survives refreshing such cache
        node = CreateNode((self.test_obj_name, "Name"))
        ref_id = id(node.obj_ref())
        self.assertEqual(ref_id, id(self.test_obj))
        self.assertEqual(ref_id, id(GetObj(self.test_obj_name)))
        del self.test_obj
        self.assertEqual(ref_id, id(GetObj(self.test_obj_name)))
        self.assertEqual(ref_id, id(GetObj(self.test_obj_name, True)))
        del onyx_db.obj_clt[self.test_obj_name]
        with self.assertRaises(KeyError):
            onyx_db.obj_clt[self.test_obj_name]
        self.assertNotEqual(ref_id, id(node.obj_ref()))  # obj_ref is None
        self.assertNotEqual(ref_id, id(GetObj(self.test_obj_name, True)))

    def test_create_nodes(self):
        # --- create a node that points to "Name"
        node = CreateNode((self.test_obj.Name, "Name"))
        self.assertTrue(isinstance(node, GraphNodeSettable))
        self.assertEqual(node.get_value(), "testobj")

        # --- create a node that points to "Version"
        node = CreateNode((self.test_obj.Name, "Version"))
        self.assertTrue(isinstance(node, GraphNodeSettable))
        self.assertEqual(node.get_value(), 0)

        # --- create a node that points to "StoredAttrs"
        node = CreateNode((self.test_obj.Name, "StoredAttrs"))
        self.assertTrue(isinstance(node, GraphNode))
        self.assertEqual(node.get_value(), self.test_obj.StoredAttrs)

        # --- create a node that points to "test_method"
        node = CreateNode((self.test_obj.Name, "test_method"))
        self.assertTrue(isinstance(node, GraphNodeCalc))
        self.assertEqual(node.get_value(123), self.test_obj.test_method(123))

        # --- create a node that points to a non-existing method
        self.assertRaises(AttributeError, CreateNode,
                          (self.test_obj.Name, "not_there"))

    def test_invalidation1(self):
        # --- create a node that points to "StoredAttrs"
        node = CreateNode((self.test_obj.Name, "StoredAttrs"))

        test_obj_attrs = copy.deepcopy(self.test_obj.StoredAttrs)

        # --- as before, test_obj has only standard attributes
        self.assertEqual(node.get_value(), test_obj_attrs)

        # --- add a new attribute to test_obj
        self.test_obj.NewAttr = "This is brand new!"

        # --- the node is still valid, hence get_value still returns the same
        #     set of attributes as before
        self.assertTrue(node.valid)
        self.assertEqual(node.get_value(), test_obj_attrs)

        # --- after invalidation we expect to see the new attribute
        node.invalidate()
        self.assertFalse(node.valid)
        self.assertEqual(node.get_value(), self.test_obj.StoredAttrs)
        self.assertTrue(node.valid)

    def test_invalidation2(self):
        # --- we add a few more attributes to test_obj as well as a
        #     calculated method
        self.test_obj.Num1 = 1.0
        self.test_obj.Num2 = 2.0

        setattr(ufo_testcls.TestCls0, "sum",
                types.MethodType(lambda s: s.Num1 + s.Num2, self.test_obj))

        # --- create a node that points to "sum"
        node = CreateNode((self.test_obj.Name, "sum"))

        # --- this should be a calculated node whose value is Num1+Num2
        self.assertTrue(isinstance(node, GraphNodeCalc))
        self.assertEqual(node.get_value(), 3.0)

        # --- if we change Num1, nothing should happen to sum because the
        #     result is still cached
        self.test_obj.Num1 = 2.0
        self.assertTrue(node.valid)
        self.assertEqual(node.get_value(), 3.0)

        # --- but after invalidation, sum will be recalculated
        node.invalidate()
        self.assertFalse(node.valid)
        self.assertEqual(node.get_value(), 4.0)

    def test_clone(self):
        # --- create a node that points to "StoredAttrs" and make a clone
        node1 = CreateNode((self.test_obj.Name, "StoredAttrs"))
        node2 = node1.clone()

        # --- test that the two nodes are different objects, return the same
        #     value and share the same reference to the underlying object
        self.assertNotEqual(node1, node2)
        self.assertEqual(node1.get_value(), node2.get_value())
        self.assertEqual(node1.obj_ref, node2.obj_ref)
        self.assertIs(node1.obj_ref, node2.obj_ref)
        self.assertIs(node1.obj_ref(), self.test_obj)
        self.assertIs(node2.obj_ref(), self.test_obj)

        # --- again, we add a few more attributes to test_obj as well as a
        #     calculated method
        self.test_obj.Num1 = 1.0
        self.test_obj.Num2 = 2.0

        def my_sum(instance):
            return instance.Num1 + instance.Num2

        setattr(ufo_testcls.TestCls0, "sum",
                types.MethodType(my_sum, self.test_obj))

        # --- create a node that points to "sum" and make a clone
        node1 = CreateNode((self.test_obj.Name, "sum"))
        node2 = node1.clone()

        # --- test that the two nodes are different objects, return the same
        #     value and share the same reference to the underlying object
        self.assertNotEqual(node1, node2)
        self.assertEqual(node1.get_value(), node2.get_value())
        self.assertEqual(node1.obj_ref, node2.obj_ref)
        self.assertIs(node1.obj_ref, node2.obj_ref)
        self.assertIs(node1.obj_ref(), self.test_obj)
        self.assertIs(node2.obj_ref(), self.test_obj)

        # --- test that invalidation only affects a specific node
        self.test_obj.Num1 = 2.0
        node1.invalidate()
        self.assertFalse(node1.valid)
        self.assertTrue(node2.valid)
        self.assertEqual(node1.get_value(), 4.0)
        self.assertEqual(node2.get_value(), 3.0)
        node2.invalidate()
        self.assertFalse(node2.valid)
        self.assertEqual(node2.get_value(), 4.0)

if __name__ == "__main__":
    from onyx.core.utils.unittest import UseEphemeralDbs
    with UseEphemeralDbs():
        unittest.main(failfast=True)
