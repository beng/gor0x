$(function() {
    var audio = new Array();
    for(var i = 0; i < 4; i++){
        console.log('pushing to audio');
        audio.push({name: Note.fromLatin("A6"), duration: 1});
        audio.push({name: Note.fromLatin("C#4"), duration: 2});
        audio.push({name: Note.fromLatin("B3"), duration: 1});
    }
    var app = new SchedulerPlayAudio(audio);
    console.log(app);
});