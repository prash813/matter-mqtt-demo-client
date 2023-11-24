
alert("hi");
var elem=document.getElementByID("divdata");
var userdata = json.parse('{{devicelist|tojson|safe}}');
let textNode = document.createTextNode("devicedata");
textNode.innerHTML=userdata.name1;
elem.appendChild(textNode)
elem.style.visibility='visible';	
