$(function() {
    $( "#sortable-trait" ).sortable();
    $( "#sortable-trait" ).disableSelection();

    $("#play").click(function() {
        var audio = new Array();
        $("ul#sortable-trait > div").each(function(index){
            var note = Note.fromLatin($(this).attr('id'));
            console.log(note);
            audio.push({name: note, duration: 1});
        });
        var app = new SchedulerPlayAudio(audio);
    });

    $("#submit-individual").click(function(){
        var melody = new Array();
        var indi_id = $(this).attr("class");
        $("ul#sortable-trait > div").each(function(index){
            /*  If I don't do it like this, then web.py WILL NOT
                receive duplicate objects (e.g. if the notes are
                C3 C3 A4 then webpy will only get 1 C3 and 1 A4).
                Ignore the multiple web requests -- doesn't matter.
            */
            var note = $(this).attr('id');
            $.ajax({
                type: 'POST',
                async: false,
                url: '/save_fitness/' + indi_id,
                data: {name: note, duration:10, trait_id: index}, // 1 is quarter I believe
                success: function(){
                    console.log("SUCCESSFUL!");
                    console.log(indi_id);
                }
            });
        })//.promise().done(function() {
          //  $.post("/fitness/" + indi_id);
        //});
    });
});

