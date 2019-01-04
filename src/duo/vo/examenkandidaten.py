import numpy as np
import pandas as pd

examenkandidaten_vo_url = 'https://duo.nl/open_onderwijsdata/images/06-examenkandidaten-en-geslaagden-2013-2018.csv'


def _examenkandidaten_vo_ruw(examenkandidaten_vo_url=examenkandidaten_vo_url):
    """Download csv-bestand met gegevens over examenkandidaten vo van DUO"""
    data = pd.read_csv(examenkandidaten_vo_url, sep=";", encoding="latin1")
    return data


def _select_columns_examenkandidaten_vo():
    """Selecteer alleen die kolommen die we nodig hebben. Hier worden slaagpercentages
    verwijderd, dat is een tenslotte het resultaat van delen van geslaagden door examenkandidaten en worden
    de TOTAAL-kolommen verwijderd. Dat is tenslotte het resultaat van een sommering van de gegevens.
    Ook de ONBEKENDEN worden verwijderd, die zijn er niet of nauwelijks en leiden alleen maar af."""

    # lees data in:
    data = _examenkandidaten_vo_ruw()
    target_cols = [col for col in data.keys().tolist() if ((('GESLAAGDEN' in col) or ('EXAMENKAND' in col) or ('-')
                                                            not in col) and ('TOTAAL' not in col) and ('ONBEKEND' not in col))]
    result = data[target_cols].copy()
    return result


def _examenkandidaten_en_geslaagden_vo_op_een_regel(data):
    """Zet Geslaagden en Examenkandidaten op een regel."""
    fields = ['BRIN NUMMER',
              'VESTIGINGSNUMMER',
              'INSTELLINGSNAAM VESTIGING',
              'GEMEENTENAAM',
              'ONDERWIJSTYPE VO',
              'INSPECTIECODE',
              'OPLEIDINGSNAAM',
              'Geslacht',
              'Cohort']

    # maak een set met geslaagden
    geslaagden = data[data.Geslaagden.notnull()].copy()
    del geslaagden['Examenkandidaten']

    # maak een set met examenkandidaten
    ex_kandidaten = data[data.Examenkandidaten.notnull()].copy()
    del ex_kandidaten['Geslaagden']

    # voeg ze samen
    result = pd.merge(ex_kandidaten, geslaagden, left_on=fields, right_on=fields, how='outer')

    return result


def examenkandidaten_vo():
    """Zet de tabel om naar tidy-format zonder informatieverlies. Er komen aparte kolommen voor
    Geslaagden en Examenkandidaten.
    """
    data = _select_columns_examenkandidaten_vo()
    result = pd.melt(data, id_vars=['BRIN NUMMER', 'VESTIGINGSNUMMER', 'INSTELLINGSNAAM VESTIGING',
                                    'GEMEENTENAAM', 'ONDERWIJSTYPE VO', 'INSPECTIECODE', 'OPLEIDINGSNAAM'], value_name='Aantal')

    result['Geslacht'] = np.where(result.variable.str.contains('MAN'), 'Man', np.nan)
    result['Geslacht'] = np.where(result.variable.str.contains('VROUW'), 'Vrouw', result['Geslacht'])
    assert result.Geslacht.isnull().sum() == 0

    result['Examenkandidaten'] = np.where(result.variable.str.contains('EXAMENKANDIDATEN '), result.Aantal, np.nan)
    result['Examenkandidaten'] = pd.to_numeric(result.Examenkandidaten)
    result['Geslaagden'] = np.where(result.variable.str.contains('GESLAAGDEN '), result.Aantal, np.nan)
    result['Geslaagden'] = pd.to_numeric(result.Geslaagden)

    # maak een tussentabel aan waarbij het eerste jaar wordt afgesplitst:
    jaren = result.variable.str.split('-', expand=True)
    jaren['Cohort'] = jaren[0].str[-4:]
    # voeg het eerste jaar toe aan de resultaattabel:
    result['Cohort'] = jaren.Cohort
    assert result.Cohort.isnull().sum() == 0

    # verwijder de kolommen die we niet meer nodig hebben:
    del result['variable']
    del result['Aantal']

    tidy = _examenkandidaten_en_geslaagden_vo_op_een_regel(result)

    tidy = tidy[tidy.Examenkandidaten > 0].copy()

    return tidy
