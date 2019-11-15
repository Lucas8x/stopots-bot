const requestURL = "https://raw.githubusercontent.com/Lucas8x/stopots-bot/master/dicionario.json";
var dicionario;
var request = new XMLHttpRequest();
request.open('GET', requestURL);
request.send();
request.responseType = 'json';
request.onload = () => {
  dicionario = request.response;
}

// Types = 'quick' , 'deny' , 'check' , null
const validator_type = null;

const randomArrayItem = array => array[Math.floor(Math.random()*array.length)];

//const xpath = elem => document.evaluate(elem ,document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
const xpath = path => {
  var xpath = document.evaluate(path, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
  var temp = [];
  for (var i = xpath.snapshotLength - 1; i >= 0; i--) {
    temp.push(xpath.snapshotItem(i));
  }
  return temp[0];
}

const getActualLetter = () => {
  try {
    return xpath('//*[@id="letter"]/span/text()').textContent.toLowerCase();
  } catch (e) {}
}

const autoComplete = letter => {
  for(let i = 0; i < dicionario.length; i++) {
    if(dicionario[i]['letter'] === letter) {
      for(let j = 1; j < 13; j++) {
        try {
          let input_field = xpath(`//*[@class="ct answers" or @class="ct answers up-enter-done"]//label[${j}]/input`).value;
          if(input_field.length === 0) {
            let item_category = xpath(`//*[@class="ct answers" or @class="ct answers up-enter-done"]//label[${j}]/span`).textContent.toLowerCase();
            if(item_category === 'nome') {
              item_category = randomArrayItem(["nome feminino", "nome masculino"]);
            }
            else if(item_category === 'comida' && dicionario[i]['categories']['comida'].length === 0) {
              item_category = 'comida saudável';
            }
            if(dicionario[i]['categories'][item_category].length > 0) {
              let resposta = randomArrayItem(dicionario[i]['categories'][item_category]);
			  // a
            }
          }
        } catch (e) {
          continue;
        }
      }
      break;
    }
  }
}

const validate = (validator_type, actual_letter) => {
  if(true) {
    if(validator_type === 'quick') {
      xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]').click();
    }
    else if(validator_type === 'deny') {
      for(let i=1; i <= 15;i++) {
        if(xpath(`//*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label[${i}]/span`).textContent.toUpperCase() === 'VALIDADO!') {
          xpath(`//*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label[${i}]/div`).click();
        }
      }
      xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]').click();
    }
    else if(validator_type === 'check') {
      let category = xpath('//*[@class="ct validation up-enter-done"]/div/h3').textContent.toLowerCase();
      for(let i = 0; i < dicionario.length; i++) {
        if(dicionario[i]['letter'] === actual_letter) {
          for(let j=1; i <= 15; j++) {
            try {
              if(xpath(`//*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label[${j}]/span`).textContent.toUpperCase() === 'VALIDADO!') {
                let category_answer = xpath(`//*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label[${j}]/div`);
                if(category_answer !== 'nome') {
                  if(!category_answer in dicionario[i]['categories'][category]) {
                    xpath(`//*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label[${j}]/div`).click();
                  }
                }
                else if(!category_answer in dicionario[i]['nome feminino'] || category_answer in dicionario[i]['nome masculino']) {
                  xpath(`//*[@class="ct validation up-enter-done"]//*[@class="scrollElements"]/label[${j}]/div`).click();
                  }
                }
            } catch (e) {
              continue;
            }
          }
          break;
        }
      }
      xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake"]').click();
    }
  }
}

const gameCheat = () => {
  try {
    var button = xpath('//*[@class="bt-yellow icon-exclamation" or @class="bt-yellow icon-exclamation shake" or @class="bt-yellow icon-exclamation disable"]/strong').textContent.toUpperCase();
    if(button === 'STOP!') {
      autoComplete(getActualLetter());
    }
    else if(button === 'AVALIAR' && validator_type !== null) {
      validate(validator_type, getActualLetter());
    }
  } catch (e) {}
}

setInterval(gameCheat, 5000);