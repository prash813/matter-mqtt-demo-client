

function StartStopDemo(userdata, btnobject)
{
	
	//alert(userdata + btnobject.getAttribute("innerHTML"));
	var ipaddr = document.getElementById("ipaddr"); 
//	btnobject.setAttribute("innerHTML", "Unpair");
	
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			var responseTxt = JSON.parse(xhttp.responseText);
			let str = responseTxt.PerformdevOpsRes;
			alert(str);
		}
	};
	request="http://"  + ipaddr.innerHTML + ":" + "5002/Performdevops?" +  "demoname=" + userdata;
	// alert(ipaddr.innerHTML);
	//xhttp.open("GET", "http://192.168.1.63:5000/login", true);
	//alert(request);
	xhttp.open("GET", request, true);
	xhttp.send();
	
}


function onloadfunction(var2)
{
	var elem=document.getElementById("divdata");
	userdata = JSON.parse(var2);
	for(var i=0; i< userdata.length; i++) {
		var div1 = document.createElement("DIV");
		var btn = document.createElement("BUTTON");
		btn.style.display="inline-block";
		btn.setAttribute("style", "font-weight: bold; background-color: rgb(157,0,117); height: 30px; width: 100px; display: inline-block; margin-left: 50px;");
		btn.innerHTML=userdata[i]
		//var tmpdataobj = "pair" + userdata[i].idxinlist;
		//btn.setAttribute("innerHTML", tmpdataobj);
		btn.setAttribute("name", "demobtn");
		btn.addEventListener("click", StartStopDemo.bind(null, userdata[i], btn));
		//imgelem.setAttribute("src", "{{ url_for('static', filename='sample_image.png') }}");
		div1.style.padding = "20px";
		div1.appendChild(btn);
		elem.appendChild(div1);
	}	
	elem.style.visibility='visible';	
};
