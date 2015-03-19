# -*- encoding: utf-8 -*-
#################################################################################
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
#################################################################################
from openerp.osv import orm, fields

class sfp_contrat(orm.Model):
    _inherit ='sfp.contrat'
    _description = 'les pieces joints'
    

    _columns = {       
        'condition1': fields.boolean(u'Age: 15 à 30 ans '),
        'condition2': fields.boolean(u'Attestation scolaire'),
        'condition3': fields.boolean(u'Certificat d\'apprentissage'),
        'condition4': fields.boolean(u'3 copies d’acte de naissance '),
        'condition5': fields.boolean(u'4 photos '),
        'condition6': fields.boolean(u'Photocopie CIN d’apprenti ou son tuteur '),
        
        'condition7': fields.boolean(u' Agé : min 20 ans  '),
        'condition10': fields.boolean(u'Taxe professionnelle (patente) '),
        'condition13': fields.boolean(u'2 photos '),
        'condition14': fields.boolean(u'Photocopie CIN '),
        'condition15': fields.boolean(u'Photocopie de  Carte professionnelle '),
        

        'condition20': fields.boolean(u'2 photos '),
        'condition21': fields.boolean(u'Photocopie CIN '),
        'condition22': fields.boolean(u'Photocopie de  Carte professionnelle '),

       }
        
        
 