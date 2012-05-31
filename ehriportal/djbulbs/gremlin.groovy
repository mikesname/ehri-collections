
// For a node that can only have a type of
// relation pointing to one entity, set
// the target node, removing any existing
// relation if necessary
def set_single_relation(outV, inV, label) {
  import org.neo4j.graphdb.DynamicRelationshipType;
  neo4j = g.getRawGraph()
  manager = neo4j.index()
  outvertex = neo4j.getNodeById(outV)
  index = manager.forRelationships(label)
  g.setMaxBufferSize(0)
  g.startTransaction()

  try {
    try {
      def existing = g.v(outV).outE(label).next()
      index.remove(neo4j.getRelationshipById(existing.id))
      g.removeEdge(existing)
    } catch (NoSuchElementException e) {
    }
    if (inV != null) {
      def relationshipType = DynamicRelationshipType.withName(label)
      def edge = outvertex.createRelationshipTo(neo4j.getNodeById(inV), relationshipType)
      index.add(edge, "label", String.valueOf(label))
    }
    g.stopTransaction(TransactionalGraph.Conclusion.SUCCESS)
    return true;
  } catch (e) {
    g.stopTransaction(TransactionalGraph.Conclusion.FAILURE)  
    return e
  }
}


// construct a query - several of these paths can probably
// be optimised, and I'm not sure if the index is being
// used as much as it could be.
def query(index_name, relations, filters, high, low, order_by, docount) {
  try {
    def opblocks = [
      "exact":   {it, a, v -> it."$a" == v},
      "iexact":  {it, a, v -> it."$a".toLowerCase() == v.toLowerCase()},
      "contains":{it, a, v -> it."$a".matches(".+$v.+")},
      "startswith":{it, a, v -> it."$a".matches("^$v.+")},
      "endswith":{it, a, v -> it."$a".matches(".+$v\$")},
      "isnull":  {it, a, v -> it."$a" == null},
      "gt":      {it, a, v -> it."$a" >  v},
      "lt":      {it, a, v -> it."$a" <  v},
      "gte":     {it, a, v -> it."$a" >= v},
      "lte":     {it, a, v -> it."$a" <= v},
    ]

    def pipe = g.V

    for (relation in relations) {
      def (relname, outV) = relation
      pipe = g.v(outV).inE(relname).outV
    }

    if (index_name != null)
      pipe = pipe.filter{it.element_type==index_name}

    for (filter in filters) {
      def (attr, op, value) = filter

      def opblock = opblocks.get(op)
      if (opblock == null)
        throw new Exception("Unsupported filter operator: '$op'")
      pipe = pipe.filter{opblock(it, attr, value)}
    }
    
    if (!docount && low != null && high != null) {
      if (low != 0 && high == null)
        pipe = pipe.range(low, -1)
      else if (low == 0 && high != null)
        pipe = pipe.range(0, high)
      else if (low > 0 && high != null)
        pipe = pipe.range(low, high)
    }
  
    if (order_by != null && order_by) {
      for (order in order_by) {
        def (attr, desc) = order
        pipe = pipe.sort{it."$attr"}
        if (desc)
          pipe = pipe.reverse()
      }
    }

    if (docount)
      return pipe.count()
    return pipe
  } catch (e) {
    return e
  }
}



