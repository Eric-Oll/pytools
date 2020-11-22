// Javascript for HTML Connect DataFrame
console.log('html.connect.js : Chargement du module');
const title = document.getElementById("title");
const ongletTitle = document.getElementsByTagName('title')[0];
const taille =  document.getElementById("size-value");
const contenu = document.getElementById('contenu');
const error_msg = document.getElementById('error-message');

window.onresize = sizeChange;

var connection ;
var message = {
    id_client: 0,
    message_type: "",
    title: "",
    size: 0,
    data: ""
};


// -------------------------------------------------------------------------------------------
// Fonctions utiles
// -------------------------------------------------------------------------------------------
function log(message){
    console.log(message);
    error_msg.innerHTML =  error_msg.innerHTML + '<br />' + message;
}
function convertTableJsonToHtml(data){
    let htmlTable = "<TABLE id='table-data'>\n<CAPTION id='caption-data'></CAPTION>\n";

    // Entête de colonne
    htmlTable += "<THEAD class='table-head'>\n<TR id='table-entete-ligne-data'><TH id='table-entete-index-data' class='table-entete'></TH>"
    cur_col = 0;
    for(col in data){
      htmlTable += "<TH id='table-entete-col" + cur_col + "-data' class='table-entete'>" + col + "</TH>";
      cur_col++;
    }
    htmlTable += "</TR>\n</THEAD>\n"


    // Données du tableau
    htmlTable += "<TBODY class='table-body'>\n"
    nb_lignes = Object.keys(data[Object.keys(data)[0]]).length;
    console.log("Nombre de ligne du tableau : " + nb_lignes);

    for(let i=0; i<nb_lignes; i++){
      if (i % 2 === 0){
        lig_class = "ligne-pair"
      }
      else{
        lig_class = "ligne-impair"
      }
      htmlTable += "<TR id='table-lig"+i+"-data' class='"+ lig_class +"'>";
      htmlTable += "<TD id='table-index"+i+"-data' class='table-index'>"+Object.keys(data[col])[i]+"</TD>"
      for(let col in data){
          let cur_col = Object.keys(data).indexOf(col);
          let value = Object.values(data[col])[i];
          if (value > 0){
              col_class = "value-positif";
          }
          else if (value<0){
              col_class = "value-negatif";
          }
          else if (value == 0){
              col_class = "value-zero";
          }
          else if (typeof value == "string"){
              col_class = "value-text";
          }
          else{
              col_class = "value-null"
          }

          htmlTable += "<TD id='table-lig"+i+"-col"+cur_col+"-data' class='"+col_class+"'>" + value + "</TD>";
      }
      htmlTable += "</TR>\n"
    }
    htmlTable = htmlTable + "</TBODY></TABLE>";
    return htmlTable;
}


// -------------------------------------------------------------------------------------------
//  MESSAGE_TYPE : Liste les valeur des types de messages
// -------------------------------------------------------------------------------------------
MESSAGE_TYPE = {
    CONNECTION: "CONNECTION",
    DISCONNECTION: "DISCONNECTION",
    ACKNOWLEDGE: "ACKNOWLEDGE",
    DATA_REFRESH: "DATA_REFRESH"
}

// -------------------------------------------------------------------------------------------
// class Message : Modélisation des informations transmis au serveur
// -------------------------------------------------------------------------------------------
class Message {
    constructor(json_buffer){
        try{
            if (json_buffer == ""){
                this._message = {
                    id_client: 0,
                    message_type: "",
                    title: "",
                    size: 0,
                    data: ""
                }
            }
            else{
                this._message = JSON.parse(json_buffer);
            }
        }
        catch(error){
            console.log("Message.<constructor> : " + error);
            error_msg.innerHTML = error_msg.innerHTML + "<br />" + error;
            this._message = {
                id_client: 0,
                message_type: "",
                title: "",
                size: 0,
                data: ""
            }
        }

    }

    get id_client () { return this._message.id_client;}
    set id_client (new_id_client) {
        if(typeof new_id_client == "string") { new_id_client = parseInt(new_id_client);}
        this._message.id_client = new_id_client;
    }

    get message_type () { return this._message.message_type;}
    set message_type (new_message_type) {this._message.message_type = new_message_type;}

    get title () { return this._message.title;}

    get size () { return this._message.size;}

    get data () { return this._message.data;}
    set data (new_data) {this._message.data = new_data;}

    get_message () { return JSON.stringify(this._message); }
}
var message = new Message("");

// -------------------------------------------------------------------------------------------
// Fonctions callback
// -------------------------------------------------------------------------------------------
function messageViewerChange(event){
    if (!btnMessageView.checked && !error_msg.hasAttribute('hidden')) {
        error_msg.setAttribute('hidden','');
        log("Masquage de zone de message. (btnMessageView.checked="+btnMessageView.checked+")");
    }
    else if(btnMessageView.checked && error_msg.hasAttribute('hidden')){
        error_msg.removeAttribute('hidden');
        log("Affichage de zone de message. (btnMessageView.checked="+btnMessageView.checked+")");
    }

}

function sizeChange(event){
    const headerHeight = document.getElementById('header').clientHeight;
    const footerHeight = document.getElementById('footer').clientHeight;
    const tableHeadHeight = document.getElementById('table-head').clientHeight;
    const tableBody = document.getElementById('table-body');

    msg = "Change height size from "+tableBody.clientHeight;
    tableBody.clientHeight = window.innerHeight - headerHeight - footerHeight - tableHeadHeight;
    log(msg + ' to ' + tableBody.clientHeight +
        " (headerHeight = " + headerHeight + ", footerHeight = " + footerHeight
        + ", Table header height = " + tableHeadHeight
        + ", current width="+contenu.clientWidth+"), window size = "
        + window.innerWidth + "x" + window.innerHeight);
}

function receiveData(event) {
    log("Message:" + event.data);
    try{
        message = new Message(event.data);
        contenu.innerHTML = convertTableJsonToHtml(message.data);
        title.innerHTML = message.title;
        ongletTitle.innerHTML = message.title;
        taille.innerHTML = message.size;
    }
    catch(error){
        log(event.data);

    }
}

function sendData(event){
    try{
        message.data = document.getElementById('txtMessage').value;
        document.getElementById('txtMessage').value = "";
    }
    catch(error){
        message.data = ""
    }
    message.message_type = MESSAGE_TYPE.DATA_REFRESH;
    log("Envoie du message : "+ message.get_message());
    connection.send(message.get_message());
}

function openConnection(event) {
    connection = connection('localhost', 8099);
}

function closeConnexion(event) {
    message.message_type = MESSAGE_TYPE.DISCONNECTION
    connection.send(message.get_message());
    connection.close();
}

function connection(address, port){
    let socket = new WebSocket("ws://"+address+":"+port);
    socket.onerror = function(error) {
        console.error(error);
    }
    socket.onopen = function(event) {
        message = new Message('');
        message.id_client = parseInt(document.getElementById('id_client').value);
        message.message_type = MESSAGE_TYPE.CONNECTION;
        this.send(message.get_message());
        log("Connexion établie.");
        sendData();

        // Lorsque la connexion se termine.
        this.onclose = function(event) {
            log("Connexion terminé.");
        };

        // Lorsque le serveur envoi un message.
        this.onmessage = receiveData;
    }
    return socket
}
