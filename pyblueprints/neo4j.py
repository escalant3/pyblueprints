#!/usr/bin/env python
#-*- coding:utf-8 -*-

#####################################################################
# A set of classes implementing Blueprints API for Neo4j engine.    #
#                                                                   #
# File: pyblueprints/neo4j.py                                       #
#####################################################################

from neo4jrestclient import client 
from base import Graph


class Neo4jDatabaseConnectionError(Exception):

    def __init__(self, url, *args, **kwargs):
        self.url = url

    def __str__(self):
        return "Unable to connect to \"%s\"" % self.url


class Neo4jGraph(Graph):

    def __init__(self, host):
        try:
            self.neograph = client.GraphDatabase(host)
        except client.NotFoundError:
            raise Neo4jDatabaseConnectionError(host)
        except ValueError:
            raise Neo4jDatabaseConnectionError(host)

    def addVertex(self, _id=None):
        """Add param declared for compability with the API. Neo4j
        creates the id automatically
        @params _id: Node unique identifier

        @returns The created Vertex or None"""
        node = self.neograph.nodes.create(_id=_id)
        return Vertex(node)

    def getVertex(self, _id):
        """Retrieves an existing vertex from the graph
        @params _id: Node unique identifier

        @returns The requested Vertex or None"""
        try:
            node = self.neograph.nodes.get(_id)
        except client.NotFoundError:
            return None
        return Vertex(node)

    def getVertices(self):
        """Returns an iterator with all the vertices"""
        raise NotImplementedError("Method has to be implemented")

    def removeVertex(self, vertex):
        """Removes the given vertex
        @params vertex: Node to be removed"""
        vertex.neoelement.delete()

    def addEdge(self, outVertex, inVertex, label):
        """Creates a new edge
        @params outVertex: Edge origin Vertex
        @params inVertex: Edge target vertex
        @params label: Edge label

        @returns The created Edge object"""
        n1 = outVertex.neoelement
        n2 = inVertex.neoelement
        edge = n1.relationships.create(label, n2)
        return Edge(edge)

    def getEdge(self, _id):
        """Retrieves an existing edge from the graph
        @params _id: Edge unique identifier

        @returns The requested Edge or None"""
        try:
            edge = self.neograph.relationships.get(_id)
        except client.NotFoundError:
            return None
        return Edge(edge)

    def getEdges(self):
        """Returns an iterator with all the vertices"""
        raise NotImplementedError("Method has to be implemented")

    def removeEdge(self, edge):
        """Removes the given edge
        @params edge: The edge to be removed"""
        edge.neoelement.delete()

    def clear(self):
        """Removes all data in the graph database"""
        raise NotImplementedError("Method has to be implemented")

    def shutdown(self):
        """Shuts down the graph database server"""
        raise NotImplementedError("Method has to be implemented")


class Element(object):
    """An class defining an Element object composed
    by a collection of key/value properties for the
    Neo4j database"""

    def __init__(self, neoelement):
        """Constructor
        @params neolement: The Neo4j element to be transformed"""
        self.neoelement = neoelement

    def getProperty(self, key):
        """Gets the value of the property for the given key
        @params key: The key which value is being retrieved

        @returns The value of the property with the given key"""
        return self.neoelement.get(key)

    def getPropertyKeys(self):
        """Returns a set with the property keys of the element

        @returns Set of property keys"""
        return self.neoelement.properties.keys()

    def setProperty(self, key, value):
        """Sets the property of the element to the given value
        @params key: The property key to set
        @params value: The value to set"""
        self.neoelement.set(key, value)

    def getId(self):
        """Returns the unique identifier of the element

        @returns The unique identifier of the element"""
        return self.neoelement.id

    def removeProperty(self, key):
        """Removes the value of the property for the given key
        @params key: The key which value is being removed"""
        self.neoelement.delete(key)


class Vertex(Element):
    """An abstract class defining a Vertex object representing
    a node of the graph with a set of properties"""

    def getOutEdges(self, label=None):
        """Gets all the outgoing edges of the node. If label
        parameter is provided, it only returns the edges of
        the given label
        @params label: Optional parameter to filter the edges

        @returns A generator function with the outgoing edges"""
        if label:
            for edge in self.neoelement.relationships.outgoing(types=[label]):
                yield Edge(edge)
        else:
            for edge in self.neoelement.relationships.outgoing():
                yield Edge(edge)

    def getInEdges(self, label=None):
        """Gets all the incoming edges of the node. If label
        parameter is provided, it only returns the edges of
        the given label
        @params label: Optional parameter to filter the edges

        @returns A generator function with the incoming edges"""
        if label:
            for edge in self.neoelement.relationships.incoming(types=[label]):
                yield Edge(edge)
        else:
            for edge in self.neoelement.relationships.incoming():
                yield Edge(edge)

    def getBothEdges(self, label=None):
        """Gets all the edges of the node. If label
        parameter is provided, it only returns the edges of
        the given label
        @params label: Optional parameter to filter the edges

        @returns A generator function with the incoming edges"""
        if label:
            for edge in self.neoelement.relationships.all(types=[label]):
                yield Edge(edge)
        else:
            for edge in self.neoelement.relationships.all():
                yield Edge(edge)


    def __str__(self):
        return "Vertex %s: %s" % (self.neoelement.id,
                                self.neoelement.properties)


