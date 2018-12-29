import os
import pandas as pd
import numpy as np


examenkandidaten_url = 'https://duo.nl/open_onderwijsdata/images/06-examenkandidaten-en-geslaagden-2013-2018.csv'

def get_examenkandidaten(examenkandidaten_url):
    data = pd.read_csv(examenkandidaten_url
                        , sep=";"
                        , encoding="latin1")
    return data



def select_columns_examenkandidaten():
    """Selecteer alleen die kolommen die we nodig hebben. Hier worden slaagpercentages
    verwijderd, dat is een tenslotte het resultaat van delen van geslaagden door examenkandidaten en worden 
    de TOTAAL-kolommen verwijderd. Dat is tenslotte het resultaat van een sommering van de gegevens.
    Ook de ONBEKENDEN worden verwijderd, die zijn er niet of nauwelijks en leiden alleen maar af."""

    # lees data in:
    data = get_examenkandidaten()
    target_cols = [col for col in df.keys().tolist() if ((('GESLAAGDEN' in col) or ('EXAMENKAND' in col) or ('-') not in col) and ('TOTAAL' not in col) and ('ONBEKEND' not in col))]
    result = data[target_cols].copy()
    return result

def _examenkandidaten_en_geslaagden_op_een_regel(data):
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
    result = pd.merge(ex_kandidaten
            , geslaagden
            , left_on=fields
            , right_on=fields
            , how='outer')
    
    return result


def tidy_format_examenkandidaten():
    """Zet de tabel om naar tidy-format zonder informatieverlies. Er komen aparte kolommen voor 
    Geslaagden en Examenkandidaten.
    """
    data = select_columns_examenkandidaten()
    result = pd.melt(data
           , id_vars =['BRIN NUMMER', 'VESTIGINGSNUMMER', 'INSTELLINGSNAAM VESTIGING',
                       'GEMEENTENAAM', 'ONDERWIJSTYPE VO', 'INSPECTIECODE', 'OPLEIDINGSNAAM']
           ,value_name='Aantal')
        
    result['Geslacht'] = np.where(result.variable.str.contains('MAN'), 'Man' , np.nan)
    result['Geslacht'] = np.where(result.variable.str.contains('VROUW'), 'Vrouw' , result['Geslacht'])
    assert result.Geslacht.isnull().sum() == 0
    
    result['Examenkandidaten'] = np.where(result.variable.str.contains('EXAMENKANDIDATEN '), result.Aantal , np.nan)
    result['Examenkandidaten'] = pd.to_numeric(result.Examenkandidaten)
    result['Geslaagden'] = np.where(result.variable.str.contains('GESLAAGDEN '), result.Aantal , np.nan)
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

    tidy = _examenkandidaten_en_geslaagden_op_een_regel(result)
    
    tidy = tidy[tidy.Examenkandidaten > 0].copy()
    
    return tidy


def aggregeer(data, groupers = ['BRIN NUMMER', 'INSTELLINGSNAAM VESTIGING','GEMEENTENAAM','ONDERWIJSTYPE VO']):
    '''Aggregeert en melt zodat een tabel ontstaat die gekoppeld kan worden met 1cho.
    Het cohort is het cohort dat start bij een instelling aan het hoger onderwijs, dus 2013 wil zeggen dat scholieren hun 
    diploma halen in het VO in 2012-2013 maar starten bij HSL in of na 2013-2014.
    Belangrijke velden zijn: BRIN NUMMER, GEMEENTENAAM, ONDERWIJSTYP VO'''
    
    filter_vmbo = data['ONDERWIJSTYPE VO']!='VMBO'
    
    subset = data[filter_vmbo].copy()
    
    totaal_cols = [col for col in subset.keys().tolist() if 'GESLAAGDEN' in col and 'TOTAAL' in col]
    result = subset.groupby(groupers).agg(sum)[totaal_cols]
    result.columns = [col[-13:-9] for col in result.columns.tolist()]
    result = result.reset_index()
    result = pd.melt(result, id_vars=groupers, var_name='Cohort', value_name='Aantal')
    result.rename(columns={'GEMEENTENAAM':'Gemeente','ONDERWIJSTYPE VO':'Vooropleiding', 'BRIN NUMMER': 'Brinnummer','INSTELLINGSNAAM VESTIGING':'NaamInstelling'}, inplace=True)
    result.Cohort = result.Cohort.astype(int)
    result = result[result.Cohort > 2014].copy()
    
    return result

def get_duo_data_mbo():
    url = mbo_url = 'https://duo.nl/open_onderwijsdata/images/10.-gediplomeerden-per-instelling%2C-plaats%2C-kenniscentrum%2C-sector%2C-sectorunit%2C-type-mbo%2C-opleiding%2C-niveau%2C-geslacht.csv'
    data = pd.read_csv(mbo_url, sep=';', encoding='latin1')
    return data

def get_mbo_data():
    mbo_ruw = get_duo_data_mbo()
    
    filter_niveau_4 = mbo_ruw.KWALIFICATIENIVEAU== 4
    filter_bol = mbo_ruw['TYPE MBO'].isin(['BOLVT','BOLDT'])
    mbo4 = mbo_ruw[(filter_niveau_4) & (filter_bol)].copy()
    id_vars = ['BRIN NUMMER',
                 'INSTELLINGSNAAM',
                 'PLAATSNAAM',]
    result = pd.melt(mbo4, id_vars=id_vars, var_name='Variabele', value_name='Aantal')
    result = result[result.Variabele.str.contains('TOTAAL')].copy()
    result['Cohort'] = result.Variabele.str[-4:]
    del result['Variabele']
    result.rename(columns={'PLAATSNAAM':'Plaatsnaam','INSTELLINGSNAAM':'NaamInstelling', 'BRIN NUMMER': 'Brinnummer'}, inplace=True)
    result = result.groupby(['Brinnummer', 'NaamInstelling', 'Plaatsnaam','Cohort']).Aantal.sum().reset_index()
    return result