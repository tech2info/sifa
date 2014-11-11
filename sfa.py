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
import datetime
import time



class sfp_contrat(orm.Model):
    _name = 'sfp.contrat'
    _columns = {
        'name': fields.char(u'Numero'),        
        'type': fields.char(u'Type'),
        'etat': fields.char(u'Etat'),
        'relation': fields.char(u'Relation'),
        'etat': fields.char(u'Etat'),
        'parent_link': fields.char(u'Lien Parental'),
        'date_start': fields.datetime(u'Date debut'),
        'date_end': fields.datetime(u"Date fin"), 
        'date_abandon': fields.datetime(u"Date abandon"), 
        'apprenti': fields.many2one('sfp.apprenti',u'Apprenti'),  
        'groupe': fields.many2one('sfp.groupe',u'Groupe'),
        'metier': fields.many2one('sfp.metier',u'Metier'),
        'responsable': fields.many2one('res.users',u'Responsable'),
        'user': fields.many2one('res.users',u'Responsable'),
        'entreprise': fields.many2one('res.partner',u'Entreprise'),
        'maitre': fields.many2one('sfp.maitre',u'Maitre'),
        'cfa': fields.many2one('sfp.cfa',u'CFA'),
        'annexe': fields.many2one('sfp.annexe',u'Annexe'),
        'province': fields.many2one('sfp.province',u'Province'),
        'vacataire': fields.many2one('sfp.vacataire',u'Vacataire'),
        'description': fields.text(u'Description'),
    }
    


class sfp_matier(orm.Model):
    _name = 'sfp.matier'
    _columns = {
        'name': fields.char('Nom'),
        'code': fields.char('Code', translate=True),
        'description': fields.text('Description', translate=True),
        'vacataire': fields.many2one('sfp.vacataire','Vacataire', translate=True),
        
    }


class sfp_grade(orm.Model):
    _name = 'sfp.grade'
    _columns = {
        'name': fields.char('Nom'),
        'code': fields.char('Code', translate=True),
        'description': fields.text('Description', translate=True),
        'vacataire': fields.many2one('sfp.vacataire','Vacataire', translate=True),
        
    }

class sfp_sector(orm.Model):
    _name = 'sfp.sector'
    _columns = {
        'name': fields.char('Nom'),
        'code': fields.char('Code', translate=True),
        'description': fields.text('Description', translate=True),
        
    }

class sfp_level(orm.Model):
    _name = 'sfp.level'
    _columns = {
        'name': fields.char('Name'),
        'code': fields.char('Code', translate=True),
        'description': fields.text('Description', translate=True),
        
    }
    

class sfp_metier(orm.Model):
    _name = 'sfp.metier'
    _columns = {
        'name': fields.char('Name'),
        'code': fields.char('Code', translate=True),
        
        'dure': fields.selection([('11',u'11 Mois'),('22',u'22 Mois')],u'Dure',required=True),
        'level': fields.many2one('sfp.level', 'Niveau',translate=True),
        'sector': fields.many2one('sfp.sector', 'Secteur',translate=True),
        'description': fields.text('Description', translate=True),
    }
    

class sfp_annexe(orm.Model):
    _name = 'sfp.annexe'
    _columns = {
        'name': fields.char('Nom'),
        'code': fields.char('Code', translate=True),
        'description': fields.text('Description', translate=True),    
        'province': fields.many2one('sfp.province','Code', translate=True),
    }




class sfp_province(orm.Model):
    _name = 'sfp.province'
    _columns = {
        'name': fields.char('Nom'),
        'code': fields.char('Code', translate=True),
        'annexe': fields.one2many('sfp.annexe','province','Annexe'),
        'description': fields.text('Description', translate=True),
    }

class sfp_cfa(orm.Model):
    _name = 'sfp.cfa'
    _columns = {
        'name': fields.char('Nom'),        
        'code': fields.char('Code', translate=True),
        'province': fields.many2one('sfp.province','Province'),  
        'description': fields.text('Description', translate=True),
    }


class sfp_groupe(orm.Model):
    _name = 'sfp.groupe'
    _columns = {
        'name': fields.char('Nom'),        
        'code': fields.char('Code', translate=True),
        'date_start': fields.datetime('Date debut'),
        'date_end': fields.datetime("Date fin"), 
        'apprenti_ids': fields.one2many('sfp.apprenti','groupe',u'Province'),  
        'description': fields.text('Description', translate=True),
    }
    
