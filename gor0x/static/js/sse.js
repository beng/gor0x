var source = new EventSource('/event_source');

source.addEventListener('message', function(e) {
    var data = JSON.parse(e.data);
    document.body.innerHTML += data.id + " : " + data.fitness + '<br>';
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
