SPEED = 200,
SPACING = 300,
LISTEN=true;

$(function() {
    colors = {
            'A': '#'+(Math.random()*0xFFFFFF<<0).toString(16),
            'B': '#'+(Math.random()*0xFFFFFF<<0).toString(16),
            'C': '#'+(Math.random()*0xFFFFFF<<0).toString(16),
            'D': '#'+(Math.random()*0xFFFFFF<<0).toString(16),
            'E': '#'+(Math.random()*0xFFFFFF<<0).toString(16),
            'F': '#'+(Math.random()*0xFFFFFF<<0).toString(16),
            'G': '#'+(Math.random()*0xFFFFFF<<0).toString(16)};

    $( "#sortable-trait" ).sortable();
    $( "#sortable-trait" ).disableSelection();

    $('#listen').click(function(){
        PATTERN = [];
        // NOTES = [];

        $('div#sortable-trait > div').each(function(index) {
            PATTERN.push($(this).attr('id'));
            // NOTES.push($(this).attr('id'));
        });
        playPattern();
    });

    $("#next-song").click(function() {
        $("#ns").submit();
    });

    $("#save-order").click(function(){
        var melody = new Array();
        var indi_id = $(this).attr("href");
        $("div#sortable-trait > div").each(function(index){
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
                data: {name: note, duration:1, trait_id: index}, // 1 is quarter I believe
                success: function(){
                    console.log("SUCCESSFUL!");
                    console.log(indi_id);
                }
            });
        })  
    });

    $("#love").click(function() {
        $("#qf").submit();
    });

    $("#hate").click(function() {
        $("#qf").submit();
    });

});

function playPattern() { // playback a pattern
    //var next = Math.random() * NOTES.length >> 0,
    var i = 0;
    //PATTERN[PATTERN.length] = next;
    
    (function play() { // recursive loop to play pattern
        setTimeout( function() {
            console.log("pattern i :: "+PATTERN[i]);

            playSingle( PATTERN[i]);

            i++;

            if( i < PATTERN.length ) {
                play();
            } else {
                setTimeout( function() { LISTEN = true; }, SPEED + SPACING );
            }
        },
        SPEED + SPACING)
    })(); // end recursion
}

function playSingle(note) { // play a color/note
    MIDI.loadPlugin(function() {
        default_bg = $('#'+note).css('background-color');
        $('#'+note).css('background-color', 'white');
        MIDI.noteOn(0, MIDI.keyToNote[note], 127, 0);
        setTimeout(function() { // turn off color
            MIDI.noteOff(0, MIDI.keyToNote[note], 0);
            $('#'+note).css('background-color', default_bg);
        }, SPEED);
    });
}
