// Javascript for HTML Connect DataFrame
document.write('Chargement du module html_connect.js');
//document.addEventListener('loadend', onload);
console.log('html.connect.js : Chargement du module')
const contenu = document.getElementById('contenu')
var connection = connection('localhost', 8099);

function onLoad(){
    console.log("html.connect.js : Execution de la fonction 'onLoad'")
    contenu.innerHTML = contenu.innerHTML + "Chargement de la page<br/>";
}

function receiveData(event) {
    console.log("Message:", event.data);
    // TODO receiveData
}

function sendData(event){
    message = document.getElementById('txtMessage').value;
    console.log("Envoie du message : "+ message);
    // TODO send to server
    connection.send(message);

    document.getElementById('txtMessage').value = "";
}

function closeConnexion(event) {
    connection.close();
}

function connection(address, port){
    let socket = new WebSocket("ws://"+address+":"+port);
    socket.onerror = function(error) {
        console.error(error);
    }
    socket.onopen = function(event) {
        console.log("Connexion établie.");

        // Lorsque la connexion se termine.
        this.onclose = function(event) {
            console.log("Connexion terminé.");
        };

        // Lorsque le serveur envoi un message.
        this.onmessage = receiveData;

        // Envoi d'un message vers le serveur.
        this.send("Hello world!");
    }
    return socket
}


