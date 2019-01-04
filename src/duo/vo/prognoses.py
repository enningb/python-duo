from duo.algemeen import generieke_kolomnamen
import pandas as pd
import numpy as np

eerste_prognose_jaar = 2018
prognoses_vo_url = "https://duo.nl/open_onderwijsdata/images/11-leerlingenprognose-vo-2012-2037.csv"

def _prognoses_vo_bestand(prognoses_vo_url=prognoses_vo_url):
    """Lees bestand in met prognoses van DUO-site"""
    data = pd.read_csv(prognoses_vo_url, sep=';', encoding='latin1')
    return data

def prognoses_vo():
    data = _prognoses_vo_bestand()

    # Maak een lijst met kolommen, zonder TOTAAL:
    target_cols = [col for col in data.keys().tolist() if 'totaal' not in col]

    signals = ['BRJ','VMBO','HAVO','VWO','PRO']
    id_vars = target_cols
    for signal in signals:
        id_vars = [col for col in id_vars if not col.startswith(signal)]

    tidy = pd.melt(data[target_cols], id_vars=id_vars, var_name='Variabele', value_name='Aantal')

    extra = tidy.Variabele.str.split('.', expand=True).rename(columns={0:'Onderwijstype',1:'Studiejaar'})
    tidy['Onderwijstype'] = extra.Onderwijstype
    tidy['Studiejaar'] = extra.Studiejaar
    tidy['Studiejaar'] = tidy.Studiejaar.astype(int)
    tidy['Aantal'] = pd.to_numeric(tidy.Aantal, errors='coerce')

    tidy['TypeAantal'] = np.where(tidy.Studiejaar < eerste_prognose_jaar, 'ReëleAantal','Prognose')

    onderwijstype = {'BRJ': 'Brugjaar'
#                    , 'VMBO'
#                    , 'HAVO'
#                    , 'VWO'
                     ,'PRO': 'PRO'}
    tidy['Onderwijstype']  = tidy['Onderwijstype'].replace(onderwijstype)
    result = tidy.rename(columns=generieke_kolomnamen)
    return result
