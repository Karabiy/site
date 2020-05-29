//alert('hello');

var a;
a = 1;

function change_image(){
	if(a == 0){
	document.getElementById("primat").src = "/static/img/приматик.png";
	a = a + 1;
	}
	else{
		if(a == 1){
		document.getElementById("primat").src = "/static/img/приматик2.png"; 
		a = a + 1;
		}
		else{
		document.getElementById("primat").src = "/static/img/приматик3.png";
		a = 0;
		}
	}
}



/*
document.addEventListener('change',kek());

function kek(){
	document.getElementById('')
}
*/