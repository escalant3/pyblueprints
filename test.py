#!/usr/bin/env python
#-*- coding:utf-8 -*-


###############################################################################
# This test has been performed with a default neo4j-community-1.3 distribution#
###############################################################################

import unittest
from pyblueprints.neo4j import *

HOST = 'http://localhost:7474/db/data'


class RequestServerTestSuite(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGraphInvalidConnection(self):
        self.assertRaises(client.NotFoundError,
                            Neo4jGraph,
                            'http://invalidurl')

    def testGraphValidConnection(self):
        graph= Neo4jGraph(HOST)
        self.assertIsInstance(graph, Neo4jGraph)

    def testAddRemoveVertex(self):
        graph= Neo4jGraph(HOST)
        vertex = graph.addVertex()
        self.assertIsInstance(vertex, Vertex)
        _id = vertex.getId()
        graph.removeVertex(vertex)
        self.assertIsNone(graph.getVertex(_id))

    def testAddRemoveEdges(self):
        graph= Neo4jGraph(HOST)
        v1 = graph.addVertex()
        v2 = graph.addVertex()
        newEdge = graph.addEdge(v1, v2, 'myLabel')
        self.assertIsInstance(newEdge, Edge)
        _id = newEdge.getId()
        graph.removeEdge(newEdge)
        self.assertIsNone(graph.getEdge(_id))

    def testVertexMethods(self):
        graph= Neo4jGraph(HOST)
        v1 = graph.addVertex()
        v2 = graph.addVertex()
        newEdge = graph.addEdge(v1, v2, 'myLabel')
        _id = v1.getId()
        vertex = graph.getVertex(_id)
        self.assertIsInstance(vertex, Vertex)
        self.assertEqual(vertex.getId(), _id)
        edge = list(vertex.getBothEdges())[0]
        self.assertIsInstance(edge, Edge)
        edge = list(vertex.getOutEdges())[0]
        self.assertIsInstance(edge, Edge)
        edges = list(vertex.getInEdges())
        self.assertEqual(edges, [])

    def testElementProperties(self):
        graph= Neo4jGraph(HOST)
        vertex = graph.addVertex()
        vertex.setProperty('name', 'paquito')
        properties = ['name']
        self.assertEqual(vertex.getPropertyKeys(), properties)
        self.assertEqual(vertex.getProperty('name'), 'paquito')
        vertex.setProperty('name', 'pablito')
        self.assertEqual(vertex.getProperty('name'), 'pablito')
        vertex.removeProperty('name')
        self.assertNotIn('name', vertex.getPropertyKeys())

    def testEdgeMethods(self):
        graph= Neo4jGraph(HOST)
        v1 = graph.addVertex()
        v2 = graph.addVertex()
        _id1 = v1.getId()
        _id2 = v2.getId()
        edge = graph.addEdge(v1, v2, 'myLabel')
        outVertex = edge.getOutVertex()
        self.assertIsInstance(outVertex, Vertex)
        self.assertEqual(outVertex.getId(), _id1)
        inVertex = edge.getInVertex()
        self.assertIsInstance(inVertex, Vertex)
        self.assertEqual(inVertex.getId(), _id2)
        self.assertEqual(edge.getLabel(), 'myLabel')

"""
TODO when API is able to delete indexes
    def testAddRemoveManualIndex(self):
        graph= Neo4jIndexableGraph(HOST)
        index = graph.createManualIndex('myManualIndex', 'vertex')
        self.assertIsInstance(index, Index)
        index = graph.getIndex('myManualIndex', 'vertex')
        self.assertIsInstance(index, Index)
        graph.dropIndex('myManualIndex')
        self.assertRaises(RexsterException,
                            graph.getIndex,
                            'myManualIndex',
                            'vertex')
    
    def testAddRemoveAutomaticIndex(self):
        pass

    def testIndexing(self):
        graph= Neo4jIndexableGraph(HOST)
        index = graph.createManualIndex('myManualIndex', 'vertex')
        vertex = graph.addVertex()
        _id = vertex.getId()
        index.put('key1', 'value1', vertex)
        self.assertEqual(index.count('key1', 'value1'), _id)
        self.assertEqual(index.getIndexName(), 'myManualIndex')
        self.assertEqual(index.getIndexClass(), 'vertex')
        self.assertEqual(index.getIndexType(), 'manual')
        vertex2 = list(index.get('key1', 'value1'))[0]
        self.assertEqual(vertex.getId(), vertex2.getId())
        index.remove('key1', 'value1', vertex)
        self.assertEqual(index.count('key1', 'value1'), 0)
        graph.dropIndex('myManualIndex')
"""
if __name__ == "__main__":
    unittest.main()
