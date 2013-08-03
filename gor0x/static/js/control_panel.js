function update_score(score){
    $('.current_score')
    .val(score)
    .trigger('change');
}

$(function($) {
    setInterval(function() {
        var score = IndividualStats.prototype.generation_score;
        update_score(score);
    }, 3000);

    $(".knob").knob({
        change : function (value) {
            console.log(this.$);
            // console.log("change : " + value);
        },
        release : function (value) {
            console.log("release : " + value);
        },
        cancel : function () {
            console.log("cancel : ", this);
        }
    });
});
