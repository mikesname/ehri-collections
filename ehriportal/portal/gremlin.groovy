//
// Experimental Groovy script for importing multiple nodes
// into Neo4j
//


def create_multiple_indexed_vertex(data,index_name,keys) {
  neo4j = g.getRawGraph()
  manager = neo4j.index()
  g.setMaxBufferSize(0)
  g.startTransaction()
  try {
    for (nodeentry in data) {
      index = manager.forNodes(index_name)
      vertex = neo4j.createNode()
      for (entry in nodeentry.entrySet()) {
        if (entry.value == null) continue;
          vertex.setProperty(entry.key,entry.value)
        if (keys == null || keys.contains(entry.key))
          index.add(vertex,entry.key,String.valueOf(entry.value))
      }
    }
    g.stopTransaction(TransactionalGraph.Conclusion.SUCCESS)
    return true;
  } catch (e) {
    g.stopTransaction(TransactionalGraph.Conclusion.FAILURE)  
    return e
  }
}
