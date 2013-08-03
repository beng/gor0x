$(function($) {
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
