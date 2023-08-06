#
#
#
#
#
from IPython.display import HTML, display_html
from collections import defaultdict
from itertools import cycle

OK = 'OK'
KO = 'KO'

BOOSTRAP_LINK = """<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">"""


STYLE_CSS = """<STYLE type="text/css">
.resultat-ok{
    color:green;
}
.resultat-ko{
    color: red;
}
.message-error{
    color: red;
    font-style: italic;
}
.info{
    color:CornflowerBlue;
}
th {
    color:CornflowerBlue;
}
</STYLE>
"""
display_html(HTML(STYLE_CSS))

def strong(message):
    return f"<strong>{message}</strong>"

def info(message, classe='info'):
    display_html(HTML(f"<span class='{classe}'>{message}</span>"))

def resultat(message, statut, erreur=None):
    display_html(HTML(f"""<span class='{"resultat-ok" if statut==OK else "resultat-ko"}'>{message}</span>"""))
    if erreur is not None:
        display_html(HTML(f"""<span class='message-error'>{erreur}</span>"""))

def active_boostrap():
    display_html(HTML(BOOSTRAP_LINK))

def h1(message, classe="info"):
    display_html(HTML(f"<h1 class='{classe}'>{message}</h1>"))

def h2(message, classe="info"):
    display_html(HTML(f"<h2 class='{classe}'>{message}</h2>"))

def h3(message, classe="info"):
    display_html(HTML(f"<h3 class='{classe}'>{message}</h3>"))

def h4(message, classe="info"):
    display_html(HTML(f"<h4 class='{classe}'>{message}</h4>"))

def h5(message, classe="info"):
    display_html(HTML(f"<h5 class='{classe}'>{message}</h5>"))

def h6(message, classe="info"):
    display_html(HTML(f"<h6 class='{classe}'>{message}</h6>"))

def div(message, classe="info"):
    display_html(HTML(f"<div class='{classe}'>{message}</div>"))

def p(message, classe="info"):
    display_html(HTML(f"<p class='{classe}'>{message}</p>"))
    
class HTMLTable:
    """
    Structure pour l'affiche de table en HTML
    """
    class HTMLColumns:
        def __init__(self):
            self.cols = list()
            self.classes = list()

        @property
        def n_cols(self):
            return len(self.cols)

        def add_column(self, column="", classe=""):
            self.cols.append(column)
            self.classes.append(classe)

        def __str__(self):
            return "".join([f"<td class='{c}'>{v}</td>" for c, v in zip(cycle(self.classes), self.cols)])
        
        def __repr__(self):
            return "<HTMLColumns: "+",".join([f"" in zip(self.cols, self.classes)])

    def __init__(self, headers=None, header_classe="", table_classe=""):
        self.classe = table_classe
        self.add_headers(headers, header_classe)
        self.rows = defaultdict(HTMLTable.HTMLColumns)
        self.row_classes = list()

    @property
    def n_rows(self):
        return len(self.rows)

    def add_headers(self, header_list=None, classe=""):
        if header_list is None:
            self.headers = None
        elif isinstance(header_list, str):
            self.headers = HTMLTable.HTMLColumns()
            self.headers.add_column(header_list, classe)
        elif '__iter__' in dir(header_list):
            self.headers = HTMLTable.HTMLColumns()
            for header in header_list:
                self.headers.add_column(header, classe)
    def add_row(self, columns=None, classe="", column_classe=""):
        """
        Ajoute une ligne au tableau
        :param columns: liste des colonnes 
        :param classe: Class HTML de la ligne
        :return: index de la ligne ajouté
        """
        new_row = self.rows[self.n_rows]
        self.row_classes.append(classe)

        if isinstance(columns, str):
            new_row.add_column(columns, column_classe)
        elif '__iter__' in dir(columns):
            _row = ""
            idx_row = self.n_rows
            for column in columns:
                self.rows[idx_row].add_column(column, column_classe)

        return new_row

    def print(self):
        """
        Génère le HTML et l'affiche
        """
        _table = f"<table class='{self.classe}'>" \
                 + "<tr>"+ "".join([f"<th class='{c}'>{v}</th>" for v, c in zip(self.headers.cols, cycle(self.headers.classes))]) + "</tr>"\
                 + "".join(f"<tr class='{r_classe}'>{str(row)}</tr>" for row, r_classe in zip(self.rows.values(), cycle(self.row_classes)))\
                 + "</table>"
        #print(_table)
        display_html(HTML(_table))