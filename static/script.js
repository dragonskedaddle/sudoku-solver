var socket = io()

$("#execute").click(function(){
    let board = []

    for(let i = 0; i < 81; i++){  // sets board up 
        let value = parseInt($($($("#board").children()[i]).children()[0]).val())
        if($("#function-switcher").text() === "SOLVE"){$($($("#board").children()[i]).children()[0]).prop("disabled", true)} // if in SOLVE mode disable all textboxes
        board.push(value)

        if(value && $("#function-switcher").text() === "SOLVE"){$($("#board").children()[i]).addClass("locked")}; // if in SOLVE mode and a text box has a value add the locked class

        if($("#function-switcher").text() === "GENERATE"){ // when in GENERATE mode ensure that all locked textboxes are removed and all inputs can be edited
            $(".locked").removeClass("locked")
            $("input").prop("disabled", false)
        }
    }

    if ($("#function-switcher").text() === "SOLVE"){ // emit the correct signal based on user choice 
        socket.emit('empty-board', {data: board})
    } else{
        socket.emit('generate-board', {data: board})
    }

    socket.on("filled-board", function(data) { // displays the solved/generated board
        let counter = 0

        for(let i = 0; i < 81; i++){
            if(counter==9){counter=0}
            if(data[i] === 0){
                $($($("#board").children()[i]).children()[0]).val(null)
            } else{
                $($($("#board").children()[i]).children()[0]).val(data[i])
            }

            counter++
        }
    })

    $("#reset").prop("disabled", false) // enables reset button
});

$("#reset").click(function(){
    $("input").val("") // clears all text boxes
    $("input").prop("disabled", false) // renables all text boxes
    $(".locked").removeClass("locked") // removes all locked clases
    $("#reset").prop("disabled", true) // disables button after use
})

$("#function-switcher").on("click",function(){ // switch modes
    if ($("#function-switcher").text() === "SOLVE"){ 
        $("#function-switcher").text("GENERATE") 
    } else {
        $("#function-switcher").text("SOLVE") 
    }
})

function randomInt(min, max){ // The maximum is exclusive and the minimum is inclusive
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min) + min); 
}

function navigate(origin, sens) { // navigates the grid 
    var inputs = $('#board').find('input:enabled');
    var index = inputs.index(origin);
    index += sens;
    if (index < 0) {
        index = inputs.length - 1;
    }
    if (index > inputs.length - 1) {
        index = 0;
    }
    inputs.eq(index).focus()
    inputs.eq(index).on("keyup", function(e){if([37,38,39,40].includes(e.keyCode)){(e.target).select()};})
}

$('input').keydown(function(e) { // use of arrow key 
    if (e.keyCode==37) {
        navigate(e.target, -1);
    }
    if (e.keyCode==38) {
        navigate(e.target, -9);
    }
    if (e.keyCode==39) {
        navigate(e.target, 1);
    }
    if (e.keyCode==40) {
        navigate(e.target, 9);
    }
})