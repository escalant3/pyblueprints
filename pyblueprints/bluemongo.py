#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'cocoon'
"""
    a blueprint interface to mongo db

"""
from pymongo import MongoClient
#from bson import  ObjectId
import bson

from base import Graph as IGraph
from base import Index as IIndex


class Graph(IGraph):
    """This is an abstract class that specifies all the
    methods that should be reimplemented in order to
    follow a Blueprints-like API in python"""

    def __init__(self, host='mongodb://localhost:27017/',db_name= 'graph_db'):
        """

        :param host:
        :return:
        """
        self.client = MongoClient(host)
        self.graph = self.client[db_name]
        self.db=self.graph


    def addVertex(self, _id=None):
        """Add param declared for compability with the API. Neo4j
        creates the id automatically
        @params _id: Node unique identifier

        @returns The created Vertex or None"""
        if not _id :
            node_id= self.graph.nodes.insert({})
        else :
            node_id = self.graph.nodes.insert({'_id':_id })
        node_data= self.graph.nodes.find_one({'_id':node_id})

        vertex= Vertex(node_data,self.graph)
        return vertex

    def getVertex(self, _id):
        """Retrieves an existing vertex from the graph
        @params _id: Node unique identifier

        @returns The requested Vertex or None"""
        node = self.graph.nodes.find_one({'_id':_id})
        if node :
            vertex= Vertex(node,self.graph)
            return vertex
        else:
            return None


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

        @returns The created Edge object


        individual edge id :  source_node_id | label | dest_node_id


        """
        n1 = outVertex
        n2 = inVertex

        links_id= "%s|%s" % ( str(n1.id), label)
        # find the links record
        links= self.graph.edges.find_one({'_id':links_id})
        if not links:
            # create it
            self.graph.edges.insert({'_id':links_id , 'targets':[]})
            links= self.graph.edges.find_one({'_id':links_id})

        # check unicity of target
        target_id= str(n2.id)
        found=False
        for target in links['targets']:
            if target['id'] == target_id:
                found= True
                break
        if not found:
            # ok to add
            links['targets'].append({'id':target_id})
            # update
            self.graph.edges.update({'_id':links_id}, links)


        edge_data= { 'id': target_id, 'start': str(n1.id) , 'end': str(n2.id), 'label': label}
        edge_data['_id']= "%s|%s|%s" % (str(n1.id),label,str(n2.id))


        edge= Edge(edge_data,self.graph)
        #edge = n1.relationships.create(label, n2)
        return edge

    def getEdge(self, _id):
        """Retrieves an existing edge from the graph
        @params _id: Edge unique identifier

        @returns The requested Edge or None


        the format of edge id is  source_id : label | dest_id


        """
        n1_id, label ,n2_id = _id.split('|')
        links_id= n1_id + '|' + label

        found= None
        edges = self.graph.edges.find_one({'_id':links_id})
        if edges:
            # get individual edge in links
            for edge in edges['targets']:
                if edge['id'] == n2_id:
                    found= edge
                    break
                continue
            if found:
                edge_data= { 'id': n2_id, 'start': str(n1_id) , 'end': n2_id, 'label': label}
                edge_data['_id']= _id

                edge= Edge(edge_data,self.graph)
                return edge

        return None

    def getEdges(self):
        """Returns an iterator with all the vertices"""
        raise NotImplementedError("Method has to be implemented")

    def removeEdge(self, edge):
        """Removes the given edge
        @params edge: The edge to be removed"""
        edge.neoelement.delete()

    def clear(self):
        """Removes all data in the graph database"""
        self.db.nodes.remove({})
        self.db.edges.remove({})
        self.db.indexes.remove({})

    def shutdown(self):
        """Shuts down the graph database server"""
        raise NotImplementedError("Method has to be implemented")


class TransactionalGraph(Graph):
    """An abstract class containing the specific methods
    for transacional graphs"""

    def startTransaction(self):
        """TODO Documentation"""
        raise NotImplementedError("Method has to be implemented")

    def stopTransaction(self):
        """TODO Documentation"""
        raise NotImplementedError("Method has to be implemented")

    def setTransactionMode(self):
        """TODO Documentation"""
        raise NotImplementedError("Method has to be implemented")

    def getTransactionMode(self):
        """TODO Documentation"""
        raise NotImplementedError("Method has to be implemented")


class IndexableGraph(Graph):
    """An abstract class containing the specific methods
    for indexable graphs"""

    def createManualIndex(self, indexName, indexClass):
        """TODO Documentation"""
        raise NotImplementedError("Method has to be implemented")

    def createAutomaticIndex(self, name, indexClass):
        """TODO Documentation"""
        raise NotImplementedError("Method has to be implemented")

    def getIndex(self, indexName, indexClass):
        """TODO Documentation"""
        raise NotImplementedError("Method has to be implemented")

    def getIndices(self):
        """TODO Documentation"""
        raise NotImplementedError("Method has to be implemented")

    def dropIndex(self, indexName):
        """TODO Documentation"""
        raise NotImplementedError("Method has to be implemented")


class Element():
    """An abstract class defining an Element object composed
    by a collection of key/value properties"""

    def __init__(self,  properties, graph) :
        """

        :param properties:
        :return:
        """
        self.graph= graph
        self.properties= properties
        self.id= self.properties['_id']


    def getProperty(self, key):
        """Gets the value of the property for the given key
        @params key: The key which value is being retrieved

        @returns The value of the property with the given key"""
        #raise NotImplementedError("Method has to be implemented")
        return self.properties.get(key,None)

    def getPropertyKeys(self):
        """Returns a set with the property keys of the element

        @returns Set of property keys"""
        #raise NotImplementedError("Method has to be implemented")
        return self.properties

    def setProperty(self, key, value):
        """Sets the property of the element to the given value
        @params key: The property key to set
        @params value: The value to set"""
        #raise NotImplementedError("Method has to be implemented")
        self.properties[key]=value
        self._update_node(self.properties)

    def getId(self):
        """Returns the unique identifier of the element

        @returns The unique identifier of the element"""
        return self.id

    def removeProperty(self, key):
        """Removes the value of the property for the given key
        @params key: The key which value is being removed"""
        raise NotImplementedError("Method has to be implemented")

    # privates
    def _oid(self,id):
        """

        :param key:
        :return:
        """
        try:
            # test if it is an objectid
            return bson.ObjectId(id)
        except bson.errors.InvalidId:
            return id

    def _fetch_node(self,id):
        """

        :param id:
        :return:
        """
        key = {'_id':id}
        try:
            # test if it is an objectid
            oid= bson.ObjectId(id)
            key = {'_id':oid}
        except bson.errors.InvalidId:
            pass
        node= self.graph.nodes.find_one(key)
        return node
        #return Vertex(node,self.graph)

    def _update_node(self,properties):
        """

        :param id:
        :param properties:
        :return:
        """
        self.graph.nodes.update({'_id':self.properties['_id']}, properties)


class Vertex(Element):
    """An abstract class defining a Vertex object representing
    a node of the graph with a set of properties"""

    def getOutEdges(self, label=None):
        """Gets all the outgoing edges of the node. If label
        parameter is provided, it only returns the edges of
        the given label
        @params label: Optional parameter to filter the edges

        @returns A generator function of edges"""
    #def outgoing(self,types=None):
        """

            iterate  edges  like  $id | $type for all type in types

        """
        types=label
        types= types or []
        if isinstance(types,basestring):
            types= [types]
        if not types:
            raise NotImplementedError("fectching all outgoing not implemented")

        for type in types:
            _id= "%s|%s" % ( self.id,type)
            links = self.graph.edges.find_one({'_id':_id})
            if links:
                #print links
                for link in links['targets']:
                    n1_id= self.id
                    n2_id= link['id']
                    edge_data= { 'id': n2_id, 'start': str(n1_id) , 'end': n2_id, 'label': label}
                    edge_data['_id']= _id + '|' + str(n1_id)

                    edge= Edge(edge_data,self.graph)
                    yield edge
                    #neoelement= NeoElement(edge_data,self.parent.graph)
                    #yield neoelement
                    #edge= Edge(neoelement)
                    #yield edge

        return

    def getInEdges(self, label=None):
        """Gets all the incoming edges of the node. If label
        parameter is provided, it only returns the edges of
        the given label
        @params label: Optional parameter to filter the edges

        @returns A generator function of edges"""
        raise NotImplementedError("Method has to be implemented")

    def getBothEdges(self, label=None):
        """Gets all the edges of the node. If label
        parameter is provided, it only returns the edges of
        the given label
        @params label: Optional parameter to filter the edges

        @returns A generator function of edges"""
        raise NotImplementedError("Method has to be implemented")

class Edge(Element):
    """An abstract class defining a Edge object representing
    a relationship of the graph with a set of properties"""

    def __init__(self,  properties, graph) :
        """

        :param properties:
        :param graph:
        :return:
        """
        Element.__init__(self,properties,graph)
        self.start= properties['start']
        self.end= properties['end']
        self.label= properties['label']


    def getOutVertex(self):
        """Returns the origin Vertex of the relationship

        @returns The origin Vertex"""
        empty_node= { '_id': self.start  }
        #node= self.graph.nodes.find_one(empty_node)
        node=self._fetch_node(self.start)

        if not node:
            # node absent: create it
            self.graph.nodes.insert(empty_node)
            node = empty_node
        vertex= Vertex(node,self.graph)
        return vertex

    def getInVertex(self):
        """Returns the target Vertex of the relationship

        @returns The target Vertex"""
        #return Vertex(self.neoelement.end)
        empty_node= { '_id': self.end  }
        #node= self.graph.nodes.find_one(empty_node)
        node=self._fetch_node(self.end)
        if not node:
            # node absent: create it
            self.graph.nodes.insert(empty_node)
            node = empty_node
        vertex= Vertex(node,self.graph)
        return vertex

    def getLabel(self):
        """Returns the label of the relationship

        @returns The edge label"""
        #return self.neoelement.type
        return self.label

    def __str__(self):
        return "Edge %s: %s" % (self.id,
                                self.properties)

    def setProperty(self, key, value):
        """Sets the property of the element to the given value
        @params key: The property key to set
        @params value: The value to set"""
        #raise NotImplementedError("Method has to be implemented")
        # update property in cache
        self.properties[key]= value

        # get links to update the record
        links_id= "%s|%s" % ( self.start,self.label)
        links = self.graph.edges.find_one({'_id': links_id})
        if not links:
            raise ValueError("no such links for %s" % self.id )
        # find the right edge
        for link in links['targets']:
            if link['id'] == self.end:
                # update it
                link[key]= value
                break
        # update it
        self.graph.edges.update({'_id':links_id}, links)
        return value




    def removeProperty(self, key):
        """Removes the value of the property for the given key
        @params key: The key which value is being removed"""
        raise NotImplementedError("Method has to be implemented")



class Index(IIndex):
    """An abstract class containing all the methods needed to
    implement an Index object


    structure of indexes

    name:key


    """

    # def __init__(self, indexName, indexClass, indexType, indexObject,graph):
    #     if indexClass != "vertex" and indexClass != "edge":
    #         raise NameError("%s is not a valid Index Class" % indexClass)
    #     self.indexClass = indexClass
    #     self.indexName = indexName
    #     if indexType != "automatic" and indexType != "manual":
    #         raise NameError("%s is not a valid Index Type" % indexType)
    #     self.indexType = indexType
    #     if not isinstance(indexObject, client.Index):
    #         raise TypeError("""%s is not a valid
    #                         neo4jrestclient.client.Index
    #                         instance""" \
    #                         % type(indexObject))
    #     self.neoindex = indexObject



    def count(self, key, value):
        raise NotImplementedError("Method has to be implemented")

    def getIndexName(self):
        """TODO Documentation"""
        raise NotImplementedError("Method has to be implemented")

    def getIndexClass(self):
        """TODO Documentation"""
        raise NotImplementedError("Method has to be implemented")

    def getIndexType(self):
        """TODO Documentation"""
        raise NotImplementedError("Method has to be implemented")

    def put(self, key, value, element):
        """TODO Documentation"""
        raise NotImplementedError("Method has to be implemented")

    def get(self, key, value):
        """TODO Documentation"""
        raise NotImplementedError("Method has to be implemented")

    def remove(self, key, value, element):
        """TODO Documentation"""
        raise NotImplementedError("Method has to be implemented")


