function CreatedivWithContent()
{



}
function UnpairAll(btnobject)
{
	var ipaddr = document.getElementById("ipaddr"); 
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			var responseTxt = JSON.parse(xhttp.responseText);
			let str="UnapirAll: ";
			str += responseTxt.UnPairAll;
			alert(str);
		}
	};
	var random1=Math.random();
	request="http://"  + ipaddr.innerHTML + ":" + "5001/UnpairAll?version=" + random1;
	//alert(request);
	xhttp.open("GET", request, true);
	xhttp.send();
	

}
function PairOrUnpair(userdata, btnobject)
{
	
	//alert(userdata.idxinlist+btnobject.getAttribute("innerHTML"));
	var ipaddr = document.getElementById("ipaddr"); 
//	btnobject.setAttribute("innerHTML", "Unpair");
	
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			var responseTxt = JSON.parse(xhttp.responseText);
			let str = responseTxt.Pairing;
			alert(str);
			if(responseTxt.Pairing=="Success")
			{
				btnobject.innerHTML="Unpair";

			}
			else 
			{

				btnobject.innerHTML="Pair";

			}

		}
	};
	var request;
	var random1=Math.random();
	if(btnobject.innerHTML == "Pair")
		request="http://"  + ipaddr.innerHTML + ":" + "5001/CommissionMatterDevice?" +  "index=" + userdata.idxinlist + "&version=" + random1;
	else 		
		request="http://"  + ipaddr.innerHTML + ":" + "5001/UnpairMatterDevice?" +  "index=" + userdata.idxinlist + "&version=" + random1;
	// alert(ipaddr.innerHTML);
	//xhttp.open("GET", "http://192.168.1.63:5000/login", true);
	//alert(request);
	xhttp.open("GET", request, true);
	xhttp.send();
	
}
//staticurl is useledd param
function onloadfunction(var2, staticurl)
{
	var elem=document.getElementById("divdata");
	userdata = JSON.parse(var2);
	for(var i=0; i< userdata.length; i++) {
		var div1 = document.createElement("DIV");
		var textNode = document.createTextNode(userdata[i].name);
		var x = document.createElement("SPAN");
		var imgelem = document.createElement("IMG")
		var btn = document.createElement("BUTTON");
                var pairstatus = userdata[i].pairstatus;
		btn.style.display="inline-block";
		btn.setAttribute("style", "font-weight: bold; background-color: rgb(157,0,117); height: 30px; width: 100px; display: inline-block; margin-left: 50px;");
		if(pairstatus  == "paired"){
			btn.innerHTML="Unpair";
			//var tmpdataobj = "pair" + userdata[i].idxinlist;
			//btn.setAttribute("innerHTML", tmpdataobj);
			btn.setAttribute("name", "Unpair");
		}
		else {
			btn.innerHTML="Pair";
			btn.setAttribute("name", "Pair");

		}
		btn.addEventListener("click", PairOrUnpair.bind(null, userdata[i], btn));
		//imgelem.setAttribute("src", "{{ url_for('static', filename='sample_image.png') }}");
		imgelem.setAttribute("src", "/static/sample_image.png");
		div1.style.padding = "20px";
		x.style.display="block";
		x.style.width="100px";
		x.style.textAlign="center";
		x.style.fontWeight = 'bold';
		x.appendChild(textNode);
		/*
		x.style.padding="10px";
		imgelem.style.padding = "20px";
		*/
		div1.appendChild(imgelem);
		div1.appendChild(btn);
		div1.appendChild(x);
		elem.appendChild(div1);
	}	
	elem.style.visibility='visible';
	var elem1=document.getElementById("divdata1");
	var y = document.getElementById("unpairbtn");
	y.addEventListener("click", UnpairAll.bind(null, y));
};
