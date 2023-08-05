# Firehawk

Experimental Language and REPL

# Installation

    pip install firehawk
   
You will also need the DSE Graph driver.  That's up to you for now.   

# Code Examples

    > from firehawk import parse_line
    > query = parse_line("CREATE VERTEX person")
    
    > type(query)
    firehawk.ddl.CreateVertex
    
    > print query
    schema = graph.schema()
    schema.buildVertexLabel('person').add()
    
# REPL

This package provides a REPL.  

    graph [name]
    
# Supported Syntax
    
    create graph [graph]
    use [graph]
    create vertex [label]
    create edge [label]
    create property [name] [type]
    CREATE [materialized|secondary|search] INDEX [name] ON VERTEX [label]([field])
    CREATE [in|out] INDEX [name] ON VERTEX [vertex-label] ON EDGE [edge-label]([edge-property])

    
