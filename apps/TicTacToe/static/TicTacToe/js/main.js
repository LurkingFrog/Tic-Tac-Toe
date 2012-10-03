var current_players = {
    "player_x": "person",
    "player_y": "computer"
}

var current_board = "000000000"


// A function to switch between computer and human players
function toggle_player(player) {
    var src = $("img#" + player + "_img").attr("src");

    if (current_players[player] == "person") {
	current_players[player] = "computer";
	src = src.replace("person", "computer");
	    
    } else {
	current_players[player] = "person";
	src = src.replace("computer", "person");
    }

    $("img#" + player + "_img").attr("src", src);
}

// An ajax call to the server to get the next board
function get_next_move() {

}


// Toggle the board images to display the current
// state of the board
function draw_board(board_id, winner) {

}