#
#
#
#
#
from IPython.display import HTML, display_html

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