class AutomaticIndex(Index):
    """An abstract class containing the specific methods for an
    automatic index"""

    def getAutoIndexKeys(self):
        raise NotImplementedError("Method has to be implemented")



if __name__=="__main__":


    mg= Graph()

    mg.clear()

    #mg.db.nodes.remove({})
    #mg.db.edges.remove({})
    #mg.db.relationships.remove({})

    v1= mg.addVertex()
    v2= mg.addVertex( _id='t:1')
    v3= mg.addVertex(_id= 't:2')
    #
    v1_id = v1.getId()
    v2_id = v2.getId()
    #
    v1= mg.getVertex(v1_id)
    v2= mg.getVertex(v2_id)
    #
    #
    edge_v1_V2= mg.addEdge(v1,v2,'son')
    edge_v1_V2_duplicate= mg.addEdge(v1,v2,'son')
    edge_v1_V3= mg.addEdge(v1,v3,'son')
    #
    e_v1_v2_older= mg.addEdge(v1,v2,'older')
    #
    r_id= edge_v1_V2.getId()
    #
    #
    #
    edge= mg.getEdge(r_id)
    #
    n1= edge.getOutVertex()
    n2= edge.getInVertex()
    # label= edge.getLabel()
    #
    #
    #
    # out_v1= list(v1.neoelement.relationships.outgoing(['son']))
    #
    out_v1= list(v1.getOutEdges('son'))


    note= v1.getProperty('note')

    v1.setProperty('note'," my node")

    note= v1.getProperty('note')


    note= edge_v1_V2.getProperty('note')

    edge_v1_V2.setProperty('note',"my edge note")



    print
