pyblueprints
============

SYNOPSIS: Provides a layer to abstract the Python developer from the graph database system used

Following the set of interfaces provided by tinkerpop for Blueprints,
this proyect aims to give Python developers a similar functionality.
A set of abstract classes are defined in order to guide the design of
implementations for the different graph database engines.

Features
--------

This is an experimental version only permitting partial functionality to:
- Rexster infrastructure, supporting every database supported by Rexster (https://github.com/tinkerpop/rexster/)
- Neo4j database providing abstraction over the neo4j-rest-client API.


Installation
------------
The easiest way to get pyblueprints installed in your virtualenv is by:

 pip install pyblueprints


Usage
-----

This version of pybluerprints allows you to connect to graph databases by a Rexster Instance or through the neo4j-rest-client API. Therefore a Neo4j database can be accessed with both options.
The Rexster instance also provides connection to the following databases:

 - TinkerGraph
 - OrientDB
 - DEX
 - Sail RDF Stores


Rexster
"""""""
Connecting to a Rexster instance

>>> from pyblueprints import RexsterServer, RexsterGraph 
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
>>> g = Neo4jGraph('http://localhost:7474/db/data')

Creating an indexable graph object through the neo4j-rest-client API

>>> from pyblueprints.neo4j import Neo4jIndexableGraph
>>> g = Neo4jIndexableGraph('http://localhost:7474/db/data')

lease keep in mind to backup your data before trying this library.
