
function getInputValue(){
   // Selecting the input element and get its value
   var inputVal = document.getElementById("myInput").value;

   // Displaying the value
   //alert(inputVal);
   document.getElementById('LinkedIn').setAttribute("href",("https://www.linkedin.com/search/results/all/?keywords=").concat(inputVal));
   document.getElementById('crunchbase').setAttribute("href",("https://www.crunchbase.com/textsearch?q=").concat(inputVal));
   document.getElementById('google').setAttribute("href",("https://www.google.com/search?q=").concat(inputVal));

}
