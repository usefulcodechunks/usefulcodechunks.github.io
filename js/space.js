


d3.csv("results.csv").then(function(data) {

  console.log(data)


  let svg = d3.select("svg#q2");
  let width = svg.attr("width");
  let height = svg.attr("height");
  let margin = { "top": 15, "right": 100, "bottom": 20, "left":100};
  let chartWidth = width - margin["left"] - margin.right;
  let chartHeight = height - margin["top"] - margin.bottom;

  let xScale = d3.scaleLinear().domain([-362599999.998328, 405400000.0]).range([0, chartWidth]);
  let yScale = d3.scaleLinear().domain([389207495.9092736, -389207495.9058842]).range([0, chartHeight]);
  let cscale = d3.scaleLinear().domain([0,1]).range(["crimson", "limegreen"])
  let cscale2 = d3.scaleLinear().domain([0,4]).range(["crimson", "limegreen"])
  let cscale3 = d3.scaleLinear().domain([2499,3200]).range(["crimson", "limegreen"])

  let cscale4 = d3.scaleLinear().domain([362600000,405400000]).range(["crimson", "limegreen"])

  for(let i=0; i < data.length; i = i + 100)
  {
      distance = Math.sqrt((data[i]["x"]*data[i]["x"])+(data[i]["y"]*data[i]["x"]))
      svg.append("circle")
          .attr("cx",xScale(data[i]["x"])+margin["left"])
          .attr("cy",yScale(data[i]["y"])+margin["top"])
          .attr("r",4)
          .attr("fill",cscale3(data[i]["packettrans"]));

      svg.append("line")
        .attr("x1", xScale(0)+margin["left"])
        .attr("y1", yScale(0)+margin["top"])
        .attr("x2",xScale(data[i]["x"])+margin["left"])
        .attr("y2",yScale(data[i]["y"])+margin["top"])
        .attr("stroke-width", 3)
        .attr("stroke", cscale4(distance))
        .attr("opacity",.4);
  }




})
