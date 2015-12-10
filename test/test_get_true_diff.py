"""
    Test of get_diff function
"""

from pydeepdiff.diff import get_diff


def test_empty_diff():
    a = {
        'blocs_reponses': [{
            'activites_affichage_immediat': [{
                'machine_learning_source': 'rr',
                'ordre': 1,
                'rubriques': [{
                    'code_an9': '54053000',
                    'libelle_rubrique': 'restaurants',
                    'code_an8': '693780'
                }, {
                    'code_an9': '00000706',
                    'libelle_rubrique': 'restaurants asiatiques',
                    'code_an8': '000706'
                }],
                'type_bloc_activite': 'IMMEDIAT',
                'identifications_bloc_reponse_activite': [{
                    'origine_bloc_reponse': 'MANUEL',
                    'identifiant_bloc_reponse': '130749'
                }],
                'libelle': 'RESTAURANTS THAÏLANDAIS',
                'correction': False,
                'identifiant': 'ac1_2',
                'machine_learning_etat': 'valide',
                'forme_canonique': 'restaurant thaïlandais',
                'expressions': [{
                    'rubriques': [{
                        'code_an9': '54053000',
                        'libelle_rubrique': '',
                        'code_an8': '693780'
                    }, {
                        'code_an9': '00000706',
                        'libelle_rubrique': '',
                        'code_an8': '000706'
                    }],
                    'rubriques_fines': [{
                        'code_an9': '00000796',
                        'libelle_rubrique': '',
                        'code_an8': '000796'
                    }],
                    'formes_brutes': ['restaurant', 'thaïlandais'],
                    'type_crc': 'C',
                    'chaine_saisie': 'restaurant thaïlandais',
                    'type_expression': 'RESTRICTION_FAIBLE',
                    'libelle': 'thaïlandaise',
                    'code': 'ObjetCrc_restaurant thaïlandais_5825-693780-50693780-000706-789300-789350-680700_Principale',
                    'formes_normales': ['RESTAURANT :: THAILANDAIS']
                }],
                'suggestion_editoriale': False,
                'scoring_qui_quoi': 'FORT'
            }],
            'type_interpretation': 'QUOI',
            'identifiant_de_bloc': 'ac1'
        }],
        'id': 'restaurant thaïlandais',
        'ambiguite': True,
        'creation_date': '2015-12-10T15:04:08.046092+00:00',
        'user': 'fabio',
        'status': 'OK',
        'mots_signifiants': ['restaurant', 'thaïlandais']
    }
    
    b = {
        'auto_state': {
            'user': None,
            'comments': [],
            'status': None
        },
        'id': 'restaurant thaïlandais',
        'ambiguite': True,
        'creation_date': '2015-12-10T15:04:28.028229+00:00',
        'blocs_reponses': [{
            'activites_affichage_immediat': [{
                'machine_learning_source': 'rr',
                'ordre': 1,
                'rubriques': [{
                    'code_an9': '54053000',
                    'libelle_rubrique': 'restaurants',
                    'code_an8': '693780'
                }, {
                    'code_an9': '00000706',
                    'libelle_rubrique': 'restaurants asiatiques',
                    'code_an8': '000706'
                }],
                'type_bloc_activite': 'IMMEDIAT',
                'identifications_bloc_reponse_activite': [{
                    'origine_bloc_reponse': 'MANUEL',
                    'identifiant_bloc_reponse': '130749'
                }],
                'libelle': 'RESTAURANTS THAÏLANDAIS',
                'correction': False,
                'identifiant': 'ac1_2',
                'machine_learning_etat': 'valide',
                'forme_canonique': 'restaurant thaïlandais',
                'expressions': [{
                    'formes_normales': ['RESTAURANT :: THAILANDAIS'],
                    'rubriques': [{
                        'code_an9': '54053000',
                        'libelle_rubrique': '',
                        'code_an8': '693780'
                    }, {
                        'code_an9': '00000706',
                        'libelle_rubrique': '',
                        'code_an8': '000706'
                    }],
                    'rubriques_fines': [{
                        'code_an9': '00000796',
                        'libelle_rubrique': '',
                        'code_an8': '000796'
                    }],
                    'formes_brutes': ['restaurant', 'thaïlandais'],
                    'type_crc': 'C',
                    'type_expression': 'RESTRICTION_FAIBLE',
                    'libelle': 'thaïlandaise',
                    'code': 'ObjetCrc_restaurant thaïlandais_5825-693780-50693780-000706-789300-789350-680700_Principale',
                    'chaine_saisie': 'restaurant thaïlandais'
                }],
                'suggestion_editoriale': False,
                'scoring_qui_quoi': 'FORT'
            }],
            'type_interpretation': 'QUOI',
            'identifiant_de_bloc': 'ac1'
        }],
        'mots_signifiants': ['restaurant', 'thaïlandais']
    }
    mapping = [{'path': '', 'id': 'id'}, {'path': 'blocs_reponses', 'id': 'identifiant_de_bloc'}, {'path': 'blocs_reponses.activites_affichage_immediat', 'id': 'identifiant'}]
    ignored_field = ['creation_date', 'auto_state', 'user', 'status', 'comments']
    diff = get_diff(a, b, [], mapping, ignored_field)

    assert diff == []
