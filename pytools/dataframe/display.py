# -*- coding: utf-8 -*-
"""
Ce module contient des fonctions d'affichage des objets du module Pandas.
"""
import os
import logging as log; log.basicConfig(level=log.DEBUG)
from IPython.core.display import display, HTML
import subprocess
import base64
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
from select import select
import json

import websockets
import asyncio
import nest_asyncio
nest_asyncio.apply()

import pandas as pd

############ Jeu de données de tests #########################
import numpy as np
df = pd.DataFrame(columns=[f"Col_{i}" for i in range(10)])
for i in range(20):
    df = df.append(dict(zip(df.columns, np.random.random_sample(20))), ignore_index=True)

for t, (i, j) in enumerate(zip([int(x) for x in np.random.random_sample(15)*10],
                [int(x) for x in np.random.random_sample(15)*10])):
    df.iloc[i, j] = [-i, -j, None, f'Exemple texte ({i},{j})'][t%4]
########################################################################################################################

URL_HEADER = 'data:text/html;charset=utf-8;base64,'
DEFAULT_CSS = """table {border:none;} 
                  tr, td {border: 1px silver solid; text-align:center;} 
                  td {min-width: 20px;} 
                  th{border:none; font-style: italic; text-align:center}"""
DEFAULT_CSS = ""
DEFAULT_CSS_FILE = os.path.dirname(__file__) + '\\default.css'


SELECT_TIMEOUT = 0.5 #Temps d'attente max pour le select

def show(dataframe):
    """
    Affiche au format HTML une dataframe
    :param dataframe: Objet DataFrame à afficher
    :return: None
    """
    display(HTML(dataframe.to_html()))

