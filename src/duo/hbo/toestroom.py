import pandas as pd

from duo.mbo.gediplomeerden import gediplomeerden_mbo
from duo.vo.examenkandidaten import examenkandidaten_gediplomeerden_vo


def mbo4_toestroom_per_jaar_brin():
    """MBO gediplomeerden per jaar per brin met kwalificatieniveau 4"""
    data = gediplomeerden_mbo()
    filter_mbo4 = data.Kwalificatieniveau == 4
    data['Instroomcohort'] = data.Diplomajaar + 1
    result = data[(filter_mbo4)].groupby(['Instroomcohort', 'Brin', ]).Gediplomeerden.sum().reset_index()
    result.Instroomcohort = result.Instroomcohort.astype(int)
    result['Vooropleiding'] = 'mbo'
    return result


def havo_vwo_toestroom_per_jaar_brin():
    data = examenkandidaten_gediplomeerden_vo()
    data['Instroomcohort'] = data.Diplomajaar + 1
    data['Vooropleiding'] = data['Onderwijstype'].replace({'HAVO': 'havo', 'VWO': 'vwo'})
    filter_havo_vwo = data.Onderwijstype.isin(['HAVO', 'VWO'])

    result = data[(filter_havo_vwo)].groupby(['Instroomcohort', 'Brin', 'Vooropleiding']).Gediplomeerden.sum().reset_index()
    result.Instroomcohort = result.Instroomcohort.astype(int)

    return result


def toestroom_hbo():
    """Potentiele hbo-toestroom uit mbo, havo en vwo, per jaar en brin."""
    # Lees alle mbo in:
    mbo4_per_jaar_brin = mbo4_toestroom_per_jaar_brin()
    # Lees alle havo en vwo
    havo_vwo_gediplomeerden_per_jaar_brin = havo_vwo_toestroom_per_jaar_brin()
    # voeg ze samen
    result = pd.concat([mbo4_per_jaar_brin, havo_vwo_gediplomeerden_per_jaar_brin], sort=False)

    assert mbo4_per_jaar_brin.Instroomcohort.max() == havo_vwo_gediplomeerden_per_jaar_brin.Instroomcohort.max()
    return result
