var source = new EventSource('/event_source');

function IndividualStats(div_id) {
    this.div_id = div_id;
};

source.addEventListener('message', function(e) {
    // TODO: push IndividualStats to HTML
    var individual_stats = JSON.parse(e.data);
    var div_id = document.getElementById("ga-stats");
    var is = new IndividualStats(div_id);
    IndividualStats.prototype.id = individual_stats.id;
    IndividualStats.prototype.fitness = individual_stats.fitness;
    IndividualStats.prototype.generation_score = individual_stats.gen_score;
}, false);

source.addEventListener('open', function(e) {
    console.log(e);
    console.log('connection opened');
}, false);

source.addEventListener('error', function(e) {
    if (e.readyState == EventSource.CLOSED) {
        console.log('connection closed');
    }
})
