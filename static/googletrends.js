function buildPlot() {
    /* data route */
  var url = "/"; 
  d3.json(url).then(function(response) {
    console.log(response);
  });
}

buildPlot();
