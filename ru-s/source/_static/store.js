varsNormal = { 
"[price]": 1890,
"[normalPrice]": 1890,
"[discount]": 0,
"[endPeriod]": "15.11.2022"
};

varsDiscount = { 
"[price]": 1499,
"[normalPrice]": 1890,
"[discount]": 20,
"[endPeriod]": "15.11.2022"
};

//replace_vars(varsDiscount, "span");
//replace_vars(varsDiscount, "a");

apply_vars("biz.interblitz.budgetpro");

function getParentElement(item){

	parent = item.parentElement;
	
	while(parent.tagName != "P"){
		parent = parent.parentElement;
	}
	
	return parent;

}

function replace_vars(vars, tagName){
	var aTags = document.getElementsByTagName(tagName);
	for (var i = 0; i < aTags.length; i++) {
		for (var key in vars) {
		    if (vars.hasOwnProperty(key)) {
			if (aTags[i].textContent.includes(key)){
				if(vars[key] == 0){
					//aTags[i].style.display = "none"
					//aTags[i].parentElement.parentElement.style.display = "none"
					parent = getParentElement(aTags[i]);
					parent.style.display = "none"
				} else {
					aTags[i].textContent = aTags[i].textContent.replace(key, vars[key])
				}
			}
			
		    }
		}
	}
}

function apply_vars(appId){

	server = "http://192.168.144.112:5000"
	path = "/api/v1/app-order-terms?appId=" + appId + "&locale=ru"

	// (1)
	var XHR = ("onload" in new XMLHttpRequest()) ? XMLHttpRequest : XDomainRequest;

	var xhr = new XHR();

	// (2) запрос на другой домен :)
	xhr.open('GET', server + path, true);

	xhr.onload = function() {
		//alert( this.responseText );
		const vars = JSON.parse(this.responseText);
		replace_vars(vars, "span")
		replace_vars(vars, "a")
	}

	xhr.onerror = function() {
		const vars = { 
		"[price]": 0,
		"[normalPrice]": 0,
		"[discount]": 0,
		"[endPeriod]": "",
		'[errorCode]': 503
		};
		replace_vars(vars, "span")
		replace_vars(vars, "a")
	}

	xhr.send();
}
