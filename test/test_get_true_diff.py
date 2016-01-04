"""
    Test of get_diff function
"""

from pydeepdiff.diff import get_diff


def test_empty_diff():
    a = {
            "api_response": {
                "status_code": 200
            },
            "ambiguite": True,
            "creation_date": "2015-12-15T10:31:41.074353+00:00",
            "blocs_reponses": [{
                "type_interpretation": "QUOI",
                "activites_affichage_immediat": [{
                    "forme_canonique": "paysagiste",
                    "machine_learning_source": "rr",
                    "suggestion_editoriale": False,
                    "type_bloc_activite": "IMMEDIAT",
                    "rubriques": [{
                        "code_an8": "850008",
                        "code_an9": "00850008",
                        "libelle_rubrique": "paysagistes d'intérieur"
                    }, {
                        "code_an8": "850009",
                        "code_an9": "00850009",
                        "libelle_rubrique": "paysagistes conseils"
                    }, {
                        "principale": True,
                        "code_an8": "594420",
                        "code_an9": "30055800",
                        "libelle_rubrique": "paysagistes"
                    }, {
                        "code_an8": "447010",
                        "code_an9": "30455800",
                        "libelle_rubrique": "aménagement, entretien de jardins, de parcs"
                    }],
                    "machine_learning_etat": "valide",
                    "expressions": [{
                        "formes_brutes": ["paysagiste"],
                        "chaine_saisie": "paysagiste",
                        "rubriques_fines": [],
                        "type_expression": "ACTIVITE",
                        "formes_normales": ["XXX"],
                        "type_crc": "",
                        "libelle": "paysagiste",
                        "code": "Objet_paysagiste_Principale"
                    }],
                    "correction": False,
                    "identifications_bloc_reponse_activite": [{
                        "origine_bloc_reponse": "MANUEL",
                        "identifiant_bloc_reponse": "106949"
                    }],
                    "ordre": 1,
                    "scoring_qui_quoi": "FORT",
                    "libelle": "PAYSAGISTES, AMENAGEMENT DE PARCS ET JARDINS",
                    "identifiant": "ac1"
                }],
                "identifiant_de_bloc": "ac1"
            }],
            "mots_signifiants": ["paysagiste"],
            "id": "paysagiste",
            "requete": {
                "libelle": "paysagiste",
                "tx_fragile": "0.039009564",
                "frequence": "29637.0"
            }
        }

    b = {
            "auto_state": {
                "user": None,
                "comments": [],
                "status": None
            },
            "api_response": {
                "status_code": 200
            },
            "ambiguite": True,
            "creation_date": "2015-12-15T10:33:12.172772+00:00",
            "blocs_reponses": [{
                "identifiant_de_bloc": "ac1",
                "activites_affichage_immediat": [{
                    "forme_canonique": "paysagiste",
                    "suggestion_editoriale": False,
                    "machine_learning_source": "rr",
                    "rubriques": [{
                        "code_an8": "850008",
                        "code_an9": "00850008",
                        "libelle_rubrique": "paysagistes d'intérieur"
                    }, {
                        "code_an8": "850009",
                        "code_an9": "00850009",
                        "libelle_rubrique": "paysagistes conseils"
                    }, {
                        "principale": True,
                        "code_an8": "594420",
                        "code_an9": "30055800",
                        "libelle_rubrique": "paysagistes"
                    }, {
                        "code_an8": "447010",
                        "code_an9": "30455800",
                        "libelle_rubrique": "aménagement, entretien de jardins, de parcs"
                    }],
                    "identifications_bloc_reponse_activite": [{
                        "origine_bloc_reponse": "MANUEL",
                        "identifiant_bloc_reponse": "106949"
                    }],
                    "expressions": [{
                        "formes_normales": ["XXX"],
                        "formes_brutes": ["paysagiste"],
                        "chaine_saisie": "paysagiste",
                        "rubriques_fines": [],
                        "type_expression": "ACTIVITE",
                        "type_crc": "",
                        "libelle": "paysagiste",
                        "code": "Objet_paysagiste_Principale"
                    }],
                    "correction": False,
                    "machine_learning_etat": "valide",
                    "ordre": 1,
                    "scoring_qui_quoi": "FORT",
                    "libelle": "PAYSAGISTES, AMENAGEMENT DE PARCS ET JARDINS",
                    "type_bloc_activite": "IMMEDIAT",
                    "identifiant": "ac1"
                }],
                "type_interpretation": "QUOI"
            }],
            "mots_signifiants": ["paysagiste"],
            "id": "paysagiste",
            "requete": {
                "libelle": "paysagiste",
                "tx_fragile": "0.039009564",
                "frequence": "29637.0"
            }
        }

    mapping = [{'path': '', 'id': 'id'}, {'path': 'blocs_reponses', 'id': 'identifiant_de_bloc'}, {'path': 'blocs_reponses.activites_affichage_immediat', 'id': 'identifiant'}]
    ignored_field = ['creation_date', 'auto_state', 'user', 'status', 'comments']
    diff = get_diff(a, b, [], mapping, ignored_field)

    assert diff == []
