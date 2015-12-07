"""
    Test of get_diff function
"""

from pydeepdiff.diff import get_diff


def test_empty_diff():
    diff = []

    obj_a = {
        'id': 'cabinetinfirmière',
        'blocs_reponses': [
            {
                'activites_affichage_immediat': [
                    {
                        'suggestion_editoriale': False,
                        'machine_learning_etat': 'valide',
                        'correction': False,
                        'machine_learning_source': 'rr',
                        'scoring_qui_quoi': 'FORT',
                        'identifiant': 'ac1',
                        'libelle': 'INFIRMIERS(CABINETS,SOINSÀDOMICILE)',
                        'expressions': [
                            {
                                'formes_brutes': [
                                    'cabinet',
                                    'infirmière'
                                ],
                                'code': 'Objet_cabinetinfirmier_Principale',
                                'formes_normales': [
                                    'XXX'
                                ],
                                'libelle': 'cabinetinfirmière',
                                'type_crc': '',
                                'rubriques_fines': [

                                ],
                                'chaine_saisie': 'cabinetinfirmière',
                                'type_expression': 'ACTIVITE'
                            }
                        ],
                        'type_bloc_activite': 'IMMEDIAT',
                        'rubriques': [
                            {
                                'libelle_rubrique': 'infirmiers(cabinets,soinsàdomicile)',
                                'code_an8': '432240',
                                'code_an9': '58101800'
                            }
                        ],
                        'ordre': 1,
                        'identifications_bloc_reponse_activite': [
                            {
                                'origine_bloc_reponse': 'MANUEL',
                                'identifiant_bloc_reponse': '4124'
                            }
                        ]
                    }
                ],
                'type_interpretation': 'QUOI',
                'identifiant_de_bloc': 'ac1'
            }
        ],
        'mots_signifiants': [
            'infirmière'
        ],
        'ambiguite': True,
        'mots_faibles': [
            'cabinet'
        ]
    }

    obj_b = {
        'id': 'cabinetinfirmière',
        'blocs_reponses': [
            {
                'activites_affichage_immediat': [
                    {
                        'suggestion_editoriale': False,
                        'machine_learning_etat': 'valide',
                        'correction': False,
                        'machine_learning_source': 'rr',
                        'scoring_qui_quoi': 'FORT',
                        'identifiant': 'ac1',
                        'libelle': 'INFIRMIERS(CABINETS,SOINSÀDOMICILE)',
                        'expressions': [
                            {
                                'formes_brutes': [
                                    'cabinet',
                                    'infirmière'
                                ],
                                'code': 'Objet_cabinetinfirmier_Principale',
                                'formes_normales': [
                                    'XXX'
                                ],
                                'libelle': 'cabinetinfirmière',
                                'type_crc': '',
                                'rubriques_fines': [

                                ],
                                'chaine_saisie': 'cabinetinfirmière',
                                'type_expression': 'ACTIVITE'
                            }
                        ],
                        'type_bloc_activite': 'IMMEDIAT',
                        'rubriques': [
                            {
                                'libelle_rubrique': 'infirmiers(cabinets,soinsàdomicile)',
                                'code_an8': '432240',
                                'code_an9': '58101800'
                            }
                        ],
                        'ordre': 1,
                        'identifications_bloc_reponse_activite': [
                            {
                                'origine_bloc_reponse': 'MANUEL',
                                'identifiant_bloc_reponse': '4124'
                            }
                        ]
                    }
                ],
                'type_interpretation': 'QUOI',
                'identifiant_de_bloc': 'ac1'
            }
        ],
        'mots_signifiants': [
            'infirmière'
        ],
        'ambiguite': True,
        'mots_faibles': [
            'cabinet'
        ]
    }

    mapping = []

    diff.extend(get_diff(obj_a, obj_b, [], mapping, p_complex_details=True))

    expected_diff = []

    assert diff == expected_diff


