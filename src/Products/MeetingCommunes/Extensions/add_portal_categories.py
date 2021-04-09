#! /usr/bin/python
# -*- coding: utf-8 -*-
from plone import api

CATEGORIES = [
    ("administration", "Administration générale"),
    ("immo", "Affaires immobilières"),
    ("espaces-publics", "Aménagement des espaces publics"),
    ("batiments-communaux", "Bâtiments communaux"),
    ("animaux", "Bien-être animal"),
    ("communication", "Communication & Relations extérieures"),
    ("cultes", "Cultes"),
    ("culture", "Culture & Folklore"),
    ("economie", "Développement économique & commercial"),
    ("enseignement", "Enseignement"),
    ("population", "État civil & Population"),
    ("finances", "Finances"),
    ("informatique", "Informatique"),
    ("interculturalite", "Interculturalité & Égalité"),
    ("jeunesse", "Jeunesse"),
    ("logement", "Logement & Énergie"),
    ("mobilite", "Mobilité"),
    ("quartier", "Participation relation avec les quartiers"),
    ("patrimoine", "Patrimoine"),
    ("enfance", "Petite enfance"),
    ("politique", "Politique générale"),
    ("environnement", "Propreté & Environnement"),
    ("sante", "Santé"),
    ("securite", "Sécurité & Prévention"),
    ("social", "Services sociaux"),
    ("sport", "Sport"),
    ("tourisme", "Tourisme"),
    ("urbanisme", "Urbanisme & Aménagement du territoire"),
    ("police", "Zone de police"),
]


def add_portal_category(portal, meeting_config_id="meeting-config-council", is_classifier=False):
    meeting_config = portal.portal_plonemeeting.get(meeting_config_id)
    folder = is_classifier and meeting_config.classifiers or meeting_config.categories
    for cat_id, cat_title in CATEGORIES:
        api.content.create(
            container=folder, type="meetingcategory", id=cat_id, title=cat_title
        )
