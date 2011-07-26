pyblueprints
============

:synopsis: Provides a layer to abstract the Python developer from the graph database system used

Following the set of interfaces provided by tinkerpop for Blueprints,
this proyect aims to give Python developers a similar functionality.
A set of abstract classes are defined in order to guide the design of
implementations for the different graph database engines.

Features
--------

This is an experimental version only permitting partial functionality to:

 - Rexster infrastructure, supporting every database supported by Rexster (https://github.com/tinkerpop/rexster/)
 - Neo4j database providing abstraction over the neo4j-rest-client API.


Please keep in mind to backup your data before trying this library.

Installation
------------
The easiest way to get pyblueprints installed in your virtualenv is by:

 pip install pyblueprints


Usage
-----

This version of pybluerprints allows you to connect to graph databases by a Rexster Instance or through the neo4j-rest-client API. Therefore a Neo4j database can be accessed with both options, although the Neo4j transactional mode is only available through the later.
The Rexster instance also provides connection to the following databases:

 - TinkerGraph
 - OrientDB
 - DEX
 - Sail RDF Stores


Rexster
"""""""
Connecting to a Rexster instance

>>> from pyblueprints import RexsterServer, RexsterGraph, RexsterIndexableGraph 
>>> #Connecting to server
>>> HOST = 'http://localhost:8182'
>>> server = RexsterServer(HOST)
>>> #List graphs availbale in server
>>> server.graphs()
[u'tinkergraph', u'gratefulgraph', u'tinkergraph-readonly', u'sailgraph', u'emptygraph']
>>> #Connecting to a given graph
>>> graph = RexsterIndexableGraph(server, 'tinkergraph')



neo4j-rest-client
"""""""""""""""""

Creating a graph object through the neo4j-rest-client API

>>> from pyblueprints.neo4j import Neo4jGraph
>>> graph = Neo4jGraph('http://localhost:7474/db/data')

Creating an indexable graph object through the neo4j-rest-client API

>>> from pyblueprints.neo4j import Neo4jIndexableGraph
>>> graph = Neo4jIndexableGraph('http://localhost:7474/db/data')

The available classes are:
 - Neo4jGraph
 - Neo4jIndexableGraph
 - Neo4jTransactionalGraph
 - Neo4jTransactionalIndexableGraph


code examples
"""""""""""""

Add/Remove Vertex
'''''''''''''''''
>>> vertex = graph.addVertex()
>>> graph.removeVertex(vertex)

Add/Remove Edge
'''''''''''''''
>>> v1 = graph.addVertex()
>>> v2 = graph.addVertex()
>>> newEdge = graph.addEdge(v1, v2, 'myLabel')
>>> graph.removeEdge(newEdge)

Vertex Methods
''''''''''''''
>>> graph= Neo4jGraph(HOST)
>>> v1 = graph.addVertex()
>>> v2 = graph.addVertex()
>>> newEdge = graph.addEdge(v1, v2, 'myLabel')
>>> vertex = graph.getVertex(_id)
>>> # get methods return a generator function
>>> edge = list(vertex.getBothEdges())[0]
>>> edge = list(vertex.getOutEdges())[0]
>>> edges = list(vertex.getInEdges())

Vertex/Edges properties
'''''''''''''''''''''''
>>> vertex_id = vertex.getId()
>>> vertex.setProperty('name', 'paquito')
>>> print vertex.getPropertyKeys()
>>> print vertex.getProperty('name')
>>> vertex.removeProperty('name')

Edge Methods
''''''''''''
>>> outVertex = edge.getOutVertex()
>>> inVertex = edge.getInVertex()
>>> print getLabel()

Add/Remove Manual Index
'''''''''''''''''''''''
>>> index = graph.createManualIndex('myManualIndex', 'vertex')
>>> graph.dropIndex('myManualIndex', 'vertex')
    
Index Methods
'''''''''''''
>>> index = graph.getIndex('myManualIndex', 'vertex')
>>> vertex = graph.addVertex()
>>> index.put('key1', 'value1', vertex)
>>> print index.count('key1', 'value1')
>>> print index.getIndexName()
>>> print index.getIndexClass()
>>> print index.getIndexType()
>>> # get returns a generator function
>>> vertex2 = list(index.get('key1', 'value1'))[0]
>>> index.remove('key1', 'value1', vertex)

Transactional Methods
'''''''''''''''''''''
>>> graph= Neo4jTransactionalGraph(HOST)
>>> graph.startTransaction()
>>> v = graph.addVertex()
# Stoping calls the commit
>>> graph.stopTransaction()
>>> vertexId = v.getId()
>>> v = graph.getVertex(vertexId)
>>> graph.startTransaction()
>>> v.setProperty('p1', 'v1')
>>> graph.stopTransaction()
