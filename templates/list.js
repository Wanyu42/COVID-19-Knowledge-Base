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

function goPage(pno,psize){
  var itable = document.getElementById("paperListTable");
  var num = itable.rows.length;//表格所有行数(所有记录数)
  console.log(num);
  var totalPage = 0;//总页数
  var pageSize = psize;//每页显示行数
  //总共分几页
  if(num/pageSize > parseInt(num/pageSize)){
      totalPage=parseInt(num/pageSize)+1;
    }else{
      totalPage=parseInt(num/pageSize);
    }
  var currentPage = pno;//当前页数
  var startRow = (currentPage - 1) * pageSize+1;//开始显示的行 31
    var endRow = currentPage * pageSize;//结束显示的行  40
    endRow = (endRow > num)? num : endRow;  //40
    console.log(endRow);
    //遍历显示数据实现分页
  for(var i=1;i<(num+1);i++){
    var irow = itable.rows[i-1];
    if(i>=startRow && i<=endRow){
      irow.style.display = "block";
    }else{
      irow.style.display = "none";
    }
  }
  var tempStr = "共"+num+"条记录 分"+totalPage+"页 当前第"+currentPage+"页";
  if(currentPage>1){
    tempStr += "<a href=\"#\" onClick=\"goPage("+(1)+","+psize+")\">首页</a>";
    tempStr += "<a href=\"#\" onClick=\"goPage("+(currentPage-1)+","+psize+")\"><上一页</a>"
  }else{
    tempStr += "首页";
    tempStr += "<上一页";
  }
  if(currentPage<totalPage){
    tempStr += "<a href=\"#\" onClick=\"goPage("+(currentPage+1)+","+psize+")\">下一页></a>";
    tempStr += "<a href=\"#\" onClick=\"goPage("+(totalPage)+","+psize+")\">尾页</a>";
  }else{
    tempStr += "下一页>";
    tempStr += "尾页";
  }
  document.getElementById("page1").innerHTML = tempStr;
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
			//$(document).click(handleClicked);
			goPage(3,5);
			//var paperList = $("paperlist.items()");
			//console.log(paperList);
});