def showInBrowser(dataframe, name=None,
                  stylesheet_file=DEFAULT_CSS_FILE,
                  stylesheet=DEFAULT_CSS,
                  browser=r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'):
    """
    Affiche une dataframe dans un novigateur web
    :param dataframe: DataFrame à afficher
    :param name: Nom de la DataFrame
    :param stylesheet: Style CSS à appliquer
    :param stylesheet_file: Fichier CSS
    :param browser: Chemin et nom du navigateur à utiliser
    :return:
    """
    html = """<!DOCTYPE html><html><head>
    <title>{title}</title><link rel="stylesheet" type="text/css" href="{stylesheet_file}">
    <style>{stylesheet}</style>
    </head>
    <body><h1>{title}</h1><hr />
    {table}
    </body></html>
    """.format(title=name, stylesheet=stylesheet, stylesheet_file=stylesheet_file, table=dataframe.to_html(border=0))

    subprocess.call([browser, URL_HEADER + str(base64.b64encode(bytes(html, 'utf-8')))[2:-1]])

class MESSAGE_TYPE:
    CONNECTION = "CONNECTION"
    DISCONNECTION = "DISCONNECTION"
    ACKNOWLEDGE = "ACKNOWLEDGE"
    DATA_REFRESH = "DATA_REFRESH"

class Message:
    """
    Represente les messages qui transite entre le serveur et le client
    Structure du message :
    {
        "id_client": <identifiant du client>,
        "message_type": <"CONNECTION", "DISCONNECTION", "DATA_REFRESH", "ACKNOWLEDGE">,
        "title": <title>,
        "size": <lines count>,
        "data": <dataframe in HTML format>,
    }
    """
    ID_CLIENT = "id_client"
    TYPE = "message_type"
    DATA_TITLE = "title"
    DATA_SIZE = "size"
    DATA_BUFFER = "data"

    def __init__(self, json_string):
        self._message = json.loads(json_string)
        if not isinstance(self._message, dict):
            raise TypeError(f"{__class__}.__init__ : Bad type for result of json parsing.")

    def __repr__(self):
        return f"<Message : {str(self)}>"

    def __str__(self):
        return json.dumps(self._message)

    def __getitem__(self, key):
        return self._message.get(key, None)

    def __setitem__(self, key, value):
        self._message[key] = value

    @property
    def id_client(self):
        return self._message.get(self.ID_CLIENT, -1)

    @property
    def message_type(self):
        return self._message.get(self.TYPE, None)
    @message_type.setter
    def message_type(self, message_type):
        self._message[self.TYPE] = message_type


class WebDataframeViewer:
    """

    """
    # GLOBAL VARIABLES
    # ... Serveur
    Event_loop = None
    Server_connexion = None
    Alive_server = False
    Client_connexions = dict() # Liste des connexions clientes
    ADDRESS = 'localhost'
    PORT = 8099

    # ... Page Web
    HTML_MODEL_FILE = "model.html"
    CSS_DEFAULT_FILE = "default.css"
    JS_FILE = "html_connect.js"

    # ... Gestion des instances
    Id_Client = 0
    Instances = dict() # Liste des instances WebDataframeViewer représentant un Dataframe

    # ------------------------------------------------------------------------------------------------------------------
    # METHODES DU SERVEUR
    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def Start_server(cls):
        """Ouvre la connexion du serveur"""
        cls.Event_loop = asyncio.get_event_loop()
        if cls.Event_loop is None :
            cls.Event_loop = asyncio.new_event_loop()

        cls.Alive_server = True
        log.debug(f"{__class__}.server_daemon : Démarrage du serveur ")
        cls.Server_connexion = websockets.serve(cls.server_daemon, cls.ADDRESS, cls.PORT)
        cls.Event_loop.run_until_complete(cls.Server_connexion)

    @classmethod
    def Stop_server(cls):
        """Arrete la connexion du serveur"""
        cls.Alive_server = False
        cls.Server_connexion.ws_server.close()
        cls.Client_connexions = dict()
        cls.Instances = dict()

    @classmethod
    def Disconnect_client(cls, client):
        log.debug(f"{__class__}.Disconnect_client : Déconnexion du client '{client}' ")
        try:
            client.close()
        except:
            pass
        del cls.Client_connexions[client]
        if len(cls.Client_connexions) == 0:
            cls.Stop_server()

    @classmethod
    async def server_daemon(cls, client, path):

        while cls.Alive_server:
            try:
                async for message_buffer in client:
                    message = Message(message_buffer)
                    log.debug(f"{__class__}.server_daemon : Message reçu : " + repr(message))
                    try:
                        if message.message_type == MESSAGE_TYPE.CONNECTION:
                            log.debug(f"{__class__}.server_daemon : Nouvelle connexion {client} - Client " + str(message.id_client))
                            cls.Client_connexions[client] = message.id_client
                            message.message_type = MESSAGE_TYPE.ACKNOWLEDGE
                            await client.send(str(message))

                        elif message.message_type == MESSAGE_TYPE.DISCONNECTION:
                            cls.Disconnect_client(client)

                        elif message.message_type == MESSAGE_TYPE.DATA_REFRESH:
                            id_client = cls.Client_connexions[client]
                            if id_client != message.id_client:
                                log.warning(f"{__class__}.server_daemon : id_client incohérent entre la connexion et le message.")
                            id_client = message.id_client
                            instance = cls.Instances.get(id_client, None)
                            if instance is not None:
                                message[Message.DATA_BUFFER] = instance.dataframe_to_html()
                                message[Message.DATA_TITLE] = instance.title
                                message[Message.DATA_SIZE] = instance.size
                                await client.send(str(message))
                            else: # L'instance n'existe pas => On déconnecte
                                try:
                                    cls.Disconnect_client(client)
                                except Exception as err:
                                    log.error(f"{__class__}.server_daemon :  : Erreur lors de la déconnexion du client : {client}\n->{err}")
                        else:
                            await client.send(message)
                            raise Exception(f"{__class__}.server_daemon : Type de message inconnu. (type de message {type(message)})")
                    except Exception as err:
                        log.error(f"{__class__}.server_daemon :  : Format de message incorrect : {type(message)}{message}")
            except websockets.exceptions.ConnectionClosedError as err:
                log.debug(f"{__class__}.server_daemon :  : Disconnection from {client}\n-> {err}")
                cls.Disconnect_client(client)

        #cls.Server_connexion.close()
        cls.Server_connexion = None
        log.debug(f"{__class__}.server_daemon : Arret du daemon de connexions clientes.")

    # ------------------------------------------------------------------------------------------------------------------
    # MESTHODES DES PAGES WEB
    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def get_html_model(cls):
       if os.path.exists(cls.HTML_MODEL_FILE):
           filename = cls.HTML_MODEL_FILE
       elif os.path.exists(os.path.dirname(__file__)+'/'+ cls.HTML_MODEL_FILE):
           filename = os.path.dirname(__file__)+'/'+ cls.HTML_MODEL_FILE
       else:
           log.error(f"{__class__}.get_html_model : Fichier HTML modèle introuvable.")
           return

       with open(filename, 'r', encoding='utf-8') as file:
            html_content = file.readlines()
       return "".join(html_content)

    @classmethod
    def get_default_css(cls):
        if os.path.exists(cls.CSS_DEFAULT_FILE):
            filename = cls.CSS_DEFAULT_FILE
        elif os.path.exists(os.path.dirname(__file__) + '/' + cls.CSS_DEFAULT_FILE):
            filename = os.path.dirname(__file__) + '/' + cls.CSS_DEFAULT_FILE
        else:
            log.error(f"{__class__}.get_default_css : Fichier CSS introuvable.")
            return

        with open(filename, 'r', encoding='utf-8') as file:
            css_content = file.readlines()
        return "".join(css_content)

    @classmethod
    def get_javascript(cls):
        if os.path.exists(cls.JS_FILE):
            filename = cls.JS_FILE
        elif os.path.exists(os.path.dirname(__file__) + '/' + cls.JS_FILE):
            filename = os.path.dirname(__file__) + '/' + cls.JS_FILE
        else:
            log.error(f"{__class__}.get_javascript : Fichier Javascript introuvable.")
            return

        with open(filename, 'r', encoding='utf-8') as file:
            js_content = file.readlines()
        return "".join(js_content)

    # ------------------------------------------------------------------------------------------------------------------
    # MESTHODES DE LA GESTION DES INSATNCES
    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def get_IdClient(cls):
        cls.Id_Client += 1
        return cls.Id_Client

    # ------------------------------------------------------------------------------------------------------------------
    # METHODES DES OBJETS
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, dataframe, title="",
                browser_executable=r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'):
        self._dataframe = dataframe
        self._browser = browser_executable
        self._title = title
        self._id_client = self.get_IdClient()
        self.Instances[self.id_client] = self

        # Contrôle l'état du serveur. Si STOP alors le lancer
        if not self.Alive_server:
            self.Start_server()

        self.create_html_client()

        log.debug(f"{__class__}.__init__ : Client {self.id_client}")

    @property
    def connexion(self):
        return self._connexion

    @property
    def id_client(self):
        return self._id_client

    @property
    def browser(self):
        return self._browser

    @property
    def title(self):
        return self._title

    @property
    def dataframe(self):
        return self._dataframe

    @property
    def size(self):
        return len(self.dataframe)

    def dataframe_to_html(self):
        return self.dataframe.fillna("<null>").to_dict()

    def create_html_client(self):
        """
        Affiche le DataFrame dans une page Web
        :return:
        """
        # Création de la page
        html = self.get_html_model()\
            .replace("{stylesheet}", self.get_default_css())\
            .replace("{javascript}", self.get_javascript())\
            .replace("{id_client}", str(self.id_client))

        # Lancement du browser et affichage de la page
        log.debug(f"{__class__}.create_html_client : Page HTML\n{html}")
        subprocess.call([self.browser, URL_HEADER + str(base64.b64encode(bytes(html, 'utf-8')))[2:-1]])







