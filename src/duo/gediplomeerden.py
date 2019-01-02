import pandas as pd

gediplomeerden_url = "https://duo.nl/open_onderwijsdata/images/10.-gediplomeerden-\
                     per-instelling%2C-plaats%2C-kenniscentrum%2C-sector%2C-sectorunit%2C-type-mbo%2C-opleiding%2C-niveau%2C-geslacht.csv"


def get_gediplomeerden():
    """Lees bestand in van DUO-site"""
    gediplomeerden_ur = gediplomeerden_url
    data = pd.read_csv(gediplomeerden_ur, sep=';', encoding='latin1')
    return data


def get_mbo_data():
    """Maak de eerste data tabel"""
    mbo_ruw = get_gediplomeerden()

    filter_niveau_4 = mbo_ruw.KWALIFICATIENIVEAU == 4
    filter_bol = mbo_ruw['TYPE MBO'].isin(['BOLVT', 'BOLDT'])
    mbo4 = mbo_ruw[(filter_niveau_4) & (filter_bol)].copy()
    id_vars = ['BRIN NUMMER', 'INSTELLINGSNAAM', 'PLAATSNAAM']
    result = pd.melt(mbo4, id_vars=id_vars, var_name='Variabele', value_name='Aantal')
    result = result[result.Variabele.str.contains('TOTAAL')].copy()
    result['Cohort'] = result.Variabele.str[-4:]
    del result['Variabele']
    result.rename(columns={'PLAATSNAAM': 'Plaatsnaam', 'INSTELLINGSNAAM': 'NaamInstelling', 'BRIN NUMMER': 'Brinnummer'}, inplace=True)
    result = result.groupby(['Brinnummer', 'NaamInstelling', 'Plaatsnaam', 'Cohort']).Aantal.sum().reset_index()
    return result
