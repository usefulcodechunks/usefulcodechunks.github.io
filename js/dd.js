var getParams = function (url) {
	var params = {};
	var parser = document.createElement('a');
	parser.href = url;
	var query = parser.search.substring(1);
	var vars = query.split('&');
	for (var i = 0; i < vars.length; i++) {
		var pair = vars[i].split('=');
		params[pair[0]] = decodeURIComponent(pair[1]);
	}
	return params;
};

function getLinks(startupname){
   list_of_links = [("https://www.linkedin.com/search/results/all/?keywords=").concat(startupname),("https://www.crunchbase.com/textsearch?q=").concat(startupname),("https://www.google.com/search?q=\"").concat(startupname).concat("\"")]
   return list_of_links
}

function openInNewTab(url) {
  var win = window.open(url, '_blank');
  win.focus();
}

function compareTrends(button_self){
  //https://trends.google.com/trends/explore?geo=US&q=term1,term2
  base_url = "https://trends.google.com/trends/explore?geo=US&q="
  self_url = "?companies="
  //grab startups Div
  startup_name_holder = document.getElementById("startups")
  // //count children inside first level
  // console.log(startup_name_holder.children)
  // console.log(startup_name_holder.getElementsByTagName("input#nameOfst"))
  //grab all the input type text
  st_inputs = startup_name_holder.getElementsByTagName("input")
  new_url = base_url
  for (var i = 0; i < st_inputs.length; i++) {
    if(st_inputs[i].getAttribute('type')=='text'){

      new_url = new_url + st_inputs[i].value + ","
      self_url = self_url + st_inputs[i].value + ","
    }
  }
  new_url = new_url.slice(0, -1)  // remove extra comma
  self_url = self_url.slice(0, -1)
  openInNewTab(new_url)
  history.pushState(null, '', self_url);



}

function addrow(startupname, number_id, list_of_links){

  main_table = document.getElementById("main-table");

  var row = main_table.insertRow(-1);
  row.id = startupname;
  var number = row.insertCell(0);
  var name = row.insertCell(1);
  var linkedin = row.insertCell(2);
  var crunchbase = row.insertCell(3);
  var google = row.insertCell(4);

  number.innerHTML = number_id[number_id.length-1]
  name.innerHTML = startupname;
  linkedin.append(createHyperlink(list_of_links[0],"LinkedIn"));
  crunchbase.append(createHyperlink(list_of_links[1],"CrunchBase"));
  google.append(createHyperlink(list_of_links[2],"Google"));
}

function createHyperlink(link,which){
  var temp = document.createElement("a");
  temp.target="_blank";
  temp.innerHTML = which;
  temp.href = link;
  return temp
}


function updateTable(selected){

  startupblock_id = selected.parentElement.parentElement.parentElement.parentElement.id;
  startupblock = document.getElementById(startupblock_id);
  input_elements = startupblock.getElementsByTagName("input");
  checkbox_ele = input_elements[0]
  text_ele = input_elements[1]

  startup_name = text_ele.value
  if(startup_name != ""){
    if (checkbox_ele.checked == true){
      // Not empty and checked
      addrow(startup_name,startupblock_id,getLinks(startup_name));
    }
    else {
      // Not Empty and unchecked
      document.getElementById(startup_name).remove();
    }

  }
  else {
    alert("This text box is empty");
    checkbox_ele.checked = false;}
}




block_counter = 1
const template = document.getElementById("startup-1").cloneNode(true);



function duplicateRadioTextBlock(){
  current = "startup-"+block_counter;
  var sel_block = document.getElementById(current);
  var clone_of_block = template.cloneNode(true);
  block_counter = block_counter + 1;
  clone_of_block.id = "startup-"+(block_counter);
  var parent_block = document.getElementById("startups");
  parent_block.append(clone_of_block);
}

function deleteLastTextBlock(){
  if(block_counter != 1){
    current = "startup-"+block_counter;
    var sel_block = document.getElementById(current);
    sel_block.remove();
    block_counter = block_counter - 1;
  }
}

function first_load(){
  current_arguements = getParams(window.location.href);

  companies_pre_list = current_arguements["companies"].split(",")


  for (var i = 0; i < companies_pre_list.length; i++) {
    startup_name_holder = document.getElementById("startups")
    st_inputs = startup_name_holder.getElementsByTagName("input")
    if(i == 0){
      //addText
      st_inputs[1].value = companies_pre_list[i];
      //checkbox
      st_inputs[0].checked = true;
      //addrow
      addrow(companies_pre_list[i],"startup-"+(i+1),getLinks(companies_pre_list[i]));

    }
    else {
      //addbox
      duplicateRadioTextBlock()
      //addtext
      st_inputs[(i*2)+1].value = companies_pre_list[i];
      //checkbox
      st_inputs[i*2].checked = true;
      //addrow
      addrow(companies_pre_list[i],"startup-"+(i+1),getLinks(companies_pre_list[i]));
    }
  }
}
first_load()
