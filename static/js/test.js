function buttonstatuscall(){
    alert("Hi there");
    document.getElementById("tryit").style.visibility='visible';
    document.getElementById("plussign").style.visibility='visible';
    document.getElementById("matterimg").style.visibility='visible';
    document.getElementById("uimage").style.visibility='visible';

	var tmp1 = document.getElementById("bulb1state");
	var btn1 = document.getElementById("btn1");
	var img1 = document.getElementById("img1");
	var tmp2 = document.getElementById("bulb2state");
	var btn2 = document.getElementById("btn2");
	var img2 = document.getElementById("img2");
	if(tmp1.innerHTML == "commissioned"){
		btn1.style.visibility='hidden';
		img1.style.visibility='visible';
		img1.addEventListener("click", onimg1click);
	}
	if(tmp2.innerHTML == "commissioned"){
		btn2.style.visibility='hidden';
		img2.style.visibility='visible';
		img2.addEventListener("click", onimg1click);
	}
}
