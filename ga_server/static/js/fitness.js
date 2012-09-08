/**
 * Different functions for the fitness function
 */
 
$(function() {
    $( "#sortable-trait" ).sortable();
    $( "#sortable-trait" ).disableSelection();
});

function playNote(note) {
        console.log('note :: ' + note);
        this.audioletApp = new AudioletAppNote(note);
    }
    
function playChord(note) {
    var intervals = new Array();
    
    $("#chordCheckboxes :input:checked").each(function() {
        intervals.push($(this).val());
    });
    
    var chord = note.add(intervals);
    this.audioletApp = new AudioletAppChord(chord);
}

function playScale(note) {
    var scale = note.scale($("#scale").val());
    this.audioletApp = new AudioletAppScale(scale);
}