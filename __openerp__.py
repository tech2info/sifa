# -*- coding: utf-8 -*-
################################################################################
#
#    SFA for Odoo                                                  
#    Copyright (C) 2015 Ait-Mlouk Addi - (<aitmlouk@gmail.com>)
#                 (<http://www.odoo-services.esy.es/>)
#                                                                               
#    This program is free software: you can redistribute it and/or modify       
#    it under the terms of the GNU Affero General Public License as             
#    published by the Free Software Foundation, either version 3 of the         
#    License, or (at your option) any later version.                            
#                                                                               
#    This program is distributed in the hope that it will be useful,            
#    but WITHOUT ANY WARRANTY; without even the implied warranty of             
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              
#    GNU Affero General Public License for more details.                        
#                                                                               
#    You should have received a copy of the GNU Affero General Public License   
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.    
#
################################################################################
{
    "name": "SIFA- Vertical for Odoo  ",
    "version": "1.0",
    "depends": ['base','account','account_voucher','contacts'],
    "author": "Ait-Mlouk Addi/Infoset R&D",
    'website': 'http://www.infosit.ma/',
    'sequence':1,
    "category": "Specific Modules/sifa",
    'summary' : 'Contrats, Entreprises, Apprentis, vacataires',
    "description": """
Système informatique de formation par apprentissage est un système complet qui gère le processus de formation 
par apprentissage d'un  ensembles de groupes des apprentis qui ont inscrit dans une  formation 
aupres des centres cfa .il constituent de:
 - contart.
 - Metiers.
 - Apprenties.
 - Vacataires.
 - Groupes.
 - Entreprises.
 - centres de formation.
 - ...
With this module you can following all contracts.
""",


    "init_xml": [],
    'update_xml': [
        'sfa_view.xml',
        'partner_view.xml',   
        'invoice_view.xml',
        'certificate_view.xml',
        'attached_piece.xml',
        'sfa_report.xml',
        'report/report_declaration_sfa.xml',
        'report/report_contrat_sfa.xml',
        'report/admin_certificate_sfa.xml',
        'report/apprenti_certificate_sfa.xml',
        'report/specialized_certificate_sfa.xml',
        'report/complement_report_contrat_sfa.xml',
        'report/report_groupe_average.xml',
        'views/report_apprenti.xml',
        'sfa_menu.xml',
        'data/sfa_data.xml',
        'data/sfa_sequence.xml',
        
    ],
    'demo': [
                 'demo/res.company.csv',
                 ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
