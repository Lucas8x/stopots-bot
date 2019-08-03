const requestURL = "https://raw.githubusercontent.com/Lucas8x/stopots-bot/master/dicionario.json";
var request = new XMLHttpRequest();
request.open('GET', requestURL);
request.send();
request.responseType = 'json';
request.onload = function () {
	dicionario = request.response;
};

function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}

function xpath(elem){
	return document.evaluate(elem ,document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue;
};

function randomItem(array){
	return array[Math.floor(Math.random()*array.length)];
};

function letter(){
	try {
		return xpath('//*[@id="letter"]/span/text()');
	} catch{};
};

function auto_complete(letter){
	try {
		for(let i = 0; i < dicionario.length; i++){
			if(dicionario[i]['letter'] === letter){
				for(let j = 1; j < 13; j++){
					try {
						let campo = xpath(`//*[@class="ct answers" or @class="ct answers up-enter-done"]//label[${j}]/input`).value;
						if(campo.length === 0){
							let item_category = xpath(`//*[@class="ct answers" or @class="ct answers up-enter-done"]//label[${j}]/span`).textContent.toLowerCase();
							if(item_category === 'nome'){
								item_category = randomItem(["nome feminino", "nome masculino"]);
							}
							else if(item_category === 'comida' && dicionario[i]['categories']['comida'].length === 0){
								item_category = 'comida saudável';
							};
							if(dicionario[i]['categories'][item_category].length > 0){
								let resposta = randomItem(dicionario[i]['categories'][item_category]);
								xpath(`//*[@class="ct answers" or @class="ct answers up-enter-done"]//label[${j}]/input`).value = resposta;
							};
						}
					} catch {
						continue;
					};
				};
				break;
			};
		};
	} catch {};
};

while (true){
	try {
		var button = xpath(`//*[@class="bt-yellow icon-exclamation" 
												or @class="bt-yellow icon-exclamation shake" 
												or @class="bt-yellow icon-exclamation disable"]/strong`).textContent.toUpperCase();
		if(button === 'STOP!'){
			var actual_letter = letter().textContent.toLowerCase();
			auto_complete(actual_letter);
		}
	} catch {};
	await sleep(3000);
};