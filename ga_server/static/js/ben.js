$(function() {
    $( "#sortable-trait" ).sortable();
    $( "#sortable-trait" ).disableSelection();

    $("#play").click(function() {
        var audio = new Array();
        $("ul#sortable-trait > div").each(function(index){
            var note = Note.fromLatin($(this).attr('id'));
            audio.push({name: note, duration: 1});
        });
        var app = new SchedulerPlayAudio(audio);
    })
});