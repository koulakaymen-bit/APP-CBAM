#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APPLICATION CBAM/ESG UNIVERSELLE - MULTI-SECTEURS
Dashboard + Questionnaire Dynamique + Évaluation Maturité + Analyse SWOT
Secteurs couverts: Aluminium, Ciment, Acier, Engrais, Hydrogène, Électricité

Exécuter avec: streamlit run app_cbam_universel.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
import json

# ============================================================================
# CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="CBAM/ESG Universal Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1F4E78 0%, #2E7D32 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1F4E78;
        margin-bottom: 1rem;
    }
    .kpi-box {
        background: linear-gradient(135deg, #E3F2FD 0%, #C8E6C9 100%);
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .kpi-value {
        font-size: 2.5em;
        font-weight: bold;
        color: #1F4E78;
    }
    .kpi-label {
        font-size: 0.9em;
        color: #666;
        margin-top: 0.5rem;
    }
    .alert-critical {
        background: #FFEBEE;
        border-left: 4px solid #C62828;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .alert-warning {
        background: #FFF3E0;
        border-left: 4px solid #F57C00;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .alert-success {
        background: #E8F5E9;
        border-left: 4px solid #2E7D32;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .alert-info {
        background: #E3F2FD;
        border-left: 4px solid #1976D2;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .question-card {
        background: #F5F5F5;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid #4CAF50;
    }
    .maturity-card {
        background: #F5F5F5;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid #FF9800;
    }
    .stButton>button {
        background: linear-gradient(135deg, #1F4E78 0%, #2E7D32 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .scenario-card {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .maturity-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        margin: 0.5rem;
    }
    .maturity-beginner {
        background: #FFEBEE;
        color: #C62828;
    }
    .maturity-intermediate {
        background: #FFF3E0;
        color: #F57C00;
    }
    .maturity-advanced {
        background: #E8F5E9;
        color: #2E7D32;
    }
    .maturity-highlight {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 8px 16px rgba(0,0,0,0.2); }
        50% { transform: scale(1.02); box-shadow: 0 12px 24px rgba(0,0,0,0.3); }
        100% { transform: scale(1); box-shadow: 0 8px 16px rgba(0,0,0,0.2); }
    }
    .maturity-score {
        font-size: 4em;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .maturity-label {
        font-size: 1.5em;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .dynamic-input {
        background: #FFF8E1;
        border: 2px solid #FFB300;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .sector-selector {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .swot-box {
        padding: 1.5rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .swot-strengths {
        background: #E8F5E9;
        border-left: 5px solid #2E7D32;
    }
    .swot-weaknesses {
        background: #FFEBEE;
        border-left: 5px solid #C62828;
    }
    .swot-opportunities {
        background: #E3F2FD;
        border-left: 5px solid #1976D2;
    }
    .swot-threats {
        background: #FFF3E0;
        border-left: 5px solid #F57C00;
    }
    .info-icon {
        display: inline-block;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: linear-gradient(135deg, #1976D2 0%, #0d47a1 100%);
        color: white;
        text-align: center;
        line-height: 24px;
        font-size: 13px;
        font-weight: bold;
        margin-left: 8px;
        cursor: help;
        vertical-align: middle;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(25, 118, 210, 0.3);
    }
    .info-icon:hover {
        background: linear-gradient(135deg, #0d47a1 0%, #1976D2 100%);
        box-shadow: 0 4px 8px rgba(25, 118, 210, 0.5);
        transform: scale(1.1);
    }
    .question-header {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 8px;
        margin-bottom: 1rem;
    }
    .sections-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 12px;
        margin-bottom: 2rem;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 10px;
    }
    .section-button {
        padding: 12px 16px;
        border: 2px solid #ddd;
        background: white;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.3s ease;
        text-align: center;
        color: #333;
    }
    .section-button:hover {
        border-color: #1976D2;
        background: #E3F2FD;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .section-button.active {
        background: linear-gradient(135deg, #1976D2 0%, #0d47a1 100%);
        border-color: #1976D2;
        color: white;
        box-shadow: 0 4px 12px rgba(25, 118, 210, 0.4);
    }
    .scope-container {
        margin-bottom: 2rem;
        border-left: 5px solid #1976D2;
        padding-left: 1.5rem;
        background: #f5f7fa;
        padding: 1.5rem;
        border-radius: 8px;
    }
    .scope-header {
        font-size: 1.3em;
        font-weight: bold;
        color: #1F4E78;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .scope-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        background: #1976D2;
        color: white;
        border-radius: 20px;
        font-size: 0.9em;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DONNÉES SECTORIELLES UNIVERSELLES CBAM
# ============================================================================

@st.cache_data
def charger_donnees_sectorielles():
    """Données sectorielles CBAM pour tous les secteurs couverts"""
    return {
        'Aluminium': {
            'unite_production': 'tonnes',
            'benchmark_cbam': 1.479,  # tCO2/t
            'ecp_typique_importe': 11.7,
            'ecp_typique_local': 0.897,
            'emission_process': 0.73,
            'emission_scope1': 0.42,
            'emission_scope2': 0.20,
            'emission_transport': 0.11,
            'description': 'Production d\'aluminium primaire et secondaire',
            'facteurs_emission': {
                'Electricité': 0.5,  # tCO2/MWh
                'Combustible fossile': 2.5,
                'Recyclage': 0.5
            }
        },
        'Ciment': {
            'unite_production': 'tonnes',
            'benchmark_cbam': 0.957,  # tCO2/t clinker (white cement)
            'ecp_typique_importe': 0.85,
            'ecp_typique_local': 0.65,
            'emission_process': 0.52,  # Calcination
            'emission_scope1': 0.35,
            'emission_scope2': 0.05,
            'emission_transport': 0.08,
            'description': 'Production de ciment Portland et ciments spéciaux',
            'facteurs_emission': {
                'Clinker': 0.85,
                'Ciment Portland': 0.65,
                'Ciment blanc': 0.95
            }
        },
        'Acier': {
            'unite_production': 'tonnes',
            'benchmark_cbam': 0.268,  # tCO2/t (EAF high alloy)
            'ecp_typique_importe': 2.3,  # Acier BF/BOF
            'ecp_typique_local': 0.4,  # Acier EAF recyclé
            'emission_process': 0.35,
            'emission_scope1': 0.25,
            'emission_scope2': 0.08,
            'emission_transport': 0.05,
            'description': 'Production d\'acier primaire (BF/BOF) et recyclé (EAF)',
            'facteurs_emission': {
                'Fonte': 1.8,
                'Acier EAF': 0.4,
                'Acier BOF': 2.2,
                'Ferroalliages': 2.0
            }
        },
        'Engrais': {
            'unite_production': 'tonnes',
            'benchmark_cbam': 1.570,  # tCO2/t (Ammonia)
            'ecp_typique_importe': 2.5,
            'ecp_typique_local': 1.8,
            'emission_process': 1.2,
            'emission_scope1': 0.8,
            'emission_scope2': 0.3,
            'emission_transport': 0.1,
            'description': 'Production d\'ammoniac, acides nitrique/sulfurique, engrais NPK',
            'facteurs_emission': {
                'Ammoniac': 1.8,
                'Acide nitrique': 0.3,
                'Engrais NPK': 1.2
            }
        },
        'Hydrogène': {
            'unite_production': 'tonnes',
            'benchmark_cbam': 6.84,  # tCO2/t H2
            'ecp_typique_importe': 12.0,  # Gris (SMR)
            'ecp_typique_local': 4.0,  # Bleu (SMR + CCS)
            'emission_process': 9.0,  # Gris
            'emission_scope1': 8.5,
            'emission_scope2': 0.3,
            'emission_transport': 0.2,
            'description': 'Production d\'hydrogène gris, bleu et vert',
            'facteurs_emission': {
                'H2 Gris (SMR)': 9.0,
                'H2 Bleu (SMR+CCS)': 4.0,
                'H2 Vert (électrolyse)': 0.0
            }
        },
        'Électricité': {
            'unite_production': 'MWh',
            'benchmark_cbam': 0.4,  # tCO2/MWh (exemple)
            'ecp_typique_importe': 0.8,  # Mix charbon/gaz
            'ecp_typique_local': 0.2,  # Mix renouvelable
            'emission_process': 0.0,
            'emission_scope1': 0.0,
            'emission_scope2': 0.0,
            'emission_transport': 0.0,
            'description': 'Production et importation d\'électricité',
            'facteurs_emission': {
                'Charbon': 0.9,
                'Gaz naturel': 0.4,
                'Renouvelable': 0.0,
                'Nucléaire': 0.0
            }
        }
    }

# ============================================================================
# ÉVALUATION DE MATURITÉ UNIVERSELLE
# ============================================================================

def afficher_question_avec_info(question_text, aide_text=None):
    """Affiche une question avec une icône info au survol"""
    if aide_text:
        return f"""
        <div class="question-header">
            <h3>{question_text}
                <span class="info-icon" title="{aide_text}">ℹ️</span>
            </h3>
        </div>
        """
    else:
        return f"<h3>{question_text}</h3>"

def organiser_questions_par_scope(section_data):
    """Organise les questions d'une section par scopes CBAM"""
    scopes = {
        'Scope 1 - Émissions Directes': {
            'emoji': '🏭',
            'description': 'Émissions directes de votre processus de production',
            'color': '#E53935',
            'questions': []
        },
        'Scope 2 - Électricité Indirecte': {
            'emoji': '⚡',
            'description': 'Émissions liées à l\'électricité importée',
            'color': '#F57C00',
            'questions': []
        },
        'Scope 3 - Chaîne d\'Approvisionnement': {
            'emoji': '🚚',
            'description': 'Émissions de votre chaîne d\'approvisionnement',
            'color': '#1976D2',
            'questions': []
        },
        'Gouvernance & Conformité': {
            'emoji': '📋',
            'description': 'Maturité organisationnelle et conformité',
            'color': '#388E3C',
            'questions': []
        }
    }
    
    # Mapping des sections aux scopes
    scope_mapping = {
        'EMISSIONS': 'Scope 1 - Émissions Directes',
        'ENERGIE': 'Scope 2 - Électricité Indirecte',
        'APPROVISIONNEMENT': 'Scope 3 - Chaîne d\'Approvisionnement',
        'DONNEES_BASE': 'Gouvernance & Conformité',
        'CONFORMITE': 'Gouvernance & Conformité',
        'STRATEGIE': 'Gouvernance & Conformité'
    }
    
    # Récupérer la section de la première question
    if section_data.get('questions'):
        section = section_data['questions'][0].get('section', 'DONNEES_BASE')
        primary_scope = scope_mapping.get(section, 'Gouvernance & Conformité')
        
        # Ajouter toutes les questions de cette section au scope principal
        for question in section_data.get('questions', []):
            scopes[primary_scope]['questions'].append(question)
    
    # Retourner seulement les scopes avec des questions
    return {k: v for k, v in scopes.items() if v['questions']}

def calculer_niveau_maturite(reponses_maturite):
    """
    Calcule le niveau de maturité basé sur les réponses
    Retourne: ('beginner'|'intermediate'|'advanced', score_0_100, détails)
    """
    if not reponses_maturite:
        return 'beginner', 0, {}
    
    # Pondération des questions
    poids = {
        'mat_1': 15,  # Connaissance CBAM
        'mat_2': 15,  # Calcul empreinte carbone
        'mat_3': 15,  # Équipe dédiée
        'mat_4': 10,  # Risques climatiques
        'mat_4b': 10,  # Audits externes
        'mat_4c': 10,  # Avantage compétitif
        'mat_5': 10,  # Traçabilité
        'mat_6': 10,  # Certifications
        'mat_7': 15,  # Relations fournisseurs
        'mat_8': 10,  # Stratégie long terme
    }
    
    # Valeurs des réponses (0-3 scale)
    valeurs = {
        'mat_1': {
            'Aucune connaissance': 0,
            'Notions de base': 1,
            'Bonne compréhension': 2,
            'Expertise complète': 3
        },
        'mat_2': {
            'Non, aucune donnée': 0,
            'Partiellement (estimations)': 1,
            'Oui, calcul interne': 2,
            'Oui, audit certifié': 3
        },
        'mat_3': {
            'Non': 0,
            'En projet': 1,
            'Oui, partielle': 2,
            'Oui, équipe complète': 3
        },
        'mat_4': {
            'Aucune analyse': 0,
            'Analyse partielle': 1,
            'Analyse complète documentée': 2,
            'Analyse avec plan d\'adaptation': 3
        },
        'mat_4b': {
            'Non, aucun audit': 0,
            'Audit fragmenté': 1,
            'Audit annuel complet': 2,
            'Audit avec certification tierce': 3
        },
        'mat_4c': {
            'Aucun avantage identifié': 0,
            'Accès à clients sensibles ESG': 1,
            'Premium prix estimé < 5%': 2,
            'Premium prix estimé > 5% + fidélisation clients': 3
        },
        'mat_5': {
            'Aucune traçabilité': 0,
            'Traçabilité manuelle': 1,
            'Système partiel': 2,
            'Système complet digital': 3
        },
        'mat_6': {
            'Aucune': 0,
            'En cours': 1,
            'ISO 14001': 2,
            'ISO 14064 + autres': 3
        },
        'mat_7': {
            'Aucune discussion': 0,
            'Discussions initiales': 1,
            'Engagements verbaux': 2,
            'Contrats signés': 3
        },
        'mat_8': {
            'Aucune stratégie': 0,
            'En réflexion': 1,
            'Stratégie définie': 2,
            'Plan détaillé validé': 3
        }
    }
    
    score_total = 0
    score_max = 0
    details = {}
    
    for q_id, reponse in reponses_maturite.items():
        if q_id in poids and q_id in valeurs:
            valeur = valeurs[q_id].get(reponse, 0)
            points = (valeur / 3) * poids[q_id]
            score_total += points
            score_max += poids[q_id]
            details[q_id] = {
                'reponse': reponse,
                'valeur': valeur,
                'points': points,
                'poids': poids[q_id]
            }
    
    score_pct = (score_total / score_max * 100) if score_max > 0 else 0
    score_5 = score_pct / 20  # Convertir 0-100% en 0-5
    
    # Détermination du niveau
    if score_pct < 35:
        niveau = 'beginner'
    elif score_pct < 70:
        niveau = 'intermediate'
    else:
        niveau = 'advanced'
    
    return niveau, score_5, details

def afficher_resultat_maturite(niveau, score, details):
    """Affiche le résultat de l'évaluation de maturité avec mise en valeur"""
    
    niveaux_info = {
        'beginner': {
            'label': 'Débutant',
            'class': 'maturity-beginner',
            'emoji': '🔴',
            'color': '#C62828',
            'description': 'Votre entreprise commence son parcours de décarbonation',
            'recommandations': [
                'Formation urgente sur les réglementations CBAM',
                'Audit initial de l\'empreinte carbone',
                'Constitution d\'une équipe projet',
                'Identification des fournisseurs bas-carbone'
            ]
        },
        'intermediate': {
            'label': 'Intermédiaire',
            'class': 'maturity-intermediate',
            'emoji': '🟠',
            'color': '#F57C00',
            'description': 'Votre entreprise a entamé sa transformation',
            'recommandations': [
                'Finaliser la certification ISO 14064',
                'Déployer système de traçabilité complet',
                'Négocier avec fournisseurs bas-carbone',
                'Étude de faisabilité énergie verte'
            ]
        },
        'advanced': {
            'label': 'Avancé',
            'class': 'maturity-advanced',
            'emoji': '🟢',
            'color': '#2E7D32',
            'description': 'Votre entreprise est bien positionnée',
            'recommandations': [
                'Viser l\'excellence carbone',
                'Transition vers électricité 100% verte',
                'Certification carbone neutre',
                'Leadership sur le marché "vert"'
            ]
        }
    }
    
    info = niveaux_info[niveau]
    
    # Calculate percentage score
    score_pct = score * 20  # Convert from 5-point scale to 100%
    
    # Affichage mis en valeur du degré de maturité
    st.markdown(f"""
    <div class="maturity-highlight" style="background: linear-gradient(135deg, {info['color']} 0%, #764ba2 100%);">
        <div class="maturity-label">{info['emoji']} NIVEAU DE MATURITÉ</div>
        <div class="maturity-score">{score:.2f}/5 ({score_pct:.1f}%)</div>
        <div style="font-size: 2em; font-weight: bold; margin: 1rem 0;">{info['label'].upper()}</div>
        <div style="font-size: 1.2em; opacity: 0.9;">{info['description']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 🎯 Recommandations Prioritaires pour votre niveau:")
    for i, rec in enumerate(info['recommandations'], 1):
        st.markdown(f"{i}. {rec}")
    
    # Graphique radar
    if details:
        categories = []
        valeurs_obtenues = []
        valeurs_max = []
        
        labels_questions = {
            'mat_1': 'Connaissance CBAM',
            'mat_2': 'Calcul carbone',
            'mat_3': 'Équipe dédiée',
            'mat_4': 'Risques climatiques',
            'mat_4b': 'Audits externes',
            'mat_4c': 'Avantage compétitif',
            'mat_5': 'Traçabilité',
            'mat_6': 'Certifications',
            'mat_7': 'Fournisseurs',
            'mat_8': 'Stratégie'
        }
        
        for q_id, detail in details.items():
            if q_id in labels_questions:
                categories.append(labels_questions[q_id])
                valeurs_obtenues.append(detail['points'])
                valeurs_max.append(detail['poids'])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=valeurs_obtenues + [valeurs_obtenues[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='Votre Score',
            line_color='#1F4E78'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=valeurs_max + [valeurs_max[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='Maximum',
            line_color='#2E7D32',
            opacity=0.3
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, max(valeurs_max)])),
            showlegend=True,
            title="Profil de Maturité par Dimension"
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# QUESTIONNAIRE DYNAMIQUE UNIVERSEL
# ============================================================================

@st.cache_data
def construire_questionnaire_universel():
    """Structure du questionnaire universel adaptable à tous les secteurs"""
    questionnaire_raw = {
        'MATURITE': {
            'titre': '🎯 Évaluation de Maturité CBAM/ESG',
            'color': '#FF9800',
            'description': 'Cette évaluation permet d\'adapter les recommandations à votre situation',
            'questions': [
                {
                    'id': 'mat_1',
                    'question': 'Quel est votre niveau de connaissance du CBAM ?',
                    'type': 'radio',
                    'options': [
                        'Aucune connaissance',
                        'Notions de base',
                        'Bonne compréhension',
                        'Expertise complète'
                    ],
                    'aide': 'Le CBAM impose des taxes sur les émissions carbone des produits importés dans l\'UE'
                },
                {
                    'id': 'mat_2',
                    'question': 'Avez-vous déjà calculé votre empreinte carbone (ECP) ?',
                    'type': 'radio',
                    'options': [
                        'Non, aucune donnée',
                        'Partiellement (estimations)',
                        'Oui, calcul interne',
                        'Oui, audit certifié'
                    ],
                    'aide': 'L\'ECP mesure les émissions de CO2 par unité de produit'
                },
                {
                    'id': 'mat_3',
                    'question': 'Disposez-vous d\'une équipe dédiée à la décarbonation ?',
                    'type': 'radio',
                    'options': [
                        'Non',
                        'En projet',
                        'Oui, partielle',
                        'Oui, équipe complète'
                    ],
                    'aide': 'Une équipe dédiée est essentielle pour piloter la transformation'
                },
                {
                    'id': 'mat_4',
                    'question': 'Avez-vous une analyse des risques climatiques dans votre activité ?',
                    'type': 'radio',
                    'options': [
                        'Aucune analyse',
                        'Analyse partielle',
                        'Analyse complète documentée',
                        'Analyse avec plan d\'adaptation'
                    ],
                    'aide': 'Identifier les risques climatiques (chaîne d\'approvisionnement, produits, régulation) est essentiel'
                },
                {
                    'id': 'mat_4b',
                    'question': 'Réalisez-vous des audits externes sur votre empreinte carbone et votre gouvernance ESG ?',
                    'type': 'radio',
                    'options': [
                        'Non, aucun audit',
                        'Audit fragmenté',
                        'Audit annuel complet',
                        'Audit avec certification tierce'
                    ],
                    'aide': 'Les audits externes valident vos calculs et renforcent la crédibilité auprès des clients/régulateurs'
                },
                {
                    'id': 'mat_4c',
                    'question': 'Quel est votre avantage compétitif lié à la décarbonation sur le marché ?',
                    'type': 'radio',
                    'options': [
                        'Aucun avantage identifié',
                        'Accès à clients sensibles ESG',
                        'Premium prix estimé < 5%',
                        'Premium prix estimé > 5% + fidélisation clients'
                    ],
                    'aide': 'Mesurer l\'impact commercial de la décarbonation aide à justifier les investissements'
                },
                {
                    'id': 'mat_5',
                    'question': 'Niveau de traçabilité de vos émissions carbone ?',
                    'type': 'radio',
                    'options': [
                        'Aucune traçabilité',
                        'Traçabilité manuelle',
                        'Système partiel',
                        'Système complet digital'
                    ],
                    'aide': 'Le CBAM exige une traçabilité précise des émissions par lot'
                },
                {
                    'id': 'mat_6',
                    'question': 'Certifications environnementales obtenues ?',
                    'type': 'radio',
                    'options': [
                        'Aucune',
                        'En cours',
                        'ISO 14001',
                        'ISO 14064 + autres'
                    ],
                    'aide': 'Les certifications facilitent la conformité CBAM'
                },
                {
                    'id': 'mat_7',
                    'question': 'Relations avec fournisseurs bas-carbone ?',
                    'type': 'radio',
                    'options': [
                        'Aucune discussion',
                        'Discussions initiales',
                        'Engagements verbaux',
                        'Contrats signés'
                    ],
                    'aide': 'Les fournisseurs locaux/faible émission réduisent significativement l\'ECP'
                },
                {
                    'id': 'mat_8',
                    'question': 'Avez-vous une stratégie de décarbonation long terme ?',
                    'type': 'radio',
                    'options': [
                        'Aucune stratégie',
                        'En réflexion',
                        'Stratégie définie',
                        'Plan détaillé validé'
                    ],
                    'aide': 'Une roadmap 2025-2030 est essentielle pour anticiper le CBAM'
                }
            ]
        },
        'DONNEES_BASE': {
            'titre': '📊 Données de Base Entreprise',
            'color': '#1F4E78',
            'questions': [
                {
                    'id': 'db_1',
                    'question': 'Production annuelle (tonnes ou MWh selon secteur)',
                    'type': 'number',
                    'valeur_defaut': 10000,
                    'min': 0,
                    'max': 1000000,
                    'aide': 'Volume total produit annuellement'
                },

                {
                    'id': 'db_3',
                    'question': 'Principaux marchés d\'exportation',
                    'type': 'multiselect',
                    'options': [
                        'Union Européenne (France, Allemagne, Italie)',
                        'Afrique du Nord',
                        'Afrique Subsaharienne',
                        'Moyen-Orient',
                        'Asie',
                        'Amériques',
                        'Autres'
                    ],
                    'aide': 'Le CBAM s\'applique uniquement aux exportations vers l\'UE'
                },
                {
                    'id': 'db_4',
                    'question': 'Part des exportations vers l\'UE (%)',
                    'type': 'slider',
                    'valeur_defaut': 60,
                    'min': 0,
                    'max': 100,
                    'aide': 'Seules les exportations UE sont soumises au CBAM'
                },
                {
                    'id': 'db_5',
                    'question': 'Secteur d\'activité principal',
                    'type': 'radio',
                    'options': [
                        'Aluminium',
                        'Ciment',
                        'Acier',
                        'Engrais',
                        'Hydrogène',
                        'Électricité',
                        'Autre industrie lourde'
                    ],
                    'aide': 'Sélectionnez votre secteur pour adapter les benchmarks'
                }
            ]
        },
        'EMISSIONS': {
            'titre': '🏭 Émissions & Empreinte Carbone',
            'color': '#C62828',
            'questions': [
                {
                    'id': 'em_1',
                    'question': 'Avez-vous calculé votre ECP (Empreinte Carbone Produit) ?',
                    'type': 'radio',
                    'options': ['Oui, certifié', 'Oui, interne', 'Estimation', 'Non'],
                    'aide': 'ECP = kg CO2 par unité de produit'
                },
                {
                    'id': 'em_2',
                    'question': 'Sources d\'émissions identifiées (Scope 1+2+3)',
                    'type': 'multiselect',
                    'options': [
                        'Matières premières importées (Scope 3)',
                        'Consommation électricité (Scope 2)',
                        'Process industriels (Scope 1)',
                        'Transport/Logistique (Scope 3)',
                        'Autres intrants'
                    ],
                    'aide': 'Les matières premières représentent souvent 60-90% des émissions!'
                },
                {
                    'id': 'em_3',
                    'question': 'Disposez-vous d\'un système de monitoring temps réel ?',
                    'type': 'radio',
                    'options': ['Oui, complet', 'Partiel', 'En projet', 'Non'],
                    'aide': 'Le CBAM exige un reporting trimestriel précis'
                },
                {
                    'id': 'em_4',
                    'question': 'Émissions Scope 1 directes (tCO2/an)',
                    'type': 'number',
                    'valeur_defaut': 5000,
                    'min': 0,
                    'max': 1000000,
                    'aide': 'Combustion sur site, process industriels'
                },
                {
                    'id': 'em_5',
                    'question': 'Émissions Scope 2 indirectes (tCO2/an)',
                    'type': 'number',
                    'valeur_defaut': 2000,
                    'min': 0,
                    'max': 1000000,
                    'aide': 'Consommation d\'électricité, chaleur, vapeur'
                }
            ]
        },
        'ENERGIE': {
            'titre': '⚡ Énergie & Process',
            'color': '#2E7D32',
            'description': 'Intégration de l\'énergie, des process industriels et calculs CBAM détaillés',
            'questions': [
                {
                    'id': 'en_1',
                    'question': 'Source d\'électricité actuelle',
                    'type': 'radio',
                    'options': [
                        'Réseau national (mix carboné)',
                        'Partiellement renouvelable',
                        '100% renouvelable',
                        'Autoproduction'
                    ],
                    'aide': 'Électricité verte réduit significativement Scope 2'
                },
                {
                    'id': 'en_2',
                    'question': 'Projet transition énergie verte',
                    'type': 'radio',
                    'options': ['En cours', 'Planifié < 2 ans', 'À l\'étude', 'Aucun'],
                    'aide': 'Transition énergétique = levier majeur de réduction'
                },
                {
                    'id': 'en_3',
                    'question': 'Optimisations process identifiées',
                    'type': 'multiselect',
                    'options': [
                        'Efficacité énergétique',
                        'Récupération chaleur',
                        'Optimisation process',
                        'Réduction déchets',
                        'Aucune'
                    ],
                    'aide': 'Gains marginaux mais cumulatifs significatifs'
                },

                {
                    'id': 'en_5',
                    'question': 'Consommation d\'électricité annuelle',
                    'type': 'number',
                    'valeur_defaut': 50000,
                    'min': 0,
                    'max': 10000000,
                    'aide': 'Consommation annuelle en MWh'
                },
                {
                    'id': 'en_6',
                    'question': 'Consommation de gaz annuelle',
                    'type': 'number',
                    'valeur_defaut': 30000,
                    'min': 0,
                    'max': 10000000,
                    'aide': 'Consommation annuelle en MWh (équivalent énergétique)'
                },
                {
                    'id': 'cbam_ad',
                    'question': 'Données d\'activité (AD)',
                    'type': 'number',
                    'valeur_defaut': 2394000,
                    'min': 0,
                    'max': 100000000,
                    'aide': 'Ex: 2 394 000 Nm³ gaz naturel ou équivalent en unités physiques'
                },
                {
                    'id': 'cbam_ncv',
                    'question': 'Pouvoir calorifique net (NCV)',
                    'type': 'number',
                    'valeur_defaut': 1,
                    'min': 0.1,
                    'max': 100,
                    'aide': 'MWh/unité AD ou coefficient de conversion standard'
                },
                {
                    'id': 'cbam_ef',
                    'question': 'Facteur d\'émission (EF)',
                    'type': 'number',
                    'valeur_defaut': 1.9,
                    'min': 0,
                    'max': 10,
                    'aide': 'tCO2/1000 unités AD (ex: 1.9 pour gaz naturel)'
                },
                {
                    'id': 'cbam_oxf',
                    'question': 'Facteur d\'oxydation (OxF)',
                    'type': 'number',
                    'valeur_defaut': 100,
                    'min': 0,
                    'max': 100,
                    'aide': 'En pourcentage (100% par défaut pour combustion totale)'
                },
                {
                    'id': 'cbam_bioc',
                    'question': 'Teneur biomasse (BioC)',
                    'type': 'number',
                    'valeur_defaut': 0,
                    'min': 0,
                    'max': 100,
                    'aide': 'En pourcentage (0% par défaut, biocarburants > 0%)'
                },
                {
                    'id': 'cbam_emissions_process',
                    'question': 'Émissions directes attribuées au process (tCO2)',
                    'type': 'calculated',
                    'formula': 'ad * ncv * ef * (oxf/100) * (1 - bioc/100)',
                    'dependencies': ['cbam_ad', 'cbam_ncv', 'cbam_ef', 'cbam_oxf', 'cbam_bioc'],
                    'valeur_defaut': 20908,
                    'min': 0,
                    'max': 100000000,
                    'aide': 'Résultat combustion: AD × NCV × EF × OxF × (1 - BioC/100) - Calculé automatiquement'
                },
                {
                    'id': 'cbam_production_totale',
                    'question': 'Production totale du process (tonnes)',
                    'type': 'number',
                    'valeur_defaut': 16284,
                    'min': 1,
                    'max': 10000000,
                    'aide': 'Production en tonnes (extrusion, peinture, anodisation, etc.)'
                },
                {
                    'id': 'cbam_electricite_mwh_t',
                    'question': 'Électricité consommée par tonne produite (MWh/t)',
                    'type': 'number',
                    'valeur_defaut': 0.343,
                    'min': 0,
                    'max': 100,
                    'aide': 'Ex: 0.343 MWh/t (extrusion), 0.399 (peinture), 1.036 (anodisation)'
                },
                {
                    'id': 'cbam_ef_electricite',
                    'question': 'Facteur d\'émission électricité (tCO2/MWh)',
                    'type': 'number',
                    'valeur_defaut': 0.4,
                    'min': 0,
                    'max': 1.5,
                    'aide': 'Méthode D.2.4 - mix électricité nationale (0.0 renouvelable, 0.4 carboné)'
                },

                {
                    'id': 'cbam_pct_emissions_couvertes',
                    'question': 'Pourcentage émissions couvertes par carbon price',
                    'type': 'number',
                    'valeur_defaut': 100,
                    'min': 0,
                    'max': 100,
                    'aide': 'En pourcentage (100% par défaut si tous process couverts)'
                },

            ]
        },
        'APPROVISIONNEMENT': {
            'titre': '🚚 Approvisionnement & Matières Premières',
            'color': '#F57C00',
            'description': 'Gestion de la chaîne d\'approvisionnement et matières premières',
            'questions': [
                {
                    'id': 'ap_1',
                    'question': 'Origine principale des matières premières',
                    'type': 'multiselect',
                    'options': [
                        'Locale (pays d\'installation)',
                        'UE voisine',
                        'Chine',
                        'Moyen-Orient',
                        'Afrique',
                        'Amériques',
                        'Autres'
                    ],
                    'aide': 'L\'origine impacte fortement l\'empreinte carbone Scope 3'
                },
                {
                    'id': 'ap_2',
                    'question': 'Vos fournisseurs peuvent-ils fournir des données d\'empreinte carbone ?',
                    'type': 'radio',
                    'options': ['Oui, certifiées', 'Oui, déclaratives', 'Incertain', 'Non'],
                    'aide': 'Obligatoire pour déclaration CBAM - sinon valeurs par défaut majorées'
                },
                {
                    'id': 'ap_3',
                    'question': '% Matière Première Locale & Bas-Carbone + ECP Ajusté',
                    'type': 'compound',
                    'aide': 'Entrez le % de MP locales. Les autres fournisseurs complèteront automatiquement à 100%. Fournissez aussi l\'ECP ajusté pour les MP locales.',
                    'fields': [
                        {
                            'name': 'pct_local',
                            'label': '% Matières Premières Locales',
                            'type': 'slider',
                            'valeur_defaut': 38,
                            'min': 0,
                            'max': 100,
                            'unite': '%'
                        },
                        {
                            'name': 'ecp_local',
                            'label': 'ECP des Matières Premières Locales',
                            'type': 'number',
                            'valeur_defaut': 1.5,
                            'min': 0,
                            'max': 20,
                            'unite': 'tCO2/tonne',
                            'aide': 'Empreinte carbone spécifique des MP locales'
                        }
                    ]
                },
                {
                    'id': 'ap_4',
                    'question': 'Fournisseurs Autres - Proportion & ECP (Les MP Locales complètent à 100%)',
                    'type': 'suppliers',
                    'aide': 'Entrez vos autres fournisseurs (hors MP locales). Leur proportion totale + MP locales doit = 100%. Les proportions doivent être saisies pour totaliser (100% - % MP locales).',
                    'auto_calculate': True,
                    'depends_on': 'ap_3',
                    'suppliers': [
                        {
                            'nom': 'Fournisseur Standard 1',
                            'proportion': 35.0,
                            'ecp': 2.8
                        },
                        {
                            'nom': 'Fournisseur Standard 2',
                            'proportion': 27.0,
                            'ecp': 3.5
                        }
                    ]
                },
                {
                    'id': 'ap_5',
                    'question': 'Types de matières premières principales',
                    'type': 'multiselect',
                    'options': [
                        'Minerais',
                        'Métaux recyclés',
                        'Produits chimiques',
                        'Combustibles fossiles',
                        'Biomasse',
                        'Autres'
                    ],
                    'aide': 'Sélectionnez les types de matières premières que vous utilisez'
                }
            ]
        },
        'CONFORMITE': {
            'titre': '📋 Conformité & Reporting',
            'color': '#1976D2',
            'questions': [
                {
                    'id': 'co_1',
                    'question': 'Connaissance des obligations CBAM',
                    'type': 'radio',
                    'options': [
                        'Expertise complète',
                        'Bonne compréhension',
                        'Notions de base',
                        'Aucune'
                    ],
                    'aide': 'Déclaration T1 2026 obligatoire dans 11 mois'
                },
                {
                    'id': 'co_2',
                    'question': 'Responsable désigné pour déclarations CBAM',
                    'type': 'radio',
                    'options': ['Oui, formé', 'Oui, à former', 'En recrutement', 'Non'],
                    'aide': 'Reporting trimestriel complexe nécessite expertise dédiée'
                },
                {
                    'id': 'co_3',
                    'question': 'Logiciel/Système préparation déclarations CBAM',
                    'type': 'radio',
                    'options': ['Déployé', 'En cours', 'Sélection', 'Aucun'],
                    'aide': 'Outils nécessaires pour calculs et reporting conformes'
                }
            ]
        },
        'STRATEGIE': {
            'titre': '🎯 Stratégie & Investissements',
            'color': '#7B1FA2',
            'questions': [
                {
                    'id': 'st_1',
                    'question': 'Objectif de réduction d\'empreinte carbone',
                    'type': 'radio',
                    'options': [
                        'Atteindre benchmark CBAM',
                        'Réduire de 50%',
                        'Réduire de 30%',
                        'Non défini'
                    ],
                    'aide': 'Objectif SMART essentiel pour piloter la transformation'
                },
                {
                    'id': 'st_2',
                    'question': 'Budget disponible pour décarbonation',
                    'type': 'radio',
                    'options': [
                        '> 2M EUR',
                        '500k - 2M EUR',
                        '100k - 500k EUR',
                        '< 100k EUR'
                    ],
                    'aide': 'ROI généralement < 3 ans avec économie CBAM'
                },
                {
                    'id': 'st_3',
                    'question': 'Horizon de mise en conformité',
                    'type': 'radio',
                    'options': [
                        '< 12 mois (urgent)',
                        '12-24 mois',
                        '24-36 mois',
                        '> 36 mois'
                    ],
                    'aide': 'Première déclaration: T1 2026 | Paiements: 2027'
                },
                {
                    'id': 'st_4',
                    'question': 'Recherche de financements (EU, BEI, AFD)',
                    'type': 'radio',
                    'options': ['Dossier déposé', 'En cours', 'Planifié', 'Non'],
                    'aide': 'Subventions disponibles pour décarbonation industrie'
                }
            ]
        }
    }
    
    # Ajouter automatiquement le champ 'section' à chaque question
    for section_key, section_data in questionnaire_raw.items():
        if section_key != 'MATURITE' and 'questions' in section_data:
            for question in section_data['questions']:
                question['section'] = section_key
    
    return questionnaire_raw

def calculer_score_maturite(reponses):
    """Calcule un score global basé sur les réponses"""
    if not reponses:
        return 0
    
    scores_par_question = {
        # Données de base
        'db_2': lambda x: min(x, 100) if isinstance(x, (int, float)) else 0,
        'db_4': lambda x: x if isinstance(x, (int, float)) else 0,
        
        # Émissions
        'em_1': lambda x: {'Oui, certifié': 100, 'Oui, interne': 75, 'Estimation': 50, 'Non': 0}.get(x, 0),
        'em_3': lambda x: {'Oui, complet': 100, 'Partiel': 66, 'En projet': 33, 'Non': 0}.get(x, 0),
        
        # Approvisionnement
        'ap_2': lambda x: {'Oui, certifiées': 100, 'Oui, déclaratives': 66, 'Incertain': 33, 'Non': 0}.get(x, 0),
        'ap_3': lambda x: min(x.get('pct_local', 0), 100) if isinstance(x, dict) else {'Oui, jusqu\'à 100% besoins': 100, 'Oui, jusqu\'à 70%': 75, 'Limité à 50%': 50, 'Incertain': 0}.get(x, 0),
        
        # Énergie
        'en_1': lambda x: {'100% renouvelable': 100, 'Partiellement renouvelable': 66, 'Autoproduction': 50, 'Réseau national (mix carboné)': 0}.get(x, 0),
        'en_2': lambda x: {'En cours': 100, 'Planifié < 2 ans': 75, 'À l\'étude': 50, 'Aucun': 0}.get(x, 0),
        
        # Conformité
        'co_1': lambda x: {'Expertise complète': 100, 'Bonne compréhension': 75, 'Notions de base': 50, 'Aucune': 0}.get(x, 0),
        'co_2': lambda x: {'Oui, formé': 100, 'Oui, à former': 75, 'En recrutement': 50, 'Non': 0}.get(x, 0),
        'co_3': lambda x: {'Déployé': 100, 'En cours': 66, 'Sélection': 33, 'Aucun': 0}.get(x, 0),
        
        # Stratégie
        'st_1': lambda x: {'Atteindre benchmark CBAM': 100, 'Réduire de 50%': 75, 'Réduire de 30%': 50, 'Non défini': 0}.get(x, 0),
        'st_3': lambda x: {'< 12 mois (urgent)': 100, '12-24 mois': 75, '24-36 mois': 50, '> 36 mois': 0}.get(x, 0),
    }
    
    total = 0
    count = 0
    
    for q_id, valeur in reponses.items():
        if q_id in scores_par_question:
            total += scores_par_question[q_id](valeur)
            count += 1
    
    return (total / count) if count > 0 else 0

# ============================================================================
# ANALYSE SWOT
# ============================================================================

def calculer_ecp_complet(reponses, data_sector, production, source_electricite='Réseau national (mix carboné)'):
    """
    Calcule l'ECP complet incluant:
    - Matières premières locales et fournisseurs
    - Émissions process
    - Émissions énergétiques (électricité + gaz)
    """
    # Matières premières
    ap_3_data = reponses.get('ap_3', {})
    if isinstance(ap_3_data, dict) and ap_3_data:
        pct_local_mp = ap_3_data.get('pct_local', 40) / 100
        ecp_local_mp = ap_3_data.get('ecp_local', 1.5)
    else:
        pct_local_mp = reponses.get('db_2', 40) / 100
        ecp_local_mp = 1.5
    
    # Calcul ECP pondéré matières premières
    ecp_calc = ecp_local_mp * pct_local_mp
    
    # Ajouter contribution des autres fournisseurs
    pct_others = 1 - pct_local_mp
    if pct_others > 0:
        suppliers = reponses.get('ap_4', [])
        if suppliers:
            total_prop_suppliers = sum(float(s.get('proportion', 0)) for s in suppliers)
            if total_prop_suppliers > 0:
                for supplier in suppliers:
                    prop = float(supplier.get('proportion', 0)) / 100
                    ecp_supplier = float(supplier.get('ecp', 0))
                    ecp_calc += ecp_supplier * prop
            else:
                ecp_calc += data_sector['ecp_typique_importe'] * pct_others
        else:
            ecp_calc += data_sector['ecp_typique_importe'] * pct_others
    
    # Ajouter process emissions
    ecp_calc += data_sector['emission_process']
    
    # Ajouter les émissions d'électricité et de gaz
    consommation_electricite = reponses.get('en_5', 50000)  # MWh
    consommation_gaz = reponses.get('en_6', 30000)  # MWh
    
    facteur_emission_gaz = 0.2  # tCO2/MWh
    
    # Facteur d'émission de l'électricité selon la source
    if source_electricite == '100% renouvelable':
        facteur_emission_electricite = 0.0
    elif source_electricite == 'Partiellement renouvelable':
        facteur_emission_electricite = 0.2
    elif source_electricite == 'Autoproduction':
        facteur_emission_electricite = 0.15
    else:  # Réseau national (mix carboné)
        facteur_emission_electricite = 0.4
    
    # Calcul des émissions énergétiques
    emissions_electricite_annuelles = consommation_electricite * facteur_emission_electricite
    emissions_gaz_annuelles = consommation_gaz * facteur_emission_gaz
    emissions_energetiques_totales = emissions_electricite_annuelles + emissions_gaz_annuelles
    
    # Convertir en tCO2 par unité de production
    emissions_energetiques_par_unite = emissions_energetiques_totales / production if production > 0 else 0
    
    # Ajouter au calcul ECP
    ecp_calc += emissions_energetiques_par_unite
    
    return ecp_calc

def calculer_cbam_complet(reponses):
    """
    Calcule les SEE (Scope Emissions Embedded) selon les formules CBAM officielles
    
    Formules CBAM pour Aluminium:
    1. Émissions directes (combustion) = AD × NCV × EF × OxF × (1 - BioC)
    2. SEE_direct = Émissions directes / Production totale
    3. SEE_indirect = Électricité consommée (MWh/t) × Facteur d'émission électricité (tCO2/MWh)
    4. SEE_total = SEE_direct + SEE_indirect
    5. CP_effectif = SEE_couvert × CP - Rabais
    6. SEE_précurseur_attribuée = SEE_précurseur × (quantité_précurseur / production_totale)
    """
    
    resultats = {}
    
    # ==========================================
    # 1. ÉMISSIONS DIRECTES (COMBUSTION)
    # ==========================================
    ad = float(reponses.get('cbam_ad', 2394000))  # Données d'activité
    ncv = float(reponses.get('cbam_ncv', 1))  # Pouvoir calorifique net
    ef = float(reponses.get('cbam_ef', 1.9))  # Facteur d'émission
    oxf = float(reponses.get('cbam_oxf', 100)) / 100  # Facteur d'oxydation (convertir % en décimal)
    bioc = float(reponses.get('cbam_bioc', 0)) / 100  # Teneur biomasse (convertir % en décimal)
    
    # Formule: AD × NCV × EF × OxF × (1 - BioC)
    emissions_directes_combustion = ad * ncv * ef * oxf * (1 - bioc)
    resultats['emissions_directes_combustion_tco2'] = emissions_directes_combustion
    
    # ==========================================
    # 2. SEE DIRECT (émissions attribuées / production)
    # ==========================================
    emissions_process = float(reponses.get('cbam_emissions_process', 20908))  # tCO2
    production_totale = float(reponses.get('cbam_production_totale', 16284))  # tonnes
    
    if production_totale > 0:
        see_direct = emissions_process / production_totale
    else:
        see_direct = 0
    
    resultats['see_direct_tco2_par_t'] = see_direct
    
    # ==========================================
    # 3. SEE INDIRECT (électricité)
    # ==========================================
    electricite_mwh_t = float(reponses.get('cbam_electricite_mwh_t', 0.343))  # MWh/tonne
    ef_electricite = float(reponses.get('cbam_ef_electricite', 0.4))  # tCO2/MWh
    
    # Formule: Électricité (MWh/t) × Facteur d'émission (tCO2/MWh)
    see_indirect = electricite_mwh_t * ef_electricite
    resultats['see_indirect_tco2_par_t'] = see_indirect
    
    # ==========================================
    # 4. SEE TOTAL
    # ==========================================
    see_total = see_direct + see_indirect
    resultats['see_total_tco2_par_t'] = see_total
    
    # ==========================================
    # 5. PRIX CARBONE EFFECTIF
    # ==========================================
    carbon_price = float(reponses.get('cbam_carbon_price', 0))  # EUR/tCO2
    pct_emissions_couvertes = float(reponses.get('cbam_pct_emissions_couvertes', 100)) / 100
    rebate_amount = float(reponses.get('cbam_rebate_amount', 0))  # EUR
    
    # Formule: CP_effectif = SEE_couvert × CP - Rabais
    see_couvert = see_total * pct_emissions_couvertes
    cp_effectif = (see_couvert * carbon_price) - rebate_amount
    
    resultats['see_couvert_tco2_par_t'] = see_couvert
    resultats['carbon_price_effectif_eur_par_t'] = cp_effectif / production_totale if production_totale > 0 else 0
    resultats['carbon_price_effectif_total_eur'] = cp_effectif
    
    # Détails pour affichage
    resultats['_details'] = {
        'ad': ad,
        'ncv': ncv,
        'ef': ef,
        'oxf_pct': oxf * 100,
        'bioc_pct': bioc * 100,
        'emissions_process_tco2': emissions_process,
        'production_totale_t': production_totale,
        'electricite_mwh_t': electricite_mwh_t,
        'ef_electricite_tco2_mwh': ef_electricite,
        'carbon_price_eur_tco2': carbon_price,
        'pct_emissions_couvertes': pct_emissions_couvertes * 100,
        'rebate_eur': rebate_amount
    }
    
    return resultats

def generer_swot(secteur, niveau_maturite, reponses):
    """
    Génère une analyse SWOT personnalisée basée sur le secteur et les réponses
    """
    
    # Vérifier que le secteur est valide
    if not secteur:
        secteur = 'Aluminium'
    
    # Forces par défaut selon secteur
    forces_sectorielles = {
        'Aluminium': [
            'Potentiel de recyclage infini de l\'aluminium',
            'Existence de fournisseurs locaux bas-carbone (ALUFOND)',
            'Technologies de production éco-éfficaces disponibles',
            'Fortes économies d\'échelle possibles'
        ],
        'Ciment': [
            'Matériau de construction indispensable',
            'Alternatives bas-carbone en développement (LC3)',
            'Potentiel de substitution partielle du clinker',
            'Marché local généralement stable'
        ],
        'Acier': [
            'Forte demande pour l\'acier "vert" en Europe',
            'Technologie EAF mature pour recyclage',
            'Possibilité de passer au H2 vert pour DRI',
            'Économies d\'échelle importantes'
        ],
        'Engrais': [
            'Stratégique pour la sécurité alimentaire',
            'Alternatives existent (engrais organiques)',
            'Optimisation possible de l\'usage via précision agricole',
            'Marché captive pour produits locaux'
        ],
        'Hydrogène': [
            'Produit stratégique pour la transition énergétique',
            'Forte demande UE pour H2 vert',
            'Potentiel d\'export vers l\'Europe',
            'Technologies d\'électrolyse en maturité'
        ],
        'Électricité': [
            'Abondance potentielle de renouvelables (solaire, éolien)',
            'Interconnexions possibles avec l\'Europe',
            'Technologies matures et coûts décroissants',
            'Potentiel de stockage (batteries, H2)'
        ]
    }
    
    # Faiblesses par défaut
    faiblesses_sectorielles = {
        'Aluminium': [
            'Dépendance aux importations de bauxite/alumine',
            'Consommation électrique très élevée',
            'Fours à arc électrique vieillissants',
            'Logistique complexe pour matières premières'
        ],
        'Ciment': [
            'Émissions de process inévitables (calcination)',
            'Transport coûteux (produit lourd/volumineux)',
            'Fours rotatifs difficiles à modifier',
            'Alternatives bas-carbone encore chères'
        ],
        'Acier': [
            'Investissements massifs nécessaires (DRI, H2)',
            'Dépendance aux importations de minerai',
            'Cycles de vie longs des équipements',
            'Concurrence intense des producteurs chinois'
        ],
        'Engrais': [
            'Process Haber-Bosch très énergivore',
            'Dépendance aux importations de gaz naturel',
            'Émissions de protoxyde d\'azote (N2O)',
            'Marché très volatile'
        ],
        'Hydrogène': [
            'Coût élevé de l\'électrolyse vs SMR',
            'Besoin en électricité renouvelable massive',
            'Infrastructure de transport limitée',
            'Manque de main-d\'œuvre qualifiée'
        ],
        'Électricité': [
            'Intermittence des renouvelables',
            'Besoin en stockage/batteries coûteux',
            'Réseau électrique à renforcer',
            'Dépendance aux importations de combustibles fossiles'
        ]
    }
    
    # Opportunités
    opportunites = [
        'Marché européen premium pour produits bas-carbone',
        'Financements UE/BEI disponibles pour décarbonation',
        'Différenciation compétitive via certification carbone',
        'Partenariats avec acheteurs européens engagés'
    ]
    
    # Menaces
    menaces = [
        'Taxe CBAM croissante jusqu\'en 2034 (100%)',
        'Concurrence de pays moins régulés',
        'Risque d\'exclusion du marché UE',
        'Volatilité des prix du carbone'
    ]
    
    # Personnalisation selon réponses
    if reponses.get('db_2', 0) > 50:  # >50% local
        forces_sectorielles[secteur].append('Fort taux d\'approvisionnement local déjà atteint')
    else:
        faiblesses_sectorielles[secteur].append('Fortes dépendances aux importations carbonées')
    
    if reponses.get('en_1') == '100% renouvelable':
        forces_sectorielles[secteur].append('Électricité 100% renouvelable déjà en place')
    elif reponses.get('en_1') == 'Réseau national (mix carboné)':
        faiblesses_sectorielles[secteur].append('Mix électrique carboné non optimisé')
    
    if niveau_maturite == 'advanced':
        if secteur in forces_sectorielles:
            forces_sectorielles[secteur].append('Excellente maturité CBAM/ESG')
    elif niveau_maturite == 'beginner':
        if secteur in faiblesses_sectorielles:
            faiblesses_sectorielles[secteur].append('Faible maturité CBAM - risque de non-conformité')
    
    # Sécurité: retourner des valeurs par défaut si le secteur n'existe pas
    forces = forces_sectorielles.get(secteur, [
        'Potentiel d\'optimisation de la production',
        'Opportunités technologiques d\'amélioration',
        'Dynamique de marché favorable pour l\'innovation',
    ])
    faiblesses = faiblesses_sectorielles.get(secteur, [
        'Nécessité d\'investissements en infrastructure',
        'Volatilité des prix des matières premières',
        'Défis réglementaires en évolution',
    ])
    
    return {
        'forces': forces,
        'faiblesses': faiblesses,
        'opportunites': opportunites,
        'menaces': menaces
    }

def afficher_swot(swot_data):
    """Affiche l'analyse SWOT de manière visuelle"""
    
    if not swot_data:
        st.warning("❌ Impossible de générer l'analyse SWOT. Données insuffisantes.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Forces
        forces_html = "<ul>\n" + "\n".join([f"<li>{force}</li>" for force in swot_data.get('forces', [])]) + "\n</ul>"
        st.markdown(f"""
        <div class="swot-box swot-strengths">
            <h3>💪 FORCES (Strengths)</h3>
            {forces_html}
        </div>
        """, unsafe_allow_html=True)
        
        # Opportunités
        opp_html = "<ul>\n" + "\n".join([f"<li>{opp}</li>" for opp in swot_data.get('opportunites', [])]) + "\n</ul>"
        st.markdown(f"""
        <div class="swot-box swot-opportunities">
            <h3>🚀 OPPORTUNITÉS (Opportunities)</h3>
            {opp_html}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Faiblesses
        faib_html = "<ul>\n" + "\n".join([f"<li>{f}</li>" for f in swot_data.get('faiblesses', [])]) + "\n</ul>"
        st.markdown(f"""
        <div class="swot-box swot-weaknesses">
            <h3>⚠️ FAIBLESSES (Weaknesses)</h3>
            {faib_html}
        </div>
        """, unsafe_allow_html=True)
        
        # Menaces
        menaces_html = "<ul>\n" + "\n".join([f"<li>{m}</li>" for m in swot_data.get('menaces', [])]) + "\n</ul>"
        st.markdown(f"""
        <div class="swot-box swot-threats">
            <h3>⛔ MENACES (Threats)</h3>
            {menaces_html}
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# VISUALISATIONS
# ============================================================================

def creer_jauge_ecp(ecp_actuel, benchmark, secteur):
    """Crée une jauge pour l'ECP"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=ecp_actuel,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"ECP {secteur} vs Benchmark CBAM", 'font': {'size': 20}},
        delta={'reference': benchmark, 'increasing': {'color': "red"}},
        gauge={
            'axis': {'range': [None, max(ecp_actuel * 1.2, benchmark * 3)], 'tickwidth': 1},
            'bar': {'color': "#C62828"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, benchmark], 'color': '#E8F5E9'},
                {'range': [benchmark, benchmark*2], 'color': '#FFF3E0'},
                {'range': [benchmark*2, max(ecp_actuel * 1.2, benchmark * 3)], 'color': '#FFEBEE'}
            ],
            'threshold': {
                'line': {'color': "green", 'width': 4},
                'thickness': 0.75,
                'value': benchmark
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig

def creer_waterfall_emissions(data, pct_local, secteur):
    """Waterfall chart des sources d'émissions"""
    
    emissions_importees = data['ecp_typique_importe'] * (1 - pct_local)
    emissions_locales = data['ecp_typique_local'] * pct_local
    
    fig = go.Figure(go.Waterfall(
        name="Émissions",
        orientation="v",
        measure=["relative", "relative", "relative", "relative", "total"],
        x=["MP<br>Importées", "MP<br>Locales", "Process<br>(Scope 1+2)", "Transport", "ECP<br>TOTAL"],
        y=[emissions_importees, emissions_locales, data['emission_process'], 
           data['emission_transport'], 0],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        decreasing={"marker": {"color": "#2E7D32"}},
        increasing={"marker": {"color": "#C62828"}},
        totals={"marker": {"color": "#1F4E78"}}
    ))
    
    fig.add_hline(y=data['benchmark_cbam'], line_dash="dash", line_color="green",
                  annotation_text=f"Benchmark CBAM: {data['benchmark_cbam']:.3f}")
    
    fig.update_layout(
        title=f"Décomposition ECP - {secteur} (tCO2/unité)",
        showlegend=False,
        height=400,
        yaxis_title="tCO2/unité"
    )
    
    return fig

def creer_comparaison_scenarios(scenarios, benchmark, secteur):
    """Graphique de comparaison des scénarios"""
    
    noms = [s['nom'] for s in scenarios]
    couts = [s['cout_annuel']/1e6 for s in scenarios]
    ecp = [s['ecp'] for s in scenarios]
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Coût CBAM Annuel (M EUR)", f"Empreinte Carbone ({secteur})"),
        specs=[[{"type": "bar"}, {"type": "bar"}]]
    )
    
    colors = ['#C62828', '#F57C00', '#FFA726', '#66BB6A', '#2E7D32']
    
    fig.add_trace(
        go.Bar(name="Coût", x=noms, y=couts, marker_color=colors, showlegend=False),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(name="ECP", x=noms, y=ecp, marker_color=colors, showlegend=False),
        row=1, col=2
    )
    
    fig.add_hline(y=benchmark, line_dash="dash", line_color="green", row=1, col=2,
                  annotation_text=f"Benchmark: {benchmark:.3f}")
    
    fig.update_layout(height=400, showlegend=False)
    fig.update_xaxes(tickangle=-45)
    
    return fig

def creer_trajectoire_temporelle(production, ecp_actuel, benchmark, prix_cbam, scenarios):
    """Projections temporelles CBAM"""
    
    annees = [2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034]
    facteurs = [0, 0.025, 0.10, 0.20, 0.35, 0.51, 0.65, 0.80, 0.90, 1.00]
    
    # Calculs pour différents scénarios
    depassement_actuel = max(0, ecp_actuel - benchmark)
    cout_actuel = [depassement_actuel * prix_cbam * production * f / 1e6 for f in facteurs]
    
    # Scénario optimal (dernier scénario)
    scenario_opt = scenarios[-1]
    depassement_opt = max(0, scenario_opt['ecp'] - benchmark)
    cout_opt = [depassement_opt * prix_cbam * production * f / 1e6 for f in facteurs]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=annees, y=cout_actuel,
        mode='lines+markers',
        name='Situation Actuelle',
        line=dict(color='#C62828', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=annees, y=cout_opt,
        mode='lines+markers',
        name='Scénario Optimal',
        line=dict(color='#2E7D32', width=3),
        marker=dict(size=8)
    ))
    
    # Zone d'économie
    fig.add_trace(go.Scatter(
        x=annees + annees[::-1],
        y=cout_actuel + cout_opt[::-1],
        fill='toself',
        fillcolor='rgba(46, 125, 50, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Économies Potentielles',
        showlegend=True
    ))
    
    fig.update_layout(
        title=f"Évolution Coût CBAM 2025-2034 (Prix: {prix_cbam} EUR/tCO2)",
        xaxis_title="Année",
        yaxis_title="Coût CBAM (M EUR/an)",
        hovermode='x unified',
        height=500
    )
    
    return fig

# ============================================================================
# SESSION STATE
# ============================================================================

if 'reponses' not in st.session_state:
    st.session_state.reponses = {}
if 'reponses_maturite' not in st.session_state:
    st.session_state.reponses_maturite = {}
if 'section_active' not in st.session_state:
    st.session_state.section_active = 'MATURITE'
if 'maturite_evaluee' not in st.session_state:
    st.session_state.maturite_evaluee = False
if 'niveau_maturite' not in st.session_state:
    st.session_state.niveau_maturite = 'beginner'
if 'score_maturite' not in st.session_state:
    st.session_state.score_maturite = 0
if 'secteur_selectionne' not in st.session_state:
    st.session_state.secteur_selectionne = 'Aluminium'
if 'benchmark_dynamique' not in st.session_state:
    st.session_state.benchmark_dynamique = 1.479
if 'prix_cbam_dynamique' not in st.session_state:
    st.session_state.prix_cbam_dynamique = 73

# ============================================================================
# INTERFACE PRINCIPALE
# ============================================================================

# Header
st.markdown("""
<div class="main-header">
    <h1>🌍 DASHBOARD CBAM/ESG UNIVERSEL</h1>
    <p style="font-size: 1.2em;">Outil d'Aide à la Décision Stratégique Multi-Secteurs</p>
    <p>Aluminium • Ciment • Acier • Engrais • Hydrogène • Électricité</p>
</div>
""", unsafe_allow_html=True)

# Sélecteur de secteur universel
st.markdown('<div class="sector-selector">', unsafe_allow_html=True)
st.markdown("### 🏭 SÉLECTIONNEZ VOTRE SECTEUR D'ACTIVITÉ")
secteur_choisi = st.selectbox(
    "",
    ['Aluminium', 'Ciment', 'Acier', 'Engrais', 'Hydrogène', 'Électricité'],
    index=['Aluminium', 'Ciment', 'Acier', 'Engrais', 'Hydrogène', 'Électricité'].index(st.session_state.secteur_selectionne),
    key='secteur_global'
)
st.session_state.secteur_selectionne = secteur_choisi
st.markdown('</div>', unsafe_allow_html=True)

# Données sectorielles
donnees_sectors = charger_donnees_sectorielles()
data_sector = donnees_sectors[secteur_choisi]

# Mise à jour automatique du benchmark selon secteur
if st.session_state.benchmark_dynamique != data_sector['benchmark_cbam']:
    st.session_state.benchmark_dynamique = data_sector['benchmark_cbam']

questionnaire = construire_questionnaire_universel()

# Paramètres dynamiques dans le sidebar
with st.sidebar:
    st.markdown("### ⚙️ Paramètres Dynamiques")
    
    st.markdown('<div class="dynamic-input">', unsafe_allow_html=True)
    st.markdown(f"**Benchmark CBAM {secteur_choisi}**")
    benchmark_dynamique = st.number_input(
        "",
        value=st.session_state.benchmark_dynamique,
        min_value=0.1,
        max_value=20.0,
        step=0.001,
        format="%.3f",
        key="input_benchmark"
    )
    st.session_state.benchmark_dynamique = benchmark_dynamique
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="dynamic-input">', unsafe_allow_html=True)
    st.markdown("**Prix CBAM (EUR/tCO2)**")
    prix_cbam_dynamique = st.number_input(
        "",
        value=st.session_state.prix_cbam_dynamique,
        min_value=10,
        max_value=200,
        step=1,
        key="input_prix_cbam"
    )
    st.session_state.prix_cbam_dynamique = prix_cbam_dynamique
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Affichage niveau maturité dans sidebar si évalué
    if st.session_state.maturite_evaluee:
        niveaux_labels = {
            'beginner': '🔴 DÉBUTANT',
            'intermediate': '🟠 INTERMÉDIAIRE',
            'advanced': '🟢 AVANCÉ'
        }
        
        niveaux_colors = {
            'beginner': '#C62828',
            'intermediate': '#F57C00',
            'advanced': '#2E7D32'
        }
        
        niveau = st.session_state.niveau_maturite
        score = st.session_state.score_maturite
        score_pct = score * 20  # Convert from 5-point scale to 100%
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {niveaux_colors[niveau]} 0%, #764ba2 100%); 
                    color: white; padding: 1.5rem; border-radius: 15px; text-align: center; 
                    margin-bottom: 1rem; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
            <p style="margin: 0; font-size: 0.9em; opacity: 0.9;">NIVEAU DE MATURITÉ</p>
            <p style="margin: 0.5rem 0; font-size: 1.8em; font-weight: bold;">
                {niveaux_labels[niveau]}
            </p>
            <p style="margin: 0; font-size: 1.8em; font-weight: bold;">{score:.2f}/5</p>
            <p style="margin: 0.3rem 0; font-size: 1.2em; opacity: 0.95;">({score_pct:.1f}%)</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📊 Navigation")
    
    st.markdown("### 🎯 KPIs Actuels")
    
    # Calculs dynamiques
    production = st.session_state.reponses.get('db_1', 10000)
    
    # Récupérer source d'électricité
    source_electricite = st.session_state.reponses.get('en_1', 'Réseau national (mix carboné)')
    
    # Calcul ECP complet avec énergies
    ecp_calc = calculer_ecp_complet(st.session_state.reponses, data_sector, production, source_electricite)
    
    # Pourcentage de MP locales
    ap_3_data = st.session_state.reponses.get('ap_3', {})
    if isinstance(ap_3_data, dict) and ap_3_data:
        pct_local = ap_3_data.get('pct_local', 40) / 100
    else:
        pct_local = st.session_state.reponses.get('db_2', 40) / 100
    
    depassement = max(0, ecp_calc - st.session_state.benchmark_dynamique)
    cout_calc = depassement * st.session_state.prix_cbam_dynamique * production
    
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-value">{ecp_calc:.2f}</div>
        <div class="kpi-label">ECP (tCO2/unité)</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-value">{(ecp_calc/st.session_state.benchmark_dynamique):.1f}x</div>
        <div class="kpi-label">vs Benchmark</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-value">{cout_calc/1e6:.2f}M</div>
        <div class="kpi-label">EUR Coût/an</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-value">{pct_local*100:.0f}%</div>
        <div class="kpi-label">MP Locales</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### ⏰ Échéances CBAM")
    st.markdown("""
    - **T1 2026:** 1ère déclaration (11 mois)
    - **2027:** Début paiements
    - **2030:** Facteur 51%
    - **2034:** Facteur 100%
    """)
    
    st.markdown("---")
    
    # Progression questionnaire
    total_questions = sum(len(section['questions']) for section in questionnaire.values())
    questions_repondues = len(st.session_state.reponses) + len(st.session_state.reponses_maturite)
    progression = (questions_repondues / total_questions * 100) if total_questions > 0 else 0
    
    st.markdown("### 📈 Progression")
    st.progress(progression / 100)
    st.markdown(f"**{questions_repondues}/{total_questions}** questions ({progression:.0f}%)")

# Tabs principales
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Évaluation Maturité",
    "📋 Questionnaire Détaillé", 
    "📊 Dashboard Analytique",
    "💰 Scénarios + SWOT",
    "📄 Rapport Exécutif"
])

# ============================================================================
# TAB 1: ÉVALUATION MATURITÉ
# ============================================================================

with tab1:
    st.markdown(f"## 🎯 Évaluation de Maturité CBAM/ESG - {secteur_choisi}")
    
    st.markdown("""
    <div class="alert-info">
        <h4>📊 Pourquoi cette évaluation ?</h4>
        <p>Cette évaluation rapide (8 questions) permet de :</p>
        <ul>
            <li>✅ Déterminer votre niveau de préparation CBAM</li>
            <li>✅ Adapter les recommandations à vos capacités réelles</li>
            <li>✅ Prioriser les actions selon votre situation</li>
            <li>✅ Identifier les scénarios réalistes pour vous</li>
        </ul>
        <p><strong>Durée estimée:</strong> 5 minutes</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Questions de maturité
    section_mat = questionnaire['MATURITE']
    
    for question in section_mat['questions']:
        st.markdown(f'<div class="maturity-card">', unsafe_allow_html=True)
        
        # Afficher la question avec icône info si une aide est disponible
        if question.get('aide'):
            st.markdown(afficher_question_avec_info(question['question'], question['aide']), unsafe_allow_html=True)
        else:
            st.markdown(f"### {question['question']}")
        
        if question['type'] == 'radio':
            valeur_actuelle = st.session_state.reponses_maturite.get(question['id'])
            index_actuel = question['options'].index(valeur_actuelle) if valeur_actuelle in question['options'] else 0
            
            reponse = st.radio(
                "",
                question['options'],
                index=index_actuel,
                key=f"mat_{question['id']}"
            )
            st.session_state.reponses_maturite[question['id']] = reponse
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Bouton évaluation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 ÉVALUER MA MATURITÉ", use_container_width=True, type="primary"):
            if len(st.session_state.reponses_maturite) >= len(section_mat['questions']):
                niveau, score, details = calculer_niveau_maturite(st.session_state.reponses_maturite)
                st.session_state.niveau_maturite = niveau
                st.session_state.score_maturite = score
                st.session_state.maturite_evaluee = True
                st.rerun()
            else:
                st.warning("⚠️ Veuillez répondre à toutes les questions d'évaluation")
    
    # Affichage résultat si évalué
    if st.session_state.maturite_evaluee:
        st.markdown("---")
        st.markdown("## 📊 Votre Profil de Maturité")
        
        niveau, score, details = calculer_niveau_maturite(st.session_state.reponses_maturite)
        afficher_resultat_maturite(niveau, score, details)
        
        st.markdown("---")
        st.markdown("""
        <div class="alert-success">
            <h4>✅ Évaluation Complétée</h4>
            <p>Vous pouvez maintenant passer aux autres sections. Les recommandations et scénarios 
            seront adaptés à votre niveau de maturité.</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# TAB 2: QUESTIONNAIRE DÉTAILLÉ
# ============================================================================

with tab2:
    st.markdown(f"## 📋 Questionnaire Détaillé CBAM/ESG - {secteur_choisi}")
    
    if not st.session_state.maturite_evaluee:
        st.warning("""
        ⚠️ **Évaluation de maturité recommandée**
        
        Pour des recommandations personnalisées, complétez d'abord l'évaluation de maturité dans l'onglet précédent.
        
        Vous pouvez néanmoins continuer le questionnaire détaillé.
        """)
    
    # Sélection section avec grille horizontale (pas de scroll)
    sections_detaillees = {k: v for k, v in questionnaire.items() if k != 'MATURITE'}
    section_names = list(sections_detaillees.keys())
    section_labels = [sections_detaillees[k]['titre'] for k in section_names]
    
    st.markdown("### 📋 Sélectionnez une section:")
    
    # Grille de sélection horizontale
    cols = st.columns(len(section_names))
    selected_section = st.session_state.section_active
    
    for idx, (col, sec_key) in enumerate(zip(cols, section_names)):
        with col:
            sec_title = sections_detaillees[sec_key]['titre']
            is_active = selected_section == sec_key
            
            if st.button(
                sec_title,
                key=f"btn_{sec_key}",
                use_container_width=True,
            ):
                st.session_state.section_active = sec_key
                selected_section = sec_key
                st.rerun()
    
    st.session_state.section_active = selected_section
    section = sections_detaillees[selected_section]
    
    st.markdown(f"""
    <div style="background: {section['color']}; color: white; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
        <h2>{section['titre']}</h2>
        {f"<p>{section.get('description', '')}</p>" if 'description' in section else ''}
    </div>
    """, unsafe_allow_html=True)
    
    # Reorganize questions by scopes
    questions_by_scope = organiser_questions_par_scope(section)
    
    # Display questions organized by scopes
    for scope_name, scope_data in questions_by_scope.items():
        st.markdown(f"""
        <div class="scope-container">
            <div class="scope-header">
                {scope_data['emoji']} {scope_name}
                <span class="scope-badge">{len(scope_data['questions'])} questions</span>
            </div>
            <p style="color: #666; margin: 0.5rem 0;">{scope_data['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        for question in scope_data['questions']:
            st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
            
            # Afficher avec icône info si aide disponible
            if question.get('aide'):
                st.markdown(afficher_question_avec_info(question['question'], question['aide']), unsafe_allow_html=True)
            else:
                st.markdown(f"### {question['question']}")
            
            if question['type'] == 'radio':
                valeur_actuelle = st.session_state.reponses.get(question['id'])
                index_actuel = question['options'].index(valeur_actuelle) if valeur_actuelle in question['options'] else 0
                
                reponse = st.radio(
                    "",
                    question['options'],
                    index=index_actuel,
                    key=f"q_{question['id']}"
                )
                st.session_state.reponses[question['id']] = reponse
                
            elif question['type'] == 'multiselect':
                reponse = st.multiselect(
                    "",
                    question['options'],
                    default=st.session_state.reponses.get(question['id'], []),
                    key=f"q_{question['id']}"
                )
                st.session_state.reponses[question['id']] = reponse
                
            elif question['type'] == 'slider':
                reponse = st.slider(
                    "",
                    min_value=question['min'],
                    max_value=question['max'],
                    value=st.session_state.reponses.get(question['id'], question['valeur_defaut']),
                    key=f"q_{question['id']}"
                )
                st.session_state.reponses[question['id']] = reponse
                
            elif question['type'] == 'number':
                try:
                    valeur_actuelle = st.session_state.reponses.get(question['id'], question['valeur_defaut'])
                    # Convertir en float si ce n'est pas déjà un nombre
                    if isinstance(valeur_actuelle, str):
                        valeur_actuelle = float(valeur_actuelle)
                    
                    reponse = st.number_input(
                        "",
                        min_value=float(question['min']),
                        max_value=float(question['max']),
                        value=float(valeur_actuelle),
                        step=1.0,
                        key=f"q_{question['id']}"
                    )
                    st.session_state.reponses[question['id']] = float(reponse)
                except (ValueError, TypeError) as e:
                    st.error(f"❌ Erreur dans le champ '{question['question']}': {str(e)}")
                    st.session_state.reponses[question['id']] = float(question['valeur_defaut'])
            
            elif question['type'] == 'calculated':
                # Handle calculated fields
                try:
                    # Get dependency values
                    ad = float(st.session_state.reponses.get('cbam_ad', 2394000))
                    ncv = float(st.session_state.reponses.get('cbam_ncv', 1))
                    ef = float(st.session_state.reponses.get('cbam_ef', 1.9))
                    oxf = float(st.session_state.reponses.get('cbam_oxf', 100))
                    bioc = float(st.session_state.reponses.get('cbam_bioc', 0))
                    
                    # Calculate the value using the formula
                    calculated_value = ad * ncv * ef * (oxf / 100) * (1 - bioc / 100)
                    
                    # Update session state
                    st.session_state.reponses[question['id']] = calculated_value
                    
                    # Display as readonly metric with formula breakdown
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.metric(
                            "Résultat du calcul",
                            f"{calculated_value:,.0f} tCO2",
                            delta="Formule: AD × NCV × EF × OxF × (1-BioC)"
                        )
                    
                    with col2:
                        st.info(f"""
                        **Composition:**
                        - AD: {ad:,.0f}
                        - NCV: {ncv:.2f}
                        - EF: {ef:.2f}
                        - OxF: {oxf:.0f}%
                        - BioC: {bioc:.0f}%
                        """)
                    
                except (ValueError, TypeError) as e:
                    st.error(f"❌ Erreur de calcul: {str(e)}")
                    st.session_state.reponses[question['id']] = float(question['valeur_defaut'])
            
            elif question['type'] == 'compound':
                # Handle MP locales avec ECP
                st.markdown("#### Matières Premières Locales & Bas-Carbone")
                
                if question['id'] not in st.session_state.reponses:
                    st.session_state.reponses[question['id']] = {}
                
                comp_data = st.session_state.reponses[question['id']]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    pct_local = st.slider(
                        "% Matières Premières Locales",
                        min_value=0,
                        max_value=100,
                        value=comp_data.get('pct_local', 38),
                        step=1,
                        help="Entrez le pourcentage de MP locales. Les autres fournisseurs complèteront à 100%",
                        key=f"{question['id']}_pct"
                    )
                    comp_data['pct_local'] = pct_local
                
                with col2:
                    ecp_local = st.number_input(
                        "ECP des MP Locales (tCO2/t)",
                        min_value=0.0,
                        max_value=20.0,
                        value=comp_data.get('ecp_local', 1.5),
                        step=0.1,
                        help="Empreinte carbone spécifique des matières premières locales",
                        key=f"{question['id']}_ecp"
                    )
                    comp_data['ecp_local'] = ecp_local
                
                st.info(f"📊 Vous avez **{pct_local}%** de MP locales avec ECP={ecp_local} tCO2/t")
                st.info(f"📊 **{100-pct_local}%** sera complété par les fournisseurs autres (voir section ci-dessous)")
            
            elif question['type'] == 'suppliers':
                # Initialize suppliers data if not present
                if question['id'] not in st.session_state.reponses:
                    st.session_state.reponses[question['id']] = question.get('suppliers', [])
                
                suppliers_data = st.session_state.reponses[question['id']]
                
                # Get MP locales data to calculate remaining percentage
                ap_3_data = st.session_state.reponses.get('ap_3', {})
                pct_local_mp = ap_3_data.get('pct_local', 38) if isinstance(ap_3_data, dict) else 38
                pct_remaining = 100 - pct_local_mp
                
                st.markdown(f"#### Fournisseurs (Pour {pct_remaining}% restant)")
                st.info(f"📊 MP Locales occupent {pct_local_mp}%. Les fournisseurs ci-dessous complètent les {pct_remaining}%")
                
                # Create columns for supplier data
                st.markdown("**Détails des fournisseurs:**")
                
                col_header1, col_header2, col_header3, col_header4 = st.columns([2, 1, 1, 1])
                col_header1.markdown("**Nom**")
                col_header2.markdown("**Proportion (%)**")
                col_header3.markdown("**ECP (tCO2/t)**")
                col_header4.markdown("**Actions**")
                
                for i, supplier in enumerate(suppliers_data):
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    
                    with col1:
                        supplier['nom'] = st.text_input(
                            "Nom du fournisseur",
                            value=supplier.get('nom', f'Fournisseur {i+1}'),
                            key=f"{question['id']}_nom_{i}",
                            label_visibility="collapsed"
                        )
                    
                    with col2:
                        supplier['proportion'] = st.number_input(
                            "Proportion (%)",
                            min_value=0.0,
                            max_value=100.0,
                            value=float(supplier.get('proportion', 0.0)),
                            step=1.0,
                            key=f"{question['id']}_prop_{i}",
                            label_visibility="collapsed"
                        )
                    
                    with col3:
                        supplier['ecp'] = st.number_input(
                            "ECP (tCO2/t)",
                            min_value=0.0,
                            max_value=50.0,
                            value=float(supplier.get('ecp', 0.0)),
                            step=0.1,
                            key=f"{question['id']}_ecp_{i}",
                            label_visibility="collapsed"
                        )
                    
                    with col4:
                        if st.button("❌ Supprimer", key=f"{question['id']}_del_{i}", use_container_width=True):
                            suppliers_data.pop(i)
                            st.rerun()
                
                # Add new supplier button
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    if st.button("➕ Ajouter un fournisseur", use_container_width=True):
                        suppliers_data.append({
                            'nom': f'Fournisseur {len(suppliers_data) + 1}',
                            'proportion': 0.0,
                            'ecp': 2.5
                        })
                        st.rerun()
                
                # Validation message
                total_prop = sum(float(s.get('proportion', 0)) for s in suppliers_data)
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Proportions Fournisseurs", f"{total_prop:.0f}%", f"Cible: {pct_remaining:.0f}%")
                with col2:
                    if abs(total_prop - pct_remaining) < 0.1:
                        st.success(f"✅ Les proportions totalisent bien {pct_remaining}%")
                    elif total_prop > 0:
                        st.warning(f"⚠️ Total = {total_prop:.0f}% | Cible = {pct_remaining:.0f}%")
                    else:
                        st.info("📝 Veuillez entrer les détails des fournisseurs")
                
                st.session_state.reponses[question['id']] = suppliers_data
                
                # Calculate weighted ECP
                total_proportion = sum(float(s.get('proportion', 0)) for s in suppliers_data)
                if total_proportion > 0:
                    weighted_ecp = sum(
                        float(s.get('ecp', 0)) * float(s.get('proportion', 0)) / total_proportion 
                        for s in suppliers_data
                    )
                else:
                    weighted_ecp = 0
                
                # Display weighted ECP result
                st.markdown("---")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("ECP Pondéré", f"{weighted_ecp:.2f} tCO2/t", 
                             delta=f"Somme proportions: {total_proportion:.0f}%")
                with col2:
                    st.info(f"**Formule:** ECP_pondéré = Σ(ECP × Proportion%) / 100")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation sections
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    current_index = section_names.index(selected_section)
    
    with col1:
        if current_index > 0:
            if st.button("⬅️ Section Précédente", use_container_width=True):
                st.session_state.section_active = section_names[current_index - 1]
                st.rerun()
    
    with col3:
        if current_index < len(section_names) - 1:
            if st.button("Section Suivante ➡️", use_container_width=True):
                st.session_state.section_active = section_names[current_index + 1]
                st.rerun()

# ============================================================================
# TAB 3: DASHBOARD ANALYTIQUE
# ============================================================================

with tab3:
    st.markdown(f"## ��� Dashboard Analytique - {secteur_choisi}")
    
    # KPIs principaux - Nouvelle organisation
    st.markdown("### 🎯 Indicateurs Clés de Performance")
    
    # Calcul ECP pondéré global
    ap_3_data = st.session_state.reponses.get('ap_3', {})
    if isinstance(ap_3_data, dict) and ap_3_data:
        pct_local_mp = ap_3_data.get('pct_local', 38) / 100
        ecp_local_mp = ap_3_data.get('ecp_local', 1.5)
    else:
        pct_local_mp = pct_local
        ecp_local_mp = 1.5
    
    suppliers = st.session_state.reponses.get('ap_4', [])
    ecp_pondere_global = ecp_local_mp * pct_local_mp
    
    if suppliers:
        total_prop_suppliers = sum(float(s.get('proportion', 0)) for s in suppliers)
        if total_prop_suppliers > 0:
            for supplier in suppliers:
                prop = float(supplier.get('proportion', 0)) / 100
                ecp_supplier = float(supplier.get('ecp', 0))
                ecp_pondere_global += ecp_supplier * prop
    
    # Ligne 1 - Comparaison Benchmark vs ECP Pondéré (À GAUCHE)
    col1, col2 = st.columns([1.5, 1.5])
    
    with col1:
        st.markdown("#### 📊 Benchmark CBAM vs ECP Pondéré")
        
        # Création graphique de comparaison
        fig_bench_compare = go.Figure()
        
        fig_bench_compare.add_trace(go.Bar(
            name='Benchmark CBAM',
            x=['Seuil'],
            y=[st.session_state.benchmark_dynamique],
            marker_color='#4CAF50',
            text=[f"{st.session_state.benchmark_dynamique:.2f}"],
            textposition='auto'
        ))
        
        fig_bench_compare.add_trace(go.Bar(
            name='ECP Pondéré (Actuel)',
            x=['Votre Production'],
            y=[ecp_pondere_global],
            marker_color='#FF9800' if ecp_pondere_global > st.session_state.benchmark_dynamique else '#2196F3',
            text=[f"{ecp_pondere_global:.2f}"],
            textposition='auto'
        ))
        
        fig_bench_compare.update_layout(
            title="Comparaison Benchmark vs ECP Pondéré",
            yaxis_title="ECP (tCO2/t)",
            barmode='group',
            height=350,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_bench_compare, use_container_width=True)
        
        # Analyse
        écart = ecp_pondere_global - st.session_state.benchmark_dynamique
        écart_pct = (écart / st.session_state.benchmark_dynamique * 100) if st.session_state.benchmark_dynamique > 0 else 0
        
        if écart <= 0:
            st.success(f"✅ Vous êtes CONFORME: ECP {écart_pct:.1f}% en-dessous du benchmark")
        else:
            st.error(f"❌ Non conforme: ECP {écart_pct:.1f}% au-dessus du benchmark")
    
    with col2:
        st.markdown("#### 📈 KPIs Globaux")
        
        col_kpi1, col_kpi2 = st.columns(2)
        
        with col_kpi1:
            st.metric(
                "Benchmark CBAM",
                f"{st.session_state.benchmark_dynamique:.2f} tCO2/t",
                help="Seuil réglementaire"
            )
            
            st.metric(
                "Production Annuelle",
                f"{production:,.0f} {data_sector['unite_production']}/an"
            )
        
        with col_kpi2:
            st.metric(
                "ECP Pondéré",
                f"{ecp_pondere_global:.2f} tCO2/t",
                delta=f"{écart:.2f}",
                delta_color="inverse"
            )
            
            st.metric(
                "Coût CBAM 2027",
                f"{cout_calc/1e6:.2f}M EUR/an"
            )
    
    st.markdown("---")
    
    # Ligne 2 - Détails fournisseurs et autres métriques
    col3, col4, col5, col6 = st.columns(4)
    
    with col3:
        st.metric(
            "ECP Pondéré (Total)",
            f"{ecp_pondere_global:.2f} tCO2/t",
            delta=f"{écart:.2f} vs Benchmark",
            delta_color="inverse",
            help="ECP pondéré = (ECP_local × %_local) + Σ(ECP_fournisseur × %_fournisseur)"
        )
    
    with col4:
        st.metric(
            "MP Locales %",
            f"{pct_local_mp*100:.0f}%",
            help="Pourcentage de matières premières locales"
        )
    
    with col5:
        st.metric(
            "ECP MP Locales",
            f"{ecp_local_mp:.2f} tCO2/t",
            help="Empreinte carbone des matières premières locales"
        )
    
    with col6:
        # Nombre de fournisseurs
        num_suppliers = len(suppliers) if suppliers else 0
        st.metric(
            "Fournisseurs",
            f"{num_suppliers}",
            help=f"{num_suppliers} fournisseur(s) + MP locales"
        )
    
    st.markdown("---")
    
    # Visualisations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Empreinte Carbone")
        fig_jauge = creer_jauge_ecp(ecp_calc, st.session_state.benchmark_dynamique, secteur_choisi)
        st.plotly_chart(fig_jauge, use_container_width=True)
        
        if ecp_calc > st.session_state.benchmark_dynamique:
            depassement_pct = ((ecp_calc / st.session_state.benchmark_dynamique) - 1) * 100
            st.markdown(f"""
            <div class="alert-critical">
                <h4>❌ DÉPASSEMENT CRITIQUE</h4>
                <p>Vous dépassez le benchmark de <strong>{depassement_pct:.0f}%</strong></p>
                <p>Coût additionnel: <strong>{cout_calc/1e6:.2f}M EUR/an</strong></p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Sources d'Émissions")
        fig_waterfall = creer_waterfall_emissions(data_sector, pct_local, secteur_choisi)
        st.plotly_chart(fig_waterfall, use_container_width=True)
        
        contrib_importees = (data_sector['ecp_typique_importe'] * (1 - pct_local)) / ecp_calc * 100
        st.markdown(f"""
        <div class="alert-warning">
            <h4>🚨 POINT CRITIQUE</h4>
            <p>Les matières premières importées représentent <strong>{contrib_importees:.0f}%</strong> de vos émissions totales!</p>
            <p>Réduction prioritaire: ↑ Approvisionnement local ({pct_local*100:.0f}% → 70%+)</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Décomposition détaillée de l'ECP
    st.markdown("---")
    st.markdown("### 🔍 Décomposition Détaillée de l'ECP")
    
    # Calcul des contributions
    ap_3_data = st.session_state.reponses.get('ap_3', {})
    if isinstance(ap_3_data, dict) and ap_3_data:
        pct_local_mp = ap_3_data.get('pct_local', 38) / 100
        ecp_local_mp = ap_3_data.get('ecp_local', 1.5)
    else:
        pct_local_mp = pct_local
        ecp_local_mp = 1.5
    
    # Contributions MP
    contrib_mp_locale = ecp_local_mp * pct_local_mp
    contrib_mp_importees = data_sector['ecp_typique_importe'] * (1 - pct_local_mp)
    contrib_process = data_sector['emission_process']
    
    # Contributions énergétiques
    consommation_electricite = st.session_state.reponses.get('en_5', 50000)
    consommation_gaz = st.session_state.reponses.get('en_6', 30000)
    source_electricite = st.session_state.reponses.get('en_1', 'Réseau national (mix carboné)')
    production = st.session_state.reponses.get('db_1', 10000)
    
    if source_electricite == '100% renouvelable':
        facteur_emission_electricite = 0.0
    elif source_electricite == 'Partiellement renouvelable':
        facteur_emission_electricite = 0.2
    elif source_electricite == 'Autoproduction':
        facteur_emission_electricite = 0.15
    else:
        facteur_emission_electricite = 0.4
    
    facteur_emission_gaz = 0.2
    emissions_electricite_annuelles = consommation_electricite * facteur_emission_electricite
    emissions_gaz_annuelles = consommation_gaz * facteur_emission_gaz
    contrib_energie = (emissions_electricite_annuelles + emissions_gaz_annuelles) / production if production > 0 else 0
    
    # Affichage en colonnes
    col_ecp1, col_ecp2 = st.columns(2)
    
    with col_ecp1:
        st.markdown("#### 📊 Contributions par Source")
        
        # Préparation des données pour le graphique
        sources = ['MP Locales', 'MP Importées', 'Process', 'Électricité', 'Gaz']
        contributions = [
            max(0, contrib_mp_locale),
            max(0, contrib_mp_importees),
            max(0, contrib_process),
            emissions_electricite_annuelles / production if production > 0 else 0,
            emissions_gaz_annuelles / production if production > 0 else 0
        ]
        
        fig_decomp = go.Figure(data=[
            go.Bar(
                x=sources,
                y=contributions,
                text=[f"{c:.3f}" for c in contributions],
                textposition='auto',
                marker=dict(
                    color=contributions,
                    colorscale='RdYlGn_r',
                    showscale=False
                )
            )
        ])
        
        fig_decomp.update_layout(
            title="Contribution à l'ECP par Source",
            yaxis_title="ECP (tCO2/unité)",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_decomp, use_container_width=True)
    
    with col_ecp2:
        st.markdown("#### 📋 Détails des Contributions")
        
        # Tableau détaillé
        total_contributions = sum(contributions)
        ecp_details = {
            'Source': sources,
            'Contribution (tCO2/u)': [f"{c:.3f}" for c in contributions],
            '% de l\'ECP Total': [f"{(c/total_contributions*100):.1f}%" if total_contributions > 0 else "0%" for c in contributions]
        }
        
        df_details = pd.DataFrame(ecp_details)
        st.dataframe(df_details, use_container_width=True)
        
        st.markdown(f"""
        <div style="background: #E3F2FD; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
            <p><strong>📌 Résumé:</strong></p>
            <ul>
                <li>ECP Total: <strong>{ecp_calc:.3f}</strong> tCO2/{data_sector['unite_production'].split()[0]}</li>
                <li>Benchmark CBAM: <strong>{st.session_state.benchmark_dynamique:.3f}</strong></li>
                <li>⚡ Électricité: <strong>{source_electricite}</strong></li>
                <li>🔥 Consommation: {consommation_electricite:.0f} MWh électricité + {consommation_gaz:.0f} MWh gaz/an</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Comparaison Benchmark vs ECP Pondéré par Fournisseur (DÉTAIL)
    st.markdown("---")
    st.markdown("### 📊 Détail: ECP par Fournisseur vs Benchmark CBAM")
    
    if 'ap_4' in st.session_state.reponses and st.session_state.reponses['ap_4']:
        suppliers = st.session_state.reponses['ap_4']
        
        # Calcul ECP pondéré incluant MP Locales et Fournisseurs
        # Récupérer données MP Locales
        ap_3_data = st.session_state.reponses.get('ap_3', {})
        if isinstance(ap_3_data, dict) and ap_3_data:
            pct_local = float(ap_3_data.get('pct_local', 38)) / 100
            ecp_local = float(ap_3_data.get('ecp_local', 1.5))
        else:
            pct_local = 0.38
            ecp_local = 1.5
        
        total_prop = sum(float(s.get('proportion', 0)) for s in suppliers)
        
        if total_prop > 0:
            # Créer données pour visualisation
            supplier_names = ['MP Locales']
            supplier_ecps = [ecp_local]
            supplier_props = [pct_local * 100]
            
            for supplier in suppliers:
                supplier_names.append(supplier.get('nom', 'Fournisseur'))
                supplier_ecps.append(float(supplier.get('ecp', 0)))
                supplier_props.append(float(supplier.get('proportion', 0)))
            
            # Calcul avec MP Locales
            weighted_ecp = ecp_local * pct_local
            weighted_ecp += sum(float(s.get('ecp', 0)) * float(s.get('proportion', 0)) / 100 for s in suppliers)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📈 ECP par Fournisseur")
                fig_suppliers = go.Figure()
                
                fig_suppliers.add_trace(go.Bar(
                    x=supplier_names,
                    y=supplier_ecps,
                    name='ECP (tCO2/t)',
                    marker_color='#FF9800',
                    text=[f"{ecp:.2f}" for ecp in supplier_ecps],
                    textposition='auto'
                ))
                
                fig_suppliers.add_hline(
                    y=st.session_state.benchmark_dynamique,
                    line_dash="dash",
                    line_color="green",
                    annotation_text="Benchmark CBAM",
                    annotation_position="right"
                )
                
                fig_suppliers.add_hline(
                    y=weighted_ecp,
                    line_dash="solid",
                    line_color="red",
                    annotation_text=f"ECP Pondéré: {weighted_ecp:.2f}",
                    annotation_position="right"
                )
                
                fig_suppliers.update_layout(
                    title="ECP des Fournisseurs vs Benchmark CBAM",
                    xaxis_title="Fournisseur",
                    yaxis_title="ECP (tCO2/t)",
                    hovermode="x unified",
                    height=400
                )
                
                st.plotly_chart(fig_suppliers, use_container_width=True)
            
            with col2:
                st.markdown("#### 📊 Proportion des Fournisseurs")
                fig_pie = go.Figure(data=[go.Pie(
                    labels=supplier_names,
                    values=supplier_props,
                    textposition='inside',
                    textinfo='label+percent'
                )])
                
                fig_pie.update_layout(
                    title="Part de chaque Fournisseur",
                    height=400
                )
                
                st.plotly_chart(fig_pie, use_container_width=True)
            
            # Résumé comparatif
            st.markdown("---")
            st.markdown("#### 🎯 Analyse Comparative")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Benchmark CBAM",
                    f"{st.session_state.benchmark_dynamique:.2f} tCO2/t",
                    help="Seuil réglementaire"
                )
            
            with col2:
                st.metric(
                    "ECP Pondéré",
                    f"{weighted_ecp:.2f} tCO2/t",
                    delta=f"{weighted_ecp - st.session_state.benchmark_dynamique:.2f}",
                    delta_color="inverse"
                )
            
            with col3:
                écart_pct = ((weighted_ecp - st.session_state.benchmark_dynamique) / st.session_state.benchmark_dynamique * 100) if st.session_state.benchmark_dynamique > 0 else 0
                st.metric(
                    "Écart Relatif",
                    f"{écart_pct:.1f}%",
                    help="Écart ECP pondéré par rapport au benchmark"
                )
            
            # Détail par fournisseur
            st.markdown("---")
            st.markdown("#### 📋 Détail par Fournisseur")
            
            df_suppliers = pd.DataFrame({
                'Fournisseur': supplier_names,
                'Proportion (%)': [f"{p:.1f}%" for p in supplier_props],
                'ECP (tCO2/t)': [f"{ecp:.2f}" for ecp in supplier_ecps],
                'vs Benchmark': [f"{((ecp / st.session_state.benchmark_dynamique - 1) * 100):.1f}%" if ecp else "N/A" for ecp in supplier_ecps],
                'Contribution pondérée': [f"{(ecp * p / total_prop):.2f}" for ecp, p in zip(supplier_ecps, supplier_props)]
            })
            
            st.dataframe(df_suppliers, use_container_width=True)
        else:
            st.info("⚠️ Veuillez définir au moins un fournisseur avec une proportion > 0%")
    else:
        st.info("💡 Complétez la section 'Approvisionnement' avec vos fournisseurs pour voir cette analyse détaillée")
    
    # ====================================================================
    # SECTION CBAM - CALCULS DÉTAILLÉS
    # ====================================================================
    st.markdown("---")
    st.markdown("### 📊 CBAM - Calculs Détaillés des Émissions & SEE")
    
    # Vérifier si des données CBAM sont présentes
    if any(k.startswith('cbam_') for k in st.session_state.reponses.keys()):
        # Calculer tous les SEE CBAM
        cbam_results = calculer_cbam_complet(st.session_state.reponses)
        
        # Tabs pour les différents calculs CBAM
        cbam_tab1, cbam_tab2, cbam_tab3 = st.tabs([
            "📊 SEE - Calculs Principaux",
            "🔧 Détails Formules",
            "💰 Prix Carbone"
        ])
        
        with cbam_tab1:
            st.markdown("#### 🎯 Scope Emissions Embedded (SEE) - Vue d'Ensemble")
            
            # KPIs principaux
            kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
            
            with kpi_col1:
                st.metric(
                    "SEE Direct",
                    f"{cbam_results.get('see_direct_tco2_par_t', 0):.3f}",
                    help="Émissions directes / Production (tCO2/t)"
                )
            
            with kpi_col2:
                st.metric(
                    "SEE Indirect",
                    f"{cbam_results.get('see_indirect_tco2_par_t', 0):.3f}",
                    help="Électricité consommée × Facteur émission (tCO2/t)"
                )
            
            with kpi_col3:
                st.metric(
                    "SEE Total",
                    f"{cbam_results.get('see_total_tco2_par_t', 0):.3f}",
                    help="SEE Direct + SEE Indirect (tCO2/t)"
                )
            
            st.markdown("---")
            
            # Graphique comparatif SEE
            see_components = {
                'SEE Direct': cbam_results.get('see_direct_tco2_par_t', 0),
                'SEE Indirect': cbam_results.get('see_indirect_tco2_par_t', 0)
            }
            
            fig_see = go.Figure(data=[
                go.Bar(
                    x=list(see_components.keys()),
                    y=list(see_components.values()),
                    text=[f"{v:.3f}" for v in see_components.values()],
                    textposition='auto',
                    marker=dict(
                        color=['#FF6B6B', '#4ECDC4'],
                    )
                )
            ])
            
            fig_see.update_layout(
                title="Décomposition SEE par Composante",
                yaxis_title="SEE (tCO2/t)",
                height=400,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_see, use_container_width=True)
            
            # Résumé textuel
            st.markdown(f"""
            <div class="alert-info">
                <h4>📋 Résumé SEE Complet</h4>
                <ul>
                    <li><strong>SEE Direct:</strong> {cbam_results.get('see_direct_tco2_par_t', 0):.3f} tCO2/t 
                        (Combustion: {cbam_results.get('emissions_directes_combustion_tco2', 0):.0f} tCO2 total)</li>
                    <li><strong>SEE Indirect:</strong> {cbam_results.get('see_indirect_tco2_par_t', 0):.3f} tCO2/t 
                        ({cbam_results.get('_details', {}).get('electricite_mwh_t', 0):.3f} MWh/t × {cbam_results.get('_details', {}).get('ef_electricite_tco2_mwh', 0):.1f} tCO2/MWh)</li>
                    <li><strong>SEE Total (avant précurseurs):</strong> {cbam_results.get('see_total_tco2_par_t', 0):.3f} tCO2/t</li>
                    <li><strong>SEE Total (avec précurseurs):</strong> {cbam_results.get('see_total_tco2_par_t', 0):.3f} tCO2/t</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with cbam_tab2:
            st.markdown("#### 🔧 Détails des Calculs - Chaque Formule")
            
            details = cbam_results.get('_details', {})
            
            # 1. Émissions directes combustion
            st.markdown("##### 1️⃣ Émissions Directes (Combustion)")
            st.markdown("**Formule:** AD × NCV × EF × OxF × (1 - BioC)")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.write(f"**AD:** {details.get('ad', 0):,.0f}")
            with col2:
                st.write(f"**NCV:** {details.get('ncv', 0):.3f}")
            with col3:
                st.write(f"**EF:** {details.get('ef', 0):.1f}")
            with col4:
                st.write(f"**OxF:** {details.get('oxf_pct', 0):.0f}%")
            with col5:
                st.write(f"**BioC:** {details.get('bioc_pct', 0):.0f}%")
            
            emissions_directes = cbam_results.get('emissions_directes_combustion_tco2', 0)
            st.info(f"**Résultat:** {emissions_directes:,.0f} tCO2")
            
            st.markdown("---")
            
            # 2. SEE Direct
            st.markdown("##### 2️⃣ SEE Direct (Émissions Attribuées / Production)")
            st.markdown("**Formule:** Émissions Process / Production Totale")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Émissions Process:** {details.get('emissions_process_tco2', 0):,.0f} tCO2")
            with col2:
                st.write(f"**Production Totale:** {details.get('production_totale_t', 0):,.0f} t")
            
            see_direct_val = cbam_results.get('see_direct_tco2_par_t', 0)
            st.success(f"**SEE Direct:** {see_direct_val:.4f} tCO2/t")
            
            st.markdown("---")
            
            # 3. SEE Indirect
            st.markdown("##### 3️⃣ SEE Indirect (Électricité)")
            st.markdown("**Formule:** Électricité (MWh/t) × Facteur d'Émission (tCO2/MWh)")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Électricité:** {details.get('electricite_mwh_t', 0):.4f} MWh/t")
            with col2:
                st.write(f"**Facteur EF:** {details.get('ef_electricite_tco2_mwh', 0):.3f} tCO2/MWh")
            
            see_indirect_val = cbam_results.get('see_indirect_tco2_par_t', 0)
            st.success(f"**SEE Indirect:** {see_indirect_val:.4f} tCO2/t")
        
        with cbam_tab3:
            st.markdown("#### 💰 Prix Carbone & Coûts")
            
            details = cbam_results.get('_details', {})
            
            # Paramètres
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Carbon Price:** {details.get('carbon_price_eur_tco2', 0):.0f} EUR/tCO2")
            with col2:
                st.write(f"**% Couvert:** {details.get('pct_emissions_couvertes', 0):.0f}%")
            with col3:
                st.write(f"**Rabais:** {details.get('rebate_eur', 0):,.0f} EUR")
            
            st.markdown("---")
            
            # Formule et résultat
            st.markdown("**Formule:** CP_effectif = SEE_couvert × Carbon_Price - Rabais")
            
            see_couvert = cbam_results.get('see_couvert_tco2_par_t', 0)
            cp_effectif_total = cbam_results.get('carbon_price_effectif_total_eur', 0)
            cp_effectif_par_t = cbam_results.get('carbon_price_effectif_eur_par_t', 0)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("SEE Couvert (tCO2/t)", f"{see_couvert:.4f}")
            with col2:
                st.metric("Coût Effectif (EUR/t)", f"{cp_effectif_par_t:.2f}")
            
            st.warning(f"**Coût Total Annuel:** {cp_effectif_total:,.0f} EUR")
    else:
        st.info("💡 Complétez la section 'Énergie & Process' pour voir les calculs SEE détaillés")
    
    # Recommandations adaptées selon maturité
    st.markdown("---")
    st.markdown("### 🎯 Recommandations Prioritaires")
    
    if st.session_state.maturite_evaluee:
        niveau = st.session_state.niveau_maturite
        
        if niveau == 'beginner':
            st.markdown(f"""
            <div class="alert-warning">
                <h4>🔴 Actions Prioritaires - Niveau Débutant ({secteur_choisi})</h4>
                <ol>
                    <li><strong>URGENT:</strong> Formation direction sur CBAM (délai: 1 mois)</li>
                    <li><strong>URGENT:</strong> Audit empreinte carbone certifié (délai: 2-3 mois)</li>
                    <li><strong>COURT TERME:</strong> Désigner responsable CBAM (délai: 1 mois)</li>
                    <li><strong>MOYEN TERME:</strong> Identifier fournisseurs bas-carbone locaux (délai: 3-6 mois)</li>
                    <li><strong>MOYEN TERME:</strong> Mettre en place traçabilité basique (délai: 4-6 mois)</li>
                </ol>
                <p><strong>Objectif 12 mois:</strong> Préparer 1ère déclaration CBAM + réduire coût de 30%</p>
            </div>
            """, unsafe_allow_html=True)
            
        elif niveau == 'intermediate':
            st.markdown(f"""
            <div class="alert-info">
                <h4>🟠 Actions Prioritaires - Niveau Intermédiaire ({secteur_choisi})</h4>
                <ol>
                    <li><strong>URGENT:</strong> Finaliser certification ISO 14064 (délai: 2-3 mois)</li>
                    <li><strong>COURT TERME:</strong> Sécuriser contrats fournisseurs bas-carbone 70% (délai: 3-4 mois)</li>
                    <li><strong>COURT TERME:</strong> Déployer système monitoring temps réel (délai: 4-6 mois)</li>
                    <li><strong>MOYEN TERME:</strong> Lancer étude faisabilité énergie verte (délai: 6 mois)</li>
                    <li><strong>MOYEN TERME:</strong> Rechercher financements EU/BEI (délai: 6-9 mois)</li>
                </ol>
                <p><strong>Objectif 18 mois:</strong> Atteindre 70% local + réduire coût de 50%</p>
            </div>
            """, unsafe_allow_html=True)
            
        else:  # advanced
            st.markdown(f"""
            <div class="alert-success">
                <h4>🟢 Actions Prioritaires - Niveau Avancé ({secteur_choisi})</h4>
                <ol>
                    <li><strong>URGENT:</strong> Sécuriser approvisionnement 100% bas-carbone (délai: 2-3 mois)</li>
                    <li><strong>COURT TERME:</strong> Lancer projet électricité verte (délai: 6 mois)</li>
                    <li><strong>COURT TERME:</strong> Obtenir certification carbone neutre (délai: 6 mois)</li>
                    <li><strong>MOYEN TERME:</strong> Devenir leader "{secteur_choisi} vert" régional</li>
                    <li><strong>MOYEN TERME:</strong> Valoriser position premium auprès clients EU</li>
                </ol>
                <p><strong>Objectif 24 mois:</strong> Scénario optimal + économie maximale + ROI &lt; 3 ans</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("💡 Complétez l'évaluation de maturité pour des recommandations personnalisées")

# ============================================================================
# TAB 4: SCÉNARIOS & SWOT
# ============================================================================

with tab4:
    st.markdown(f"## 💰 Scénarios de Décarbonation & Analyse SWOT - {secteur_choisi}")
    
    # Génération des scénarios dynamiques selon secteur
    scenarios = [
        {
            'nom': 'Situation Actuelle',
            'pct_local': pct_local * 100,
            'ecp': ecp_calc,
            'depassement': max(0, ecp_calc - st.session_state.benchmark_dynamique),
            'cout_annuel': max(0, ecp_calc - st.session_state.benchmark_dynamique) * st.session_state.prix_cbam_dynamique * production,
            'economie_vs_actuel': 0,
            'description': f'Situation actuelle - {secteur_choisi}',
            'niveau_requis': 'beginner'
        },
        {
            'nom': 'Objectif 50% local',
            'pct_local': 50,
            'ecp': data_sector['ecp_typique_local'] * 0.5 + data_sector['ecp_typique_importe'] * 0.5 + data_sector['emission_process'],
            'depassement': max(0, (data_sector['ecp_typique_local'] * 0.5 + data_sector['ecp_typique_importe'] * 0.5 + data_sector['emission_process']) - st.session_state.benchmark_dynamique),
            'cout_annuel': max(0, (data_sector['ecp_typique_local'] * 0.5 + data_sector['ecp_typique_importe'] * 0.5 + data_sector['emission_process']) - st.session_state.benchmark_dynamique) * st.session_state.prix_cbam_dynamique * production,
            'economie_vs_actuel': 0,  # Calculé dynamiquement
            'description': 'Premier palier - Réduction modérée',
            'niveau_requis': 'beginner'
        },
        {
            'nom': 'Objectif 70% local',
            'pct_local': 70,
            'ecp': data_sector['ecp_typique_importe'] * 0.3 + data_sector['ecp_typique_local'] * 0.7 + data_sector['emission_process'],
            'depassement': max(0, (data_sector['ecp_typique_importe'] * 0.3 + data_sector['ecp_typique_local'] * 0.7 + data_sector['emission_process']) - st.session_state.benchmark_dynamique),
            'cout_annuel': max(0, (data_sector['ecp_typique_importe'] * 0.3 + data_sector['ecp_typique_local'] * 0.7 + data_sector['emission_process']) - st.session_state.benchmark_dynamique) * st.session_state.prix_cbam_dynamique * production,
            'economie_vs_actuel': 0,
            'description': 'Position compétitive acceptable',
            'niveau_requis': 'intermediate'
        },
        {
            'nom': '100% Bas-Carbone',
            'pct_local': 100,
            'ecp': data_sector['ecp_typique_local'] + data_sector['emission_process'],
            'depassement': max(0, (data_sector['ecp_typique_local'] + data_sector['emission_process']) - st.session_state.benchmark_dynamique),
            'cout_annuel': max(0, (data_sector['ecp_typique_local'] + data_sector['emission_process']) - st.session_state.benchmark_dynamique) * st.session_state.prix_cbam_dynamique * production,
            'economie_vs_actuel': 0,
            'description': 'Excellence environnementale',
            'niveau_requis': 'advanced'
        },
        {
            'nom': 'Combiné Optimal',
            'pct_local': 100,
            'ecp': data_sector['ecp_typique_local'] * 0.5,  # Avec énergie verte
            'depassement': max(0, data_sector['ecp_typique_local'] * 0.5 - st.session_state.benchmark_dynamique),
            'cout_annuel': max(0, data_sector['ecp_typique_local'] * 0.5 - st.session_state.benchmark_dynamique) * st.session_state.prix_cbam_dynamique * production,
            'economie_vs_actuel': 0,
            'description': '100% local + Électricité verte + Optimisations',
            'niveau_requis': 'advanced'
        }
    ]
    
    # Calcul des économies
    cout_actuel = scenarios[0]['cout_annuel']
    for s in scenarios:
        s['economie_vs_actuel'] = cout_actuel - s['cout_annuel']
    
    # Comparaison scénarios
    st.markdown("### 📊 Comparaison des Scénarios")
    
    fig_scenarios = creer_comparaison_scenarios(scenarios, st.session_state.benchmark_dynamique, secteur_choisi)
    st.plotly_chart(fig_scenarios, use_container_width=True)
    
    st.markdown("---")
    
    # Détails scénarios
    st.markdown("### 🔍 Détails des Scénarios")
    
    for i, scenario in enumerate(scenarios):
        # Déterminer si recommandé selon maturité
        est_recommande = False
        if st.session_state.maturite_evaluee:
            if st.session_state.niveau_maturite == 'beginner' and scenario['niveau_requis'] == 'beginner':
                est_recommande = True
            elif st.session_state.niveau_maturite == 'intermediate' and scenario['niveau_requis'] == 'intermediate':
                est_recommande = True
            elif st.session_state.niveau_maturite == 'advanced' and scenario['niveau_requis'] == 'advanced':
                est_recommande = True
        
        expanded = (i == 4) or est_recommande
        
        titre = f"**{scenario['nom']}** - {scenario['description']}"
        if est_recommande:
            titre = f"⭐ {titre} (RECOMMANDÉ POUR VOUS)"
        
        with st.expander(titre, expanded=expanded):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Coût Annuel",
                    f"{scenario['cout_annuel']/1e6:.2f}M EUR",
                    delta=f"{scenario['economie_vs_actuel']/1e6:.2f}M EUR" if scenario['economie_vs_actuel'] != 0 else None
                )
            
            with col2:
                st.metric(
                    "ECP",
                    f"{scenario['ecp']:.2f} tCO2/unité",
                    delta=f"{scenario['ecp'] - scenarios[0]['ecp']:.2f}"
                )
            
            with col3:
                reduction = (scenarios[0]['ecp'] - scenario['ecp']) / scenarios[0]['ecp'] * 100
                st.metric(
                    "Réduction",
                    f"{reduction:.0f}%",
                    delta="vs actuel"
                )
            
            with col4:
                st.metric(
                    "% Local",
                    f"{scenario['pct_local']:.0f}%"
                )
            
            if i == 4:  # Scénario optimal
                st.markdown(f"""
                <div class="alert-success">
                    <h4>🎯 SCÉNARIO OPTIMAL - {secteur_choisi}</h4>
                    <p><strong>Combinaison 100% bas-carbone + Électricité verte + Optimisations</strong></p>
                    <p>✅ Économie maximale: {scenario['economie_vs_actuel']/1e6:.2f}M EUR/an</p>
                    <p>✅ Réduction émissions: {((scenarios[0]['ecp']-scenario['ecp'])/scenarios[0]['ecp']*100):.0f}%</p>
                    <p>✅ ECP final: {scenario['ecp']:.2f} tCO2/unité</p>
                    <p>✅ ROI estimé: &lt; 3 ans</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Trajectoire temporelle
    st.markdown("### 📈 Projections Temporelles 2025-2034")
    
    fig_trajectoire = creer_trajectoire_temporelle(
        production, 
        ecp_calc, 
        st.session_state.benchmark_dynamique, 
        st.session_state.prix_cbam_dynamique,
        scenarios
    )
    st.plotly_chart(fig_trajectoire, use_container_width=True)
    
    st.markdown("""
    <div class="alert-warning">
        <h4>⏰ Points Clés Temporels</h4>
        <p><strong>2026 T1:</strong> Première déclaration CBAM obligatoire (11 mois)</p>
        <p><strong>2026 T2:</strong> Extension probable Scope 2 (électricité)</p>
        <p><strong>2027:</strong> Début paiements effectifs CBAM</p>
        <p><strong>2027-2028:</strong> Extension probable Scope 3 (chaîne approvisionnement)</p>
        <p><strong>2030:</strong> Facteur correcteur 51% → Impact financier majeur</p>
        <p><strong>2034:</strong> Facteur correcteur 100% → Plein effet CBAM</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ANALYSE SWOT
    st.markdown("---")
    st.markdown(f"## 🎯 Analyse SWOT Stratégique - {secteur_choisi}")
    
    swot_data = generer_swot(
        secteur_choisi, 
        st.session_state.niveau_maturite if st.session_state.maturite_evaluee else 'beginner',
        st.session_state.reponses
    )
    
    afficher_swot(swot_data)
    
    # Matrice stratégique SWOT
    st.markdown("---")
    st.markdown("### 🎲 Matrice Stratégique")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="alert-success">
            <h4>🚀 Stratégies Offensives (SO)</h4>
            <ul>
                <li>Utiliser vos forces pour saisir les opportunités du marché vert UE</li>
                <li>Certifier rapidement votre avantage carbone vs concurrents</li>
                <li>Développer des partenariats privilégiés avec acheteurs engagés</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="alert-info">
            <h4>🛡️ Stratégies de Renforcement (WO)</h4>
            <ul>
                <li>Combler les lacunes via financements UE disponibles</li>
                <li>Externaliser la conformité CBAM si expertise interne limitée</li>
                <li>Former rapidement les équipes pour réduire le risque opérationnel</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="alert-warning">
            <h4>⚔️ Stratégies de Défense (ST)</h4>
            <ul>
                <li>Accélérer la réduction d'empreinte avant 2027 (début paiements)</li>
                <li>Diversifier les marchés pour réduire la dépendance UE</li>
                <li>Constituer un fonds de précaution pour les coûts CBAM</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="alert-critical">
            <h4>🆘 Stratégies de Survie (WT)</h4>
            <ul>
                <li>Plan d'urgence si non-conformité risquée</li>
                <li>Revitalisation stratégique rapide (M&A, repositionnement)</li>
                <li>Exit du marché UE si coûts prohibitifs vs marges</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# TAB 5: RAPPORT EXÉCUTIF
# ============================================================================

with tab5:
    st.markdown(f"## 📋 Rapport Exécutif Synthétique - {secteur_choisi}")
    
    questions_minimum = 5 if not st.session_state.maturite_evaluee else 13
    
    if len(st.session_state.reponses) + len(st.session_state.reponses_maturite) < questions_minimum:
        st.warning(f"""
        ⚠️ **Rapport incomplet**
        
        Vous devez répondre à au moins {questions_minimum} questions pour générer un rapport complet.
        
        **Progression:** {len(st.session_state.reponses) + len(st.session_state.reponses_maturite)} questions répondues
        """)
    else:
        score = calculer_score_maturite(st.session_state.reponses)
        
        st.markdown(f"""
        <div class="main-header">
            <h2>📊 RAPPORT EXÉCUTIF - {secteur_choisi.upper()}</h2>
            <h3>Score Maturité Global: {score:.0f}%</h3>
            {f'<h3>Niveau CBAM/ESG: {st.session_state.niveau_maturite.upper()}</h3>' if st.session_state.maturite_evaluee else ''}
            <p>{datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Synthèse 3 points
        st.markdown("### 🎯 Synthèse en 3 Points")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="alert-critical">
                <h4>1️⃣ SITUATION</h4>
                <p><strong>Secteur:</strong> {secteur_choisi}</p>
                <p><strong>ECP:</strong> {ecp_calc:.2f} tCO2/unité</p>
                <p><strong>Dépassement:</strong> {(ecp_calc/st.session_state.benchmark_dynamique):.1f}x benchmark</p>
                <p><strong>Coût:</strong> {cout_calc/1e6:.1f}M EUR/an</p>
                <p style="color: #C62828; font-weight: bold;">��� NON CONFORME</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Scénario recommandé selon maturité
            if st.session_state.maturite_evaluee:
                if st.session_state.niveau_maturite == 'beginner':
                    scenario_cible = scenarios[1]  # 50% local
                elif st.session_state.niveau_maturite == 'intermediate':
                    scenario_cible = scenarios[2]  # 70% local
                else:
                    scenario_cible = scenarios[4]  # Optimal
            else:
                scenario_cible = scenarios[4]
            
            st.markdown(f"""
            <div class="alert-success">
                <h4>2️⃣ OPPORTUNITÉ</h4>
                <p><strong>Scénario:</strong> {scenario_cible['nom']}</p>
                <p><strong>Économie:</strong> {scenario_cible['economie_vs_actuel']/1e6:.1f}M EUR/an</p>
                <p><strong>Réduction:</strong> {((scenarios[0]['ecp']-scenario_cible['ecp'])/scenarios[0]['ecp']*100):.0f}%</p>
                <p style="color: #2E7D32; font-weight: bold;">✅ RÉALISABLE</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="alert-warning">
                <h4>3️⃣ URGENCE</h4>
                <p><strong>Déclaration:</strong> T1 2026 (11 mois)</p>
                <p><strong>Paiements:</strong> 2027 (19 mois)</p>
                <p><strong>Fenêtre:</strong> 6-12 mois</p>
                <p style="color: #F57C00; font-weight: bold;">⏰ ACTION IMMÉDIATE</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Plan d'action adapté à la maturité
        st.markdown("### 🎯 Plan d'Action Recommandé")
        
        if st.session_state.maturite_evaluee:
            niveau = st.session_state.niveau_maturite
            
            col1, col2 = st.columns(2)
            
            with col1:
                if niveau == 'beginner':
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>🚨 IMMÉDIAT (0-3 mois) - {secteur_choisi}</h4>
                        <ol>
                            <li>Formation direction CBAM (urgence critique)</li>
                            <li>Lancement audit empreinte carbone certifié</li>
                            <li>Désignation responsable CBAM/ESG</li>
                            <li>Constitution équipe projet minimaliste</li>
                            <li>Premiers contacts fournisseurs bas-carbone</li>
                        </ol>
                    </div>
                    """, unsafe_allow_html=True)
                elif niveau == 'intermediate':
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>🚨 IMMÉDIAT (0-3 mois) - {secteur_choisi}</h4>
                        <ol>
                            <li>Finalisation certification ISO 14064</li>
                            <li>Déploiement système monitoring temps réel</li>
                            <li>Négociation contrats fournisseurs 70%</li>
                            <li>Lancement étude énergie verte</li>
                            <li>Préparation dossiers financements EU</li>
                        </ol>
                    </div>
                    """, unsafe_allow_html=True)
                else:  # advanced
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>🚨 IMMÉDIAT (0-3 mois) - {secteur_choisi}</h4>
                        <ol>
                            <li>Sécurisation approvisionnement 100% bas-carbone</li>
                            <li>Lancement projet électricité verte</li>
                            <li>Demande certification carbone neutre</li>
                            <li>Stratégie communication "{secteur_choisi} vert"</li>
                            <li>Valorisation premium clients EU</li>
                        </ol>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                if niveau == 'beginner':
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>⏱️ COURT TERME (3-6 mois) - {secteur_choisi}</h4>
                        <ol>
                            <li>Mise en place traçabilité basique</li>
                            <li>Négociation passage {pct_local*100:.0f}% → 50% local</li>
                            <li>Formation équipe sur reporting CBAM</li>
                            <li>Identification fournisseurs alternatifs</li>
                            <li>Préparation 1ère déclaration CBAM</li>
                        </ol>
                    </div>
                    """, unsafe_allow_html=True)
                elif niveau == 'intermediate':
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>⏱️ COURT TERME (3-6 mois) - {secteur_choisi}</h4>
                        <ol>
                            <li>Signature contrats long terme 70%</li>
                            <li>Obtention financements EU/BEI</li>
                            <li>Lancement travaux infrastructure verte</li>
                            <li>Roadmap détaillée 2025-2030</li>
                            <li>Communication externe position ESG</li>
                        </ol>
                    </div>
                    """, unsafe_allow_html=True)
                else:  # advanced
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>⏱️ COURT TERME (3-6 mois) - {secteur_choisi}</h4>
                        <ol>
                            <li>Mise en service infrastructure électricité verte</li>
                            <li>Obtention certification carbone neutre</li>
                            <li>Lancement marketing "{secteur_choisi} vert"</li>
                            <li>Partenariats R&D décarbonation</li>
                            <li>Leadership sectoriel régional</li>
                        </ol>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>🚨 IMMÉDIAT (0-3 mois) - {secteur_choisi}</h4>
                    <ol>
                        <li>Audit complet empreinte carbone certifié</li>
                        <li>Système monitoring temps réel</li>
                        <li>Formation équipe direction CBAM/ESG</li>
                        <li>Consultation juridique conformité</li>
                        <li>Recherche financements EU/BEI/AFD</li>
                    </ol>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>⏱️ COURT TERME (3-6 mois) - {secteur_choisi}</h4>
                    <ol>
                        <li>Négociation fournisseurs (↑{pct_local*100:.0f}%→70%)</li>
                        <li>Étude faisabilité énergie verte</li>
                        <li>Identification fournisseurs alternatifs</li>
                        <li>Roadmap décarbonation 2025-2030</li>
                        <li>Préparation 1ère déclaration CBAM</li>
                    </ol>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Message décideur adapté
        st.markdown(f"""
        <div class="main-header" style="background: linear-gradient(135deg, #C62828 0%, #F57C00 100%);">
            <h3>✅ MESSAGE AU DÉCIDEUR - {secteur_choisi.upper()}</h3>
            <p style="text-align: left; font-size: 1.1em; padding: 1rem;">
            <strong>Le CBAM n'est pas une contrainte passagère, c'est une RÉVOLUTION du commerce UE.</strong>
            <br><br>
            <strong>Vous avez DEUX CHOIX:</strong>
            <br><br>
            1️⃣ <strong>SUBIR:</strong> Payer {cout_calc/1e6:.1f}M EUR/an (croissant) + risque exclusion marché UE
            <br><br>
            2️⃣ <strong>ANTICIPER:</strong> Investir maintenant → économiser jusqu'à {scenarios[4]['economie_vs_actuel']/1e6:.1f}M EUR/an + 
            devenir leader "{secteur_choisi} vert" + ROI &lt; 3 ans
            <br><br>
            <strong>⏰ Fenêtre d'action: 6-12 MOIS maximum.</strong>
            <br><br>
            Chaque mois de retard = 500k+ EUR/an de surcoût et perte compétitivité.
            <br><br>
            <strong>🎯 DÉCISION STRATÉGIQUE REQUISE: MAINTENANT</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Export
        st.markdown("---")
        st.markdown("### 📥 Export du Rapport")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 PDF", use_container_width=True):
                st.info("Fonctionnalité export PDF à venir")
        
        with col2:
            if st.button("📊 Excel", use_container_width=True):
                st.info("Fonctionnalité export Excel à venir")
        
        with col3:
            if st.button("📧 Email", use_container_width=True):
                st.info("Fonctionnalité envoi email à venir")

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>Dashboard CBAM/ESG Universel Multi-Secteurs avec Analyse SWOT</strong></p>
    <p>Version 4.0 - Outil d'Aide à la Décision Stratégique Personnalisé</p>
    <p>Secteur actuel: <strong>{secteur_choisi}</strong> | Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}</p>
</div>
""", unsafe_allow_html=True)
