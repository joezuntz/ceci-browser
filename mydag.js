
function visualize_graph(nodes, edges) { 
    // Create a new directed graph 
    var g = new dagre.graphlib.Graph();

    // Set an object for the graph label
    g.setGraph({});

    // Default to assigning a new object as a label for each new edge.
    g.setDefaultEdgeLabel(function() { return {}; });

    console.log(nodes);
    console.log(edges);
    nodes.forEach(function(node) {
        // console.log(node[0]);
        g.setNode(node[0], { label: node[0],  width: 144, height: 30 });
    });

    edges.forEach(function(edge) {
        // console.log(edge[0], edge[1]);
        g.setEdge(edge[0], edge[1]);
    });

    // Create the renderer
    var render = new dagreD3.render();

    // Set up an SVG group so that we can translate the final graph.
    var svg = d3.select("svg"),  svgGroup = svg.append("g");

    // Run the renderer. This is what draws the final graph.
    render(d3.select("svg g"), g);

    // // Center the graph
    // var xCenterOffset = (svg.attr("width") - g.graph().width) / 2;
    // svgGroup.attr("transform", "translate(" + xCenterOffset + ", 20)");
    // svg.attr("height", g.graph().height + 40);


}
