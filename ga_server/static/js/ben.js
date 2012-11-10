SPEED = 250,
SPACING = 200,
LISTEN=true;

$(function() {
    NOTES = ['Ab2','B4','C3', 'D5','A4','A3'];
    colors = {
            'A': '#'+(Math.random()*0xFFFFFF<<0).toString(16),
            'B': '#'+(Math.random()*0xFFFFFF<<0).toString(16),
            'C': '#'+(Math.random()*0xFFFFFF<<0).toString(16),
            'D': '#'+(Math.random()*0xFFFFFF<<0).toString(16),
            'E': '#'+(Math.random()*0xFFFFFF<<0).toString(16),
            'F': '#'+(Math.random()*0xFFFFFF<<0).toString(16),
            'G': '#'+(Math.random()*0xFFFFFF<<0).toString(16)};

    $.each(NOTES, function(idx) {
        for(var k in colors) {
            if(NOTES[idx][0] == k){
                $('#sortable-trait').append('<div id='+NOTES[idx]+' style="background-color:'+colors[k]+';border:2px solid black;">'+NOTES[idx]+'</div>')
            }
        }
    });

    $( "#sortable-trait" ).sortable();
    $( "#sortable-trait" ).disableSelection();

    // $("#play").click(function() {        
    //     var audio = new Array();
    //     $("div#sortable-trait > div").each(function(index){            
    //         var note = Note.fromLatin($(this).attr('id'));
    //         console.log(note);
    //         audio.push({name: note, duration: 1});
    //     });
    //     var app = new SchedulerPlayAudio(audio);
    // });

    $('#listen').click(function(){
        PATTERN = [];
        
        $('div#sortable-trait > div').each(function(index) {
            PATTERN.push($(this).attr('id'));
        });
        
        console.log(PATTERN);
        playPattern();
    });

    $("#next-song").click(function() {
        $("#ns").submit();
    });

    $("#save-order").click(function(){
        var melody = new Array();
        var indi_id = $(this).attr("class");
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
        })//.promise().done(function() {
          //  $.post("/fitness/" + indi_id);
        //});
    });

});

function playPattern() { // playback a pattern
    //var next = Math.random() * NOTES.length >> 0,
    var i = 0;
    //PATTERN[PATTERN.length] = next;
    
    (function play() { // recursive loop to play pattern
        setTimeout( function() {
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
        MIDI.noteOn(0, MIDI.keyToNote[note], 127, 0);
        setTimeout(function() { // turn off color
            MIDI.noteOff(0, MIDI.keyToNote[note], 0);
        }, SPEED);
    });
}