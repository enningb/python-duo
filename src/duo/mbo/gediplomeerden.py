import pandas as pd

from duo.algemeen import generieke_kolomnamen

gediplomeerden_mbo_url = ("https://duo.nl/open_onderwijsdata/images/10.-gediplomeerden-"
                          "per-instelling%2C-plaats%2C-kenniscentrum%2C-sector%2C-sectorunit%2C-type-mbo"
                          "%2C-opleiding%2C-niveau%2C-geslacht.csv")


def _gediplomeerden_mbo_bestand(gediplomeerden_mbo_url=gediplomeerden_mbo_url):
    """Lees bestand in met mbo-gediplomeerden van DUO-site"""
    data = pd.read_csv(gediplomeerden_mbo_url, sep=';', encoding='latin1')
    return data


def gediplomeerden_mbo():
    """Maak de eerste data tabel in tidy format.
    De TOTAAL-kolommen worden verwijderd.
    De tabel wordt in tidy format gezet.
    Kolommen voor Geslacht, Afstudeercohort en Gediplomeerden worden toevoegd.

    Afstudeercohort wil zeggen dat studenten in het betreffende jaar het diploma hebben behaald.
    """
    gediplomeerden_ruw = _gediplomeerden_mbo_bestand()

    # Maak een lijst met kolommen, zonder TOTAAL:
    target_cols = [col for col in gediplomeerden_ruw.keys().tolist() if 'TOTAAL' not in col]
    # Maak een lijst met id_vars:
    id_vars = [col for col in target_cols if not col.startswith('DIP')]

    tidy = pd.melt(gediplomeerden_ruw[target_cols], id_vars=id_vars, var_name='Variabele', value_name='Gediplomeerden')

    # Maak een kolom Afstudeercohort:
    tidy['Afstudeercohort'] = tidy.Variabele.str[-4:]
    tidy['Afstudeercohort'] = pd.to_numeric(tidy['Afstudeercohort'], errors='coerce')
    # Maak een kolom geslacht:
    tidy['Geslacht'] = tidy.Variabele.str[-7:-4]
    tidy['Geslacht'] = tidy['Geslacht'].replace({'MAN': 'Man', 'VRW': 'Vrouw'})
    assert tidy['Geslacht'].nunique() == 2
    # Verwijder Variabele
    del tidy['Variabele']
    # Verwijder rijen waarbij Gediplomeerden leeg is of 0:
    tidy.dropna(subset=['Gediplomeerden'], inplace=True)
    result = tidy[tidy.Gediplomeerden != 0].copy()

    # Geef kolommen  generieke namen:
    result = result.rename(columns=generieke_kolomnamen)
    return result
