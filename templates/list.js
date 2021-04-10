/*1.add search function
 *2 add key events handler
 *3.setAuthorPaperNum
 *4.setDatePaperNum
 */

//var searchNum = 0;
var authorPaperNum = {};
function setAuthorPaperNum(authorPaperNum){
	//for
}

/*function addAuthorElements(listID, referenceID, spanID, authorName, paperNum){
	
	var newList = document.createElement("li"); 
	newList.class = "nav-item";
	newList.id = listID;
	//newList.innerHTML = "This is a paragraph.";
	document.getElementById("authorList").appendChild(newList); 
	
	var newReference = document.createElement("a"); 
	newReference.class = "d-flex nav-link";
	newReference.href = "#";
	newReference.innerHTML = authorName;
	newReference.id = referenceID;
	document.getElementById(listID).appendChild(newReference); 
	
	var newSpan = document.createElement("span"); 
	newSpan.class = "ml-auto align-self-center badge badge-secondary badge-pill";
	newSpan.innerHTML = paperNum;
	newSpan.id = spanID;
	document.getElementById(referenceID).appendChild(newSpan); 
	
}*/

function search(searchSelect, searchContent){
	//authorPaperNum
}

function handleClicked(evt) {
    // Determine which page has been clicked on
    // evt.target tells us which item triggered this function
	if (typeof($(evt.target).attr("id")) == "string" && $(evt.target).attr("id").substring(0,4) == "page"){
		let page_number = $(evt.target).attr("id").substring(4);
		page_number = parseInt(page_number);
		$(evt.target).focus;
		$(evt.target).active;
		console.log("clicked " + page_number + "!");
	}
	//clicked search
	else if (typeof($(evt.target).attr("id")) == "string" && $(evt.target).attr("id") == "searchButton"){
		console.log("clicked search!");
		if ($("#searchContent").val() == ""){
			alert("Please type something.");
			return false;
		}
		console.log($("#searchSelect").val());
		console.log($("#searchContent").val());
		addAuthorElements("expList", "expR", "expS", "Yin Yue", 10);
		//change the # of different papers		
		//searchNum++;
		var a1 = 4;
		var a2 = 5;
		var a3 = 6;
		var p1 = 7;
		var p2 = 8;
		var p3 = 9;
		
		document.getElementById("a1").innerHTML = a1;
		document.getElementById("a2").innerHTML = a2;
		document.getElementById("a3").innerHTML = a3;
		
		document.getElementById("p1").innerHTML = p1;
		document.getElementById("p2").innerHTML = p2;
		document.getElementById("p3").innerHTML = p3;
	}
	else if (typeof($(evt.target).attr("id")) == "string" && $(evt.target).attr("id").toString(0,4) == "link"){
		console.log("clicked link!");
	}
	
    // Start the note
    //handleNoteOn(key_number);

    // Select the key
    //$("#key-" + key_number).focus();
}


$(document).ready(function() {

            // Set up the event handlers for all the buttons
			console.log("ready function");
            //$("button").on("mousedown", handlePianoMouseDown);
			//$("page-item").on("mousedown", handlePianoMouseDown);
			//$("button").on("mousedown", handlePianoMouseDown);
            //$(document).on("mouseup", handlePianoMouseUp);

            // Set up key events
            //$(document).keydown(handlePageKeyDown);
            //$(document).keyup(handlePageKeyUp);
			
			//Set up the click events
			$(document).click(handleClicked);
			//var paperList = $("paperlist.items()");
			//console.log(paperList);
});