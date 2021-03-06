var current_players = {
    "player_x": "person",
    "player_o": "computer"
}

var turn = "player_x"
var current_board = "000000000"


// A function to switch between computer and human players

// There seems to be a race condition sometimes causing
// a random error "Cannot call method 'replace' of undefined" 
function toggle_player(player) {
    var src = $("img#" + player + "_img").attr("src");

    try {
	if (current_players[player] == "person") {
	    current_players[player] = "computer";
	    src = src.replace("person", "computer");
	    
	} else {
	    current_players[player] = "person";
	    src = src.replace("computer", "person");
	}
	
    } catch(err) {
//	alert($("img#" + player + "_img").attr("src") + "\n  " + src);
    }

    $("img#" + player + "_img").attr("src", src);
    
    if (current_players[turn] == "computer") {
	get_next_move();
    }

}

// An ajax call to the server to get the next board
function get_next_move() {
    $.ajax({
	url: "/move/" + current_board,
	dataType: 'json',
	success: function(data) {
	    finish_turn(data["new_board"], data["winner"]);
	}
    });
}


// For humans clicking 
function make_move(square_id) {
    if (current_players[turn] != "person") {
	alert("Please wait for the computer to finish its turn");
	return;
    }

    square = parseInt(square_id.charAt(square_id.length-1));
    
    if (current_board.charAt(square) != "0") {
	alert("That square has already been played");
	return;
    }
	
    move = (turn=="player_x")? "1" : "2"
    b = current_board
    current_board = b.substr(0, square) + move + b.substr(square + 1);
    
    $.ajax({
	url: "/win/" + current_board,
	dataType: 'json',
	success: function(data) {
	    finish_turn(current_board, data["winner"]);
	}
    });
}


// a simple helper function to end a turn
function finish_turn(board, winner) {
    if (turn=="player_x") {
	turn = "player_o";
    } else {
	turn = "player_x";
    }
    draw_board(board, winner); 
    current_board = board;
}


// Toggle the board images to display the current
// state of the board
function draw_board(board_id, winners) {
    var src = $("#game_board #square_0 img").attr("src");
    var path = src.substring(0, src.lastIndexOf("/"));

    for (i=0; i < 9; i++) {
	switch(board_id.charAt(i)) {
	case '0':
	    $("#game_board #square_" + i + " img").attr("src", path + "/blank.gif");
	    break;
	case '1':
	    $("#game_board #square_" + i + " img").attr("src", path + "/X.png");
	    break;
	case '2':
	    $("#game_board #square_" + i + " img").attr("src", path + "/O.png");
	    break;
	}
    }

    $("div#winning_line_0").hide();
    $("div#winning_line_1").hide();
    for (var i in winners) {
	// The upper left-most square to grab measurements from
	square = $("#game_board #square_" + winners[i][0])
	pos_1 = square.offset()
	pos_2 = $("#game_board #square_" + winners[i][1]).offset()
	pos_3 = $("#game_board #square_" + winners[i][2]).offset()
	
	var angle = 0;
	var length = square.height() * 3 + 12;
	var left = pos_1.left;
	var top = pos_1.top;

	// Set the angle and length
	if (pos_1.left == pos_2.left) {
	    // vertical
	    angle = 90;
	    left = pos_1.left + square.width() / 2;

	} else if (pos_1.top == pos_2.top) {
	    // horizontal
	    angle = 0;
	    top = pos_1.top + square.height() / 2;

	} else {
	    length = length * Math.sqrt(2);
	    if (pos_1.left < pos_2.left) {
		angle = 45;
	    } else {
		left = pos_1.left + square.width() + 3;
		angle = 135;
	    }
	}

	// set the position and display
	line = $("div#winning_line_" + i)
	line.css({
	    'position': 'absolute',
	    'left': 0,
	    'top': 0,
	    '-ms-transform-origin': '0% 0%',
	    '-ms-transform': 'rotate(' + angle + 'deg)',
	    '-moz-transform-origin': '0% 0%',
	    '-moz-transform': 'rotate(' + angle + 'deg)',
	    '-webkit-transform-origin': '0% 0%',
	    '-webkit-transform': 'rotate(' + angle + 'deg)',
	    '-o-transform-origin': '0% 0%',
	    '-o-transform': 'rotate(' + angle + 'deg)'
	});
	line.offset({top: top, left: left});
	line.width(length);
	line.show();
    }

    if (current_players[turn] == "computer") {
	get_next_move();
    }
}


// Resets the board to all blanks
function new_board() {
    current_board = "000000000";
    turn = "player_x"
    draw_board(current_board, []);
}