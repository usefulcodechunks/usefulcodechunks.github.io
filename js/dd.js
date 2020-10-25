
function getLinks(startupname){
   // // Selecting the input element and get its value
   // var inputVal = document.getElementById("myInput").value;
   // console.log(inputVal)
   // // Displaying the value
   // //alert(inputVal);
   // document.getElementById('LinkedIn').setAttribute("href",("https://www.linkedin.com/search/results/all/?keywords=").concat(inputVal));
   // document.getElementById('crunchbase').setAttribute("href",("https://www.crunchbase.com/textsearch?q=").concat(inputVal));
   // document.getElementById('google').setAttribute("href",("https://www.google.com/search?q=\"").concat(inputVal).concat("\""));

   list_of_links = [("https://www.linkedin.com/search/results/all/?keywords=").concat(startupname),("https://www.crunchbase.com/textsearch?q=").concat(startupname),("https://www.google.com/search?q=\"").concat(startupname).concat("\"")]
   return list_of_links
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
console.log(template)


function duplicateRadioTextBlock(){


  current = "startup-"+block_counter;
  var sel_block = document.getElementById(current);
  console.log(template)
  var clone_of_block = template.cloneNode(true);
  block_counter = block_counter + 1
  clone_of_block.id = "startup-"+(block_counter);
  var parent_block = document.getElementById("startups");
  parent_block.append(clone_of_block)
}

function deleteLastTextBlock(){
  if(block_counter != 1){
    current = "startup-"+block_counter;
    var sel_block = document.getElementById(current);
    sel_block.remove()
    block_counter = block_counter - 1
  }
}