def test_simplevalue_diff():
    diff = []

    obj_a = {
        'id': 'cabinetinfirmière',
        'blocs_reponses': [
            {
                'activites_affichage_immediat': [
                    {
                        'suggestion_editoriale': False,
                        'machine_learning_etat': 'valide',
                        'correction': False,
                        'machine_learning_source': 'rr',
                        'scoring_qui_quoi': 'FORT',
                        'identifiant': 'ac1',
                        'libelle': 'INFIRMIERS(CABINETS,SOINSÀDOMICILE)',
                        'expressions': [
                            {
                                'formes_brutes': [
                                    'cabinet',
                                    'infirmière'
                                ],
                                'code': 'Objet_cabinetinfirmier_Principale',
                                'formes_normales': [
                                    'XXX'
                                ],
                                'libelle': 'cabinetinfirmière',
                                'type_crc': '',
                                'rubriques_fines': [

                                ],
                                'chaine_saisie': 'cabinetinfirmière',
                                'type_expression': 'ACTIVITE'
                            }
                        ],
                        'type_bloc_activite': 'IMMEDIAT',
                        'rubriques': [
                            {
                                'libelle_rubrique': 'infirmiers(cabinets,soinsàdomicile)',
                                'code_an8': '432240',
                                'code_an9': '58101800'
                            }
                        ],
                        'ordre': 1,
                        'identifications_bloc_reponse_activite': [
                            {
                                'origine_bloc_reponse': 'MANUEL',
                                'identifiant_bloc_reponse': '4124'
                            }
                        ]
                    }
                ],
                'type_interpretation': 'QUOI',
                'identifiant_de_bloc': 'ac1'
            }
        ],
        'mots_signifiants': [
            'infirmière'
        ],
        'ambiguite': True,
        'mots_faibles': [
            'cabinet'
        ]
    }

    obj_b = {
        'id': 'cabinetinfirmière',
        'blocs_reponses': [
            {
                'activites_affichage_immediat': [
                    {
                        'suggestion_editoriale': False,
                        'machine_learning_etat': 'valide',
                        'correction': False,
                        'machine_learning_source': 'rr',
                        'scoring_qui_quoi': 'FORT',
                        'identifiant': 'ac1',
                        'libelle': 'INFIRMIERS(CABINETS,SOINSÀDOMICILE)',
                        'expressions': [
                            {
                                'formes_brutes': [
                                    'cabinet',
                                    'infirmière'
                                ],
                                'code': 'Objet_cabinetinfirmier_Principale',
                                'formes_normales': [
                                    'XXX'
                                ],
                                'libelle': 'cabinetinfirmière',
                                'type_crc': '',
                                'rubriques_fines': [

                                ],
                                'chaine_saisie': 'cabinetinfirmière',
                                'type_expression': 'ACTIVITE'
                            }
                        ],
                        'type_bloc_activite': 'IMMEDIAT',
                        'rubriques': [
                            {
                                'libelle_rubrique': 'infirmiers(cabinets,soinsàdomicile)',
                                'code_an8': '432240',
                                'code_an9': '58101800'
                            }
                        ],
                        'ordre': 2,
                        'identifications_bloc_reponse_activite': [
                            {
                                'origine_bloc_reponse': 'MANUEL',
                                'identifiant_bloc_reponse': '4124'
                            }
                        ]
                    }
                ],
                'type_interpretation': 'QUOI',
                'identifiant_de_bloc': 'ac1'
            }
        ],
        'mots_signifiants': [
            'infirmière'
        ],
        'ambiguite': True,
        'mots_faibles': [
            'cabinet'
        ]
    }

    mapping = [
        {'path': '', 'id': 'id'},
        {'path': 'blocs_reponses', 'id': 'identifiant_de_bloc'},
        {'path': 'blocs_reponses.activites_affichage_immediat', 'id': 'identifiant'}
    ]

    diff.extend(get_diff(obj_a, obj_b, "", mapping, p_complex_details=True))

    expected_diff = [{'kind': 'E', 'lhs': 1, 'path_to_object': 'blocs_reponses.[0].activites_affichage_immediat.[0].ordre',  'filter': 'blocs_reponses.activites_affichage_immediat.ordre', 'rhs': 2}]

    assert diff == expected_diff
