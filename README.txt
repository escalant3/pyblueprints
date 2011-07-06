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


Please keep in mind to backup your data before trying this library.
