//
// Experimental Groovy script for importing multiple nodes
// into Neo4j
//


def ingest_portal_data(data, relations) {
  import org.neo4j.graphdb.DynamicRelationshipType;
  neo4j = g.getRawGraph()
  manager = neo4j.index()
  g.setMaxBufferSize(0)
  g.startTransaction()

  def create_relation(outV, inV, label) {
    def relationshipType = DynamicRelationshipType.withName(label)
    def index = manager.forRelationships(label)
    def edge = outV.createRelationshipTo(inV, relationshipType)
    index.add(edge, "label", String.valueOf(label))
  }

  def create_vertex(index_name, data, keys=null) {
    def index = manager.forNodes(index_name)
    def vertex = neo4j.createNode()
    for (entry in data.entrySet()) {
      if (entry.value == null)
        continue;

      // if this attribute signifies a relation, find
      // the related entity and create it.
      def rel = relations.get(index_name + "." + entry.key)
      if (rel != null) {
        def (relname, relclass) = rel
        def (slug) = entry.value
        def rel_index = manager.forNodes(relclass)
        def inV = rel_index.get("slug", slug).getSingle()
        create_relation(vertex, inV, relname)
      } else {
        vertex.setProperty(entry.key, entry.value)
        if (keys == null || keys.contains(entry.key)) {
          index.add(vertex, entry.key, String.valueOf(entry.value))
        }
      }
    }
    return vertex;
  }

  try {
    i = 0
    for (item in data) {
      index_name = item["fields"]["element_type"]
      create_vertex(index_name, item["fields"])
      i++
    }
    g.stopTransaction(TransactionalGraph.Conclusion.SUCCESS)
    return i;
  } catch (e) {
    g.stopTransaction(TransactionalGraph.Conclusion.FAILURE)  
    return e
  }
}




def create_multiple_indexed_vertex(dataitems,index_name,keys) {
  neo4j = g.getRawGraph()
  manager = neo4j.index()
  g.setMaxBufferSize(0)
  g.startTransaction()
  try {
    index = manager.forNodes(index_name)
    i = 0
    for (data in dataitems) {
      vertex = neo4j.createNode()
      for (entry in data.entrySet()) {
        if (entry.value == null) continue;
        vertex.setProperty(entry.key,entry.value)
        if (keys == null || keys.contains(entry.key)) {
          index.add(vertex,entry.key,String.valueOf(entry.value))
        }
      }
      i++
    }
    g.stopTransaction(TransactionalGraph.Conclusion.SUCCESS)
    return true;
  } catch (e) {
    g.stopTransaction(TransactionalGraph.Conclusion.FAILURE)  
    return e
  }
}
