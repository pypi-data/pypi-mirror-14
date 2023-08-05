// this is the javascript for the data entry page
// template at templates/head/entry.html

cursor_accession_number = max_accession_number;



var NP_EN_STRUCT = {
  "!": 1,
  '@': 2,
  '#': 3,
  '$': 4,
  '%': 5,
  '^': 6,
  '&': 7,
  '*': 8,
  '(': 9,
  ')': 0
};

$("#dataEntrySuccessful").hide();
$("#dataEntryUnSuccessful").hide();

function saveBook(){
  /*
   * This function saves the book
   * To do so, it makes 2 ajax calls to the sever.
   * The first call validates the book
   * if the book should be accessioned,it is accessioned by the second call
   * */
  acc_no = $(".input-acc_no").val();
  var book_exists = true;
  $.get("/head/book/validate",{accNo: parseInt(acc_no)}).success(function(data){
    if (data.exists == 0)
      book_exists = false;
    console.log("book exists: " + book_exists.toString());
    if (book_exists === true || book_exists == false){
      console.log(data);
      var post_data = Object.create(null);
      for(i=0;i < cols_entry.length;i++){
        loc = cols_entry[i][1][1];
        post_data[loc] = $(".input-"+loc).val();
      }
      post_data.is_edit = is_edit;
      post_data.csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
      console.log(post_data);

      $.post('/head/book/add', post_data, function(data){
        if (data.success === true){
          max_accession_number = data.acc_no;
          $(".current_acc_no").text(max_accession_number);
          $(".input-acc_no").text(max_accession_number);
          $("html, body").animate({ scrollTop: 0 }, "fast"); // scroll to the top of the screen
          $("#dataEntrySuccessful").show("slow").delay(2000).hide("slow");
          $("#1").focus(); // focus on the first field
          if (clear_fields == 1)
            clearInputFields();
        }
        else {
          var bg_color = $("body").css("background-color");
          $("#dataEntryUnSuccessful").show("slow").delay(2000).hide("slow");
        }
      });
    }
    else if (book_exists = null){
      console.log("accession number is invalid");
    }
  });
}


$("#saveBook").click(function(){ //when i click the save button, save the book
  saveBook();
});

$(window).on('keypress', function(e){ // when i press ctrl+enter save teh book
  // keycode 10 is for enter with ctrl key on chrome and 13 is for enter on
  // firefox
  if (e.ctrlKey == true && (e.keyCode == 10 || e.keyCode == 13)){
    e.preventDefault();
    saveBook();
  }
});


//
//generate a metrix of rows and columns for all the fields
//
var field_matrix = new Array();
for (row = 0;row < no_of_rows;row +=1){
  column = new Array();
  for (col = row; col <= total_cols_entry;col+=no_of_rows){
    column.push(col);
  }
  field_matrix[row] = column
}

function get_last_column(column_id){
  // returns the last column number of the row
  var column_id = parseInt(column_id, 10);
  for (i=0;i < field_matrix.length;i++){
    index = field_matrix[i].indexOf(column_id);
    if (index != -1)
      return field_matrix[i][field_matrix[i].length -1];
    else
      return -1
  }
}

$(".input").on("keypress", function(e){
  // keycode 13 - enter
  // when i press enter, take me to the field below me, thats two fields ahead
  // when i press shift+enter, take me to the field above me, thats two fields
  // back.
  if (e.shiftKey && e.keyCode == 13){
    e.preventDefault();
    var current_element_id = (parseInt(e.currentTarget.id, 10));
    var element_id = current_element_id - 2;
    var element = document.getElementById(element_id.toString());
    if (element == null){
      var last_element_id = get_last_column(current_element_id);
      console.log(last_element_id);
      document.getElementById(last_element_id.toString()).focus();
    }
    else{
      element.focus();
    }
  }
  else if (e.keyCode == 13){
    e.preventDefault();
    var element_id = (parseInt(e.currentTarget.id, 10)+2);
    var element = document.getElementById(element_id.toString());
    if (element == null){
      if (element_id % 2 == 0)
        document.getElementById("2").focus();
      else
        document.getElementById("1").focus();
    }
    else{
      element.focus();
    }
  }
});


$("#"+total_cols_entry.toString()).on('keypress', function(e){
  // keycode 9 - TAB
  // when i press TAB - take me to the next field
  // when i press shift+TAB - take me to the previous field
  // when i am on the last field and i press tab, take me to the first field
  if (e.shiftKey && e.keyCode == 9){
    e.preventDefault();
    $("#"+(total_cols_entry-1).toString()).focus();
  }
  else if (e.keyCode == 9){
    e.preventDefault();
    document.getElementById("1").focus();
  }
});

$("#1").on('keypress', function(e){
  // if i am on the first field, and i press shift+TAB, take me to the last
  // field
  if (e.shiftKey && e.keyCode == 9)
  {
    e.preventDefault();
    $("#"+total_cols_entry.toString()).focus();
  }
});