class Edge(Element):
    """An abstract class defining a Edge object representing
    a relationship of the graph with a set of properties"""

    def getOutVertex(self):
        """Returns the origin Vertex of the relationship

        @returns The origin Vertex"""
        return Vertex(self.neoelement.start)

    def getInVertex(self):
        """Returns the target Vertex of the relationship

        @returns The target Vertex"""
        return Vertex(self.neoelement.end)

    def getLabel(self):
        """Returns the label of the relationship

        @returns The edge label"""
        return self.neoelement.type

    def __str__(self):
        return "Edge %s: %s" % (self.neoelement.id,
                                self.neoelement.properties)


class Index(object):
    """An class containing all the methods needed by an
    Index object"""

    def __init__(self, indexName, indexClass, indexType, indexObject):
        if indexClass != "vertex" and indexClass != "edge":
            raise NameError("%s is not a valid Index Class" % indexClass)
        self.indexClass = indexClass
        self.indexName = indexName
        if indexType != "automatic" and indexType != "manual":
            raise NameError("%s is not a valid Index Type" % indexType)
        self.indexType = indexType
        if not isinstance(indexObject, client.Index):
            raise TypeError("""%s is not a valid
                            neo4jrestclient.client.Index
                            instance""" \
                            % type(indexObject))
        self.neoindex = indexObject

    def count(self, key, value):
        """Returns the number of elements indexed for a
        given key-value pair
        @params key: Index key string
        @params outVertex: Index value string

        @returns The number of elements indexed"""
        return len(self.neoindex[key][value])

    def getIndexName(self):
        """Returns the name of the index

        @returns The name of the index"""
        return self.indexName

    def getIndexClass(self):
        """Returns the index class (vertex or edge)

        @returns The index class"""
        return self.indexClass

    def getIndexType(self):
        """Returns the index type (automatic or manual)

        @returns The index type"""
        return self.indexType

    def put(self, key, value, element):
        """Puts an element in an index under a given
        key-value pair
        @params key: Index key string
        @params value: Index value string
        @params element: Vertex or Edge element to be indexed"""
        self.neoindex[key][value] = element.neoelement

    def get(self, key, value):
        """Gets an element from an index under a given
        key-value pair
        @params key: Index key string
        @params value: Index value string
        @returns A generator of Vertex or Edge objects"""
        for element in self.neoindex[key][value]:
            if self.indexClass == "vertex":
                yield Vertex(element)
            elif self.indexClass == "edge":
                yield Edge(element)
            else:
                raise TypeError(self.indexClass)

    def remove(self, key, value, element):
        """Removes an element from an index under a given
        key-value pair
        @params key: Index key string
        @params value: Index value string
        @params element: Vertex or Edge element to be removed"""
        self.neoindex.delete(key, value, element.neoelement)

    def __str__(self):
        return "Index: %s (%s, %s)" % (self.indexName,
                                        self.indexClass,
                                        self.indexType)


class Neo4jIndexableGraph(Neo4jGraph):
    """An class containing the specific methods
    for indexable graphs"""

    def createManualIndex(self, indexName, indexClass):
        """Creates an index manually managed
        @params name: The index name
        @params indexClass: vertex or edge

        @returns The created Index"""
        indexClass = str(indexClass).lower()
        if indexClass == "vertex":
            index = self.neograph.nodes.indexes.create(indexName)
        elif indexClass == "edge":
            index = self.neograph.relationships.indexes.create(indexName)
        else:
            NameError("Unknown Index Class %s" % indexClass)
        return Index(indexName, indexClass, "manual", index)

    def createAutomaticIndex(self, indexName, indexClass):
        """Creates an index automatically managed my Neo4j
        @params name: The index name
        @params indexClass: vertex or edge

        @returns The created Index"""
        raise NotImplementedError("Method has to be implemented")

    def getIndex(self, indexName, indexClass):
        """Retrieves an index with a given index name and class
        @params indexName: The index name
        @params indexClass: vertex or edge

        @return The Index object or None"""
        if indexClass == "vertex":
            try:
                return Index(indexName, indexClass, "manual",
                        self.neograph.nodes.indexes.get(indexName))
            except client.NotFoundError:
                return None
        elif indexClass == "edge":
            try:
                return Index(indexName, indexClass, "manual",
                        self.neograph.relationships.indexes.get(indexName))
            except client.NotFoundError:
                return None
        else:
            raise KeyError("Unknown Index Class (%s). Use vertex or edge"\
                    % indexClass)

    def getIndices(self):
        """Returns a generator function over all the existing indexes

        @returns A generator function over all rhe Index objects"""
        for indexName in self.neograph.nodes.indexes.keys():
            indexObject = self.neograph.nodes.indexes.get(indexName)
            yield Index(indexName, "vertex", "manual", indexObject)
        for indexName in self.neograph.relationships.indexes.keys():
            indexObject = self.neograph.relationships.indexes.get(indexName)
            yield Index(indexName, "edge", "manual", indexObject)

    def dropIndex(self, indexName, indexClass):
        index = self.getIndex(indexName, indexClass)
        index.neoindex.delete()


class Neo4jTransactionalGraph(Neo4jGraph):
    """An class containing the specific methods
    for transacional graphs"""

    _transaction = False
    _txObj = None

    def startTransaction(self):
        self._txObj = self.neograph.transaction(commit=False)
        self._transaction = True

    def stopTransaction(self):
        self._txObj.commit()
        self._txObj.__exit__(None, None, None)
        self._txObj = None
        self._transaction = False


class Neo4jTransactionalIndexableGraph(Neo4jTransactionalGraph, Neo4jIndexableGraph):
    pass
