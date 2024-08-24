let active = false
var socket = io()

socket.on('connect', function() {
    socket.emit('event', {data: 'I\'m connected!'});
});

$("#execute").click(function(event){
    if ($("#function-switcher").text() === "SOLVE"){
        if (active){
            $("input").val("")
            $("input").prop("disabled", false)
            $(".locked").removeClass("locked")
            $("#execute").html("execute")
            active = false
        } else {
            let board = []
            let textboxes = []
            for(let i = 0; i < 81; i++){
                let value = parseInt($($($("#board").children()[i]).children()[0]).val())
                $($($("#board").children()[i]).children()[0]).prop("disabled", true)
                board.push(value)
                textboxes.push($($($("#board").children()[i]).children()[0]))
                if(value){$($("#board").children()[i]).addClass("locked")};
            }

            socket.emit('empty-board', {data: board})
            socket.on("filled-board", function(data) {
                console.log(data)
                let counter = 0
                for(let i = 0; i < 81; i++){
                    if(counter==9){counter=0}
                    $($($("#board").children()[i]).children()[0]).val(data[i])
                    counter++
                }
            })

            $("#execute").html("reset")
            active = true
            
        }
    } else {
        
    }   
});

$("#function-switcher").on("click",function(){
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

$('input').keydown(function(e) {
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