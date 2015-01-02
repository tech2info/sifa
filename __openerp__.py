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
    "name": "SFA- Vertical for Odoo",
    "version": "0.1",
    "depends": ['base','account','account_voucher','contacts'],
    "author": "Infoset R&D/Ait-Mlouk Addi",
    'website': 'http://www.infosit.ma/',
    'sequence':1,
    "category": "Specific Modules/SFA",
    'summary' : 'Contrats, Entreprises, Apprentis, vacataires',
    "description": """
Système de formation par apprentissage est un système complet qui gère le processus de formation 
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
        'sfa_menu.xml',
        'sfa_report.xml',
        'views/report_apprenti.xml',
        'data/sfa_data.xml',
        'data/sfa_sequence.xml',
        #'views/report_sfa.xml',
       
        
        
    ],
    'demo': [
                 'demo/res.company.csv',
                 ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
