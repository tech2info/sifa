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
from openerp import tools
from openerp.tools.translate import _
import time
from datetime import date


class sfp_contrat(orm.Model):
    _name = 'sfp.contrat'
    _description = 'les contrats'
    
    def create(self, cr, user, vals, context=None):
        u"""méthode créer"""
        if ('name' not in vals) or (vals.get('name')=='/'):
            vals['name'] = self.pool.get('ir.sequence').get(cr, user, 'sfp.contrat')
        return super(sfp_contrat, self).create(cr, user, vals, context) 
    
    def action_preinscription(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state' : 'preinscription'})
    
    def action_training(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state' : 'en_formation'})
    
    def action_laureat(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state' : 'laureat'})
    
    def action_cancel(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state' : 'cancel'})
    
  
    _columns = {
        'name': fields.char(u'Numero'),        
        'declaration': fields.boolean(u'Declaration'),
        'etat': fields.selection([('abandon',u'Abandon'),('loureat',u'Loureat'),('formation',u'En formation')],u'Etat'),
        'relation': fields.char(u'Relation'),
        'parent_link': fields.char(u'Lien Parental'),
        'date_start': fields.datetime(u'Date debut'),
        'date_end': fields.datetime(u"Date fin"), 
        'date_abandon': fields.datetime(u"Date abandon"), 
        'apprenti': fields.many2one('sfp.apprenti',u'Apprenti'),  
        'groupe': fields.many2one('sfp.groupe',u'Groupe'),
        'metier': fields.many2one('sfp.metier',u'Metier'),
        'responsable': fields.many2one('res.users',u'Responsable'),
        'user': fields.many2one('res.users',u'Utilisateur'),
        'entreprise': fields.many2one('res.partner',u'Entreprise',domain=[('entreprise_ok','=',True)]),
        'maitre': fields.many2one('sfp.maitre',u'Maitre'),
        'cfa': fields.many2one('sfp.cfa',u'CFA'),
        'annexe': fields.many2one('sfp.annexe',u'Annexe'),
        'province': fields.many2one('sfp.province',u'Province'),
        'vacataire': fields.many2one('res.partner',u'Vacataire',domain=[('vacataire_ok','=',True)]),
        'description': fields.text(u'Description'),
        'invoice_ids': fields.one2many('account.invoice','contrat_id',u'Les Factures'),
        'state' : fields.selection([('preinscription',u'Préinscription'),('en_formation',u'En formation'),('loreat',u'Lauréat'),('cancel',u'Abandonné')],u'Statut',required=True),
   
    }
    
    _defaults = {  
        'state': lambda *a: 'preinscription',
        'user' : lambda x, y, z, c: z,
        'name': lambda self, cr, uid, context: '/',
        'date_start': lambda *a : time.strftime('%Y-%m-%d'),
        }

   
    """def onchange_grade(self,cr,uid,ids,grade,context={}):
        data={}
        if grade:
            object_grade=self.pool.get('sfp.grade').browse(cr,uid,grade)
            if object_grade:
                data['price'] = object_grade.price_h or False
        return {'value' : data }"""
        
    
class sfp_tuteur(orm.Model):
    _name = 'sfp.tuteur'
    _columns = {
        'name_ar': fields.char(u'الاسم',required=True),        
        'last_name_ar': fields.char(u'النسب', translate=True),
        'date_birth': fields.datetime(u'تاريخ الازدياد'),
        'lieu_ar': fields.char(u'مكان الازدياد'), 
        'na_ar': fields.char(u'الصفة'),   
        'adresse_ar': fields.char(u'عوان محل السكنى'),
        'profession_ar': fields.char(u'المهنة'),    
        'tel_ar': fields.char(u'Tel'), 
        'cin_ar': fields.char(u'CIN',required=True),   
        'description': fields.text(u'Description'),  
    }
    

class sfp_maitre(orm.Model):
    _name = 'sfp.maitre'
    _columns = {
                
        'name': fields.char(u'Nom',required=True),
        'last_name': fields.char(u'Prènom'), 
        'name_ar': fields.char(u'الاسم'),        
        'last_name_ar': fields.char(u'النسب'),
        'encadrant': fields.char(u'بصفته مؤطر بالمقاولة'),
        'gender' : fields.selection([('male',u'Masculin'),('female',u'Féminin')],u'Sexe',required=True),    
        'age': fields.char(u'Age'),
        'n_entreprise': fields.char(u'N entreprise'),    
        'tel': fields.char(u'Tel'), 
        'cin': fields.char(u'CIN'),   
        'description': fields.text(u'Description'),  
    }
    
    
    
class sfp_apprenti(orm.Model):
    
    _name='sfp.apprenti'
    
    
    def _get_age(self, cr, uid, ids, name, arg, context={}):
        data={}
        for object_parent in self.browse(cr,uid,ids):
            data[object_parent.id] = 0
            today = date.today()
            if object_parent.birthdate:
                date_birth=time.strptime(object_parent.birthdate, '%Y-%m-%d')
                data[object_parent.id]=today.year-date_birth.tm_year
        return data
 
    _columns = {
            'name': fields.char('Name', required=True, select=True),
            'name_arabic' : fields.char(u'الإسم '),
            'first_name_arabic' : fields.char(u'النسب'),
            'birthdate': fields.char('Birthdate'),
            'lieu_birth' : fields.char(u'lieu de naissance'),
            'age' : fields.function(_get_age,type='integer',string=u'âge'),
            'cin' : fields.char(u'CIN',size=50),
            'function': fields.char('Job Position'),
            'gender_' : fields.selection([('male',u'Masculin'),('female',u'Féminin')],u'Sexe'), 
            'gender_ar' : fields.selection([('male',u'دكر'),('female',u'انتى')],u'الجنس'), 
            'image': fields.binary("Image",help="This field holds the image used as avatar for this contact, limited to 1024x1024px"),
            
            'street': fields.char('Street'),
            'street2': fields.char('Street2'),
            'zip': fields.char('Zip', size=24, change_default=True),
            'city': fields.char('City'),
            'state_id': fields.many2one("res.country.state", 'State', ondelete='restrict'),
            'country_id': fields.many2one('res.country', 'Country', ondelete='restrict'),
            'email': fields.char('Email'),
            'phone': fields.char('Phone'),
            'fax': fields.char('Fax'),
            'mobile': fields.char('Mobile'),
            'website': fields.char('Website', help="Website of Partner or Company"),
             
            'nv_scolaire' : fields.char(u'Niveau scolaire',size=50),
            'dure_formation' : fields.char(u'Dure de formation',size=50),
            'diplom' : fields.char(u'Diplom',size=50),
            'user': fields.many2one('res.users',u'Utilisateur'),

            'function_ar' : fields.char(u'الحرفة',size=50),
            'parental_ar' : fields.char(u'القرابة العائلية',size=50),
            'dure_ar' : fields.char(u'مدة التكوين',size=50),
            'profession_tuteur_ar' : fields.char(u'مهة الاب او ولي الامر ',size=50),
            'situation_ar' : fields.char(u'الوضعية قبل الانخراط',size=50),
            }
    

class sfp_matier(orm.Model):
    _name = 'sfp.matier'
    _columns = {
        'name': fields.char(u'Nom', required=True),
        'code': fields.char(u'Code', translate=True),
        'description': fields.text(u'Description', translate=True),
        'vacataire': fields.many2one('res.partner',u'Vacataire', translate=True),
        
        
    }


class sfp_grade(orm.Model):
    _name = 'sfp.grade'
    _columns = {
        'name': fields.char(u'Nom', required=True),
        'code': fields.char(u'Code', translate=True),
        'price_h': fields.float(u'Taux horaire'),
        'description': fields.text(u'Description', translate=True),
        'vacataire': fields.many2one('res.partner',u'Vacataire', translate=True),
        
    }

class sfp_sector(orm.Model):
    _name = 'sfp.sector'
    _columns = {
        'name': fields.char(u'Nom', required=True),
        'code': fields.char(u'Code', translate=True),
        'description': fields.text(u'Description', translate=True),
        'metier_train_ids': fields.one2many('sfp.sectortraining','sector_id',u'Secteurs de Formation'),
        
    }

class sfp_training_sector(orm.Model):
    _name = 'sfp.sectortraining'
    _columns = {
        'name': fields.char(u'Nom', required=True),
        'code': fields.char(u'Code', translate=True),
        'description': fields.text(u'Description', translate=True),
        'metier_ids': fields.one2many('sfp.metier','sect_id',u'Metiers'),
        'sector_id': fields.many2one('sfp.sector', u'Secteur'),
        
    }
class sfp_level(orm.Model):
    _name = 'sfp.level'
    _columns = {
        'name': fields.char(u'Name', required=True),
        'code': fields.char(u'Code', translate=True),
        'description': fields.text(u'Description', translate=True),
        
    }
    

class sfp_metier(orm.Model):
    _name = 'sfp.metier'
    _columns = {
        'name': fields.char(u'Name', required=True),
        'name_ar': fields.char(u'الاسم'),
        'code': fields.char(u'Code', translate=True),      
        'duree': fields.many2one('metier.duration',u'Durée',required=True),
        'level': fields.many2one('sfp.level', u'Niveau'),
        'sector': fields.many2one('sfp.sector', u'Secteur'),
        'description': fields.text(u'Description'),
        'sect_id': fields.many2one('sfp.sectortraining', u'Secteur de formation'),
    }

class metier_duration(orm.Model):
    _name = 'metier.duration'
    _columns = {
        'duree': fields.integer(u'Durée', required=True),
        'description': fields.char(u'Description'),      
    }    

class sfp_annexe(orm.Model):
    _name = 'sfp.annexe'
    _columns = {
        'name': fields.char(u'Nom', required=True),
        'code': fields.char(u'Code', translate=True),
        'description': fields.text(u'Description', translate=True),    
        'province': fields.many2one('sfp.province','province'),
    }




class sfp_province(orm.Model):
    _name = 'sfp.province'
    _columns = {
        'name': fields.char(u'Nom', required=True),
        'code': fields.char(u'Code', translate=True),
        'annexe': fields.one2many('sfp.annexe','province',u'Annexe'),
        'description': fields.text(u'Description', translate=True),
        'cfa': fields.many2one('sfp.cfa',u'CFA'),
    }

class sfp_cfa(orm.Model):
    _name = 'sfp.cfa'
    _columns = {
        'name': fields.char(u'Nom', required=True),        
        'code': fields.char(u'Code', translate=True),
        'province': fields.one2many('sfp.province','cfa',u'Province'),  
        'description': fields.text(u'Description', translate=True),
    }


class sfp_groupe(orm.Model):
    _name = 'sfp.groupe'
    _columns = {
        'name': fields.char(u'Nom', required=True),        
        'code': fields.char(u'Code', translate=True),
        'date_start': fields.datetime(u'Date debut'),
        'date_end': fields.datetime(u'Date fin'),  
        'contrat_ids': fields.one2many('sfp.contrat','groupe',u'Contrats'), 
        'description': fields.text(u'Description', translate=True),
    }
    
