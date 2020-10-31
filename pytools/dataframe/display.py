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


class ServerConnexion(Thread):
    CLIENT_MODE = 'Client'
    SERVER_MODE = 'Server'

    Server_connexion = None
    Client_connexions = dict() # Liste des connexions clientes
    ADDRESS = 'localhost'
    PORT = 8099

    @classmethod
    def Start_server(cls):
        """Ouvre la connexion du serveur"""
        cls.Server_connexion = socket(AF_INET, SOCK_STREAM)
        cls.Server_connexion.bind((cls.ADDRESS, cls.PORT))
        cls.Server_connexion.listen(5)
        #cls.Client_connexions["SERVER"] = ServerConnexion(cls.Server_connexion, mode=cls.SERVER_MODE)

    @classmethod
    def Stop_server(cls):
        """Arrete la connexion du serveur"""
        cls.Client_connexions["SERVER"].alive_commutator = False
        cls.Server_connexion.close()
        cls.Server_connexion = None

    def __init__(self, connexion, mode):
        Thread.__init__(self)
        self._mode = mode
        if self.mode == self.SERVER_MODE:
            if 'SERVER' in self.Client_connexions:
                self.Client_connexions['SERVER'].alive_commutator = False
            connexion = ServerConnexion.Server_connexion
            if self.Server_connexion is None:
                self.Start_server()
                self.Client_connexions['SERVER'] = self

        self._connexion = connexion
        self.alive_commutator = False
        self._input_buffer = []
        self.start()

    @property
    def mode(self):
        return self._mode

    @property
    def connexion(self):
        return self._connexion

    def run(self):
        """
        Lancement le daamon en fonction du mode :
        - MODE SERVEUR : Récupère les demandes de connexions et les acceptent
        - MODE CLIENT : Récupère les messages des clients connectés
        """
        self.alive_commutator = True

        if self.mode == self.SERVER_MODE:
            self.server_daemon()
        elif self.mode == self.CLIENT_MODE:
            self.client_daemon()
        else: # Undefine mode
            log.error("<ServerConnexion>.run : Mode de fonctionnement non défini.")


    def server_daemon(self):
        # TODO : Acceptation des connexions
        log.debug("Lancement du daemon de connexions clientes.")
        while self.alive_commutator:
            connexions_demandees, wl, xl = select([ServerConnexion.Server_connexion], [], [], SELECT_TIMEOUT)
            for connexion in connexions_demandees:
                connexion_acceptees, info_connexion = connexion.accept()
                log.info("<ServerConnexion>.server_daemon :  Nouvelle connexion {}".format(connexion_acceptees))
                self.Client_connexions[connexion_acceptees] = ServerConnexion(connexion_acceptees, self.CLIENT_MODE)

        log.debug("Arret du daemon de connexions clientes.")

    def client_daemon(self):
        log.debug("Lancement du daemon de lecture des messages.")
        while self.alive_commutator:
            # Lecture des messages (entrants)
            try:
                r_clients, wl,xl = select([self.connexion], [], [], SELECT_TIMEOUT)
            except Exception as err:
                log.error(err)
            else:
                for client in r_clients:
                    try:
                        message = client.recv(1024)
                        if message != b'':
                            log.debug("Message reçu : '{}'".format(message.decode()))
                            self._input_buffer.append(json.load(message.decode()))
                    except:
                        pass
        # TODO : Traitement des messages => définir un protocole

        log.debug("Arret du daemon de lecture des messages.")


class HTMLConnect(Thread):
    HTML_MODEL_FILE = "model.html"
    CSS_DEFAULT_FILE = "default.css"
    JS_FILE = "html_connect.js"

    Id_Dataframe = 0
    List_Dataframe = dict() # Liste des instances HHTConnect représentant un Dataframe
    Server = ServerConnexion(None, ServerConnexion.SERVER_MODE) # Serveur de gestion des connexions


    @classmethod
    def get_IdDataframe(cls):
        cls.Id_Dataframe += 1
        return cls.Id_Dataframe

    @classmethod
    def get_html_model(cls):
       if os.path.exists(cls.HTML_MODEL_FILE):
           filename = cls.HTML_MODEL_FILE
       elif os.path.exists(os.path.dirname(__file__)+'/'+ cls.HTML_MODEL_FILE):
           filename = os.path.dirname(__file__)+'/'+ cls.HTML_MODEL_FILE
       else:
           log.error("<HTMLConnect>.get_html_model : Fichier HTML modèle introuvable.")
           return

       with open(filename, 'r') as file:
            html_content = file.readlines()
       return "".join(html_content)

    @classmethod
    def get_default_css(cls):
        if os.path.exists(cls.CSS_DEFAULT_FILE):
            filename = cls.CSS_DEFAULT_FILE
        elif os.path.exists(os.path.dirname(__file__) + '/' + cls.CSS_DEFAULT_FILE):
            filename = os.path.dirname(__file__) + '/' + cls.CSS_DEFAULT_FILE
        else:
            log.error("<HTMLConnect>.get_default_css : Fichier CSS introuvable.")
            return

        with open(filename, 'r') as file:
            css_content = file.readlines()
        return "".join(css_content)

    @classmethod
    def get_javascript(cls):
        if os.path.exists(cls.JS_FILE):
            filename = cls.JS_FILE
        elif os.path.exists(os.path.dirname(__file__) + '/' + cls.JS_FILE):
            filename = os.path.dirname(__file__) + '/' + cls.JS_FILE
        else:
            log.error("<HTMLConnect>.get_javascript : Fichier Javascript introuvable.")
            return

        with open(filename, 'r') as file:
            js_content = file.readlines()
        return "".join(js_content)


    def __init__(self, dataframe, title="",
                 browser_executable=r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'):
        Thread.__init__(self)

        self._browser = browser_executable
        self._dataframe = dataframe
        self._title = title

    @property
    def browser(self):
        return self._browser

    @property
    def title(self):
        return self._title

    @property
    def dataframe(self):
        return self._dataframe

    def run(self):
        """
        Lancement le serveur d'écoute pour la mise à jour
        :return:
        """
        # TODO : lancement du serveur
        pass

    def view(self):
        """
        Affiche le DataFrame dans une page Web
        :return:
        """
        # Création de la page
        html = self.get_html_model()\
            .replace("{stylesheet}", self.get_default_css())\
            .replace("{javascript}", self.get_javascript())

        # TODO : Lancement du browser et affichage de la page
        print(html)

