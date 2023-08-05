


var LANG_SHEET = {
  "acc_no": {
    NP: "btf{=g+=",
    EN: "Accession Number"
  },
  "call_no":{
    NP: "sn =;+",
    EN: "Call Number"
  },
  "title": {
    NP: "lzif{s",
    EN: "Title"
  },
  "auth": {
    NP: "n]vs",
    EN: "Author"
  },
  "pub_name": {
    NP: "k|sfzs",
    EN: "Publisher's Name"
  },
  "pub_year": {
    NP: "ldtL",
    EN: "Year of Publication"
  },
  "pub_place": {
    NP: "k|sfzg :yfg",
    EN: "Place of Publication"
  },
  "kwds": {
    NP: "d'n ljifo",
    EN: "Keywords"
  },
  "edtn": {
    NP: ";+:s/0f",
    EN: "Edition"
  },
  "ser": {
    NP: "cg'qmd",
    EN: "series"
  },
  "vol": {
    NP: "v08",
    EN: "Volume"
  },
  "price": {
    NP: 'd"No',
    EN: "Price"
  },
  "gifted-by": {
    NP: "pkxf/",
    EN: "Gifted By"
  }
}

function changeLang(lang){
  var input_font = $("font");
  var form_control = $(".form-control");

  if (lang=="NP"){
    input_font.attr("face", "preeti");
    form_control.css("font-size","20px");
    // change placeholder values
    for (i=0;i < form_control.length;i++){
      var y = form_control[i];
      var input = $(".input-"+y.attributes["mid"].value);
      input.attr("placeholder",LANG_SHEET[input.attr("mid")].NP);
      var th = $(".th-"+y.attributes['mid'].value);
      th.text(LANG_SHEET[input.attr('mid')].NP);
    }
    language = "NP"
  }
  else if (lang=="EN"){
    input_font.attr("face", "");
    form_control.css("font-size","14px");
    for (i=0;i < form_control.length;i++){
      var y = form_control[i];
      var d = $(".input-"+y.attributes["mid"].value);
      d.attr("placeholder",LANG_SHEET[d.attr("mid")].EN);
      var th = $(".th-"+y.attributes['mid'].value);
      th.text(LANG_SHEET[input.attr('mid')].EN);
    }
    langauge = "EN"
  }
}

function clearInputFields(){
  var inputs = $(".input");
  for (i=0;i < inputs.length;i++){
    inputs[i].value = "";
  }
}
