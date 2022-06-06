"""
Ensemble de fonctions pour le formatage des données à l'affichage
"""

# Formatage pour les pandas.DataFrame
PD_FMT_EURO = lambda x: f"{x:,.2f} €".replace(',', ' ').replace('.', ',')
PD_FMT_INTEGER = lambda x: f"{x:,.0f}".replace(',', ' ').replace('.', ',')
PD_FMT_POURCENT = lambda x: f"{x:.2%}"