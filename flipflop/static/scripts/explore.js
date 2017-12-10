queue()
.defer(d3.json, "/explore/data")
.defer(d3.json, "/static/scripts/vendor/us-states.json")
.await(makeGraphs);


function makeGraphs(error, data, statesJson) {
	if (error) throw error;
	console.log(data);
};
