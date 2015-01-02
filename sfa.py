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
from datetime import datetime


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
        'name': fields.char(u'Numero', required=True),        
        'declaration': fields.boolean(u'Declaration'),
        'parent_link': fields.char(u'Lien Parental'),
        'date_start': fields.date(u'Date debut'),
        'date_end': fields.date(u"Date fin"), 
        'date_abandon': fields.date(u"Date abandon"), 
        'apprenti': fields.many2one('sfp.apprenti',u'Apprenti'),  
        'groupe': fields.many2one('sfp.groupe',u'Groupe'),
        'metier': fields.many2one('sfp.metier',u'Metier'),
        'duree': fields.integer(u'Durée de metier'),
        'responsable': fields.many2one('res.partner',u'Tuteur'),
        'user': fields.many2one('res.users',u'Utilisateur'),
        'entreprise': fields.many2one('res.partner',u'Entreprise', domain=[('is_company','=',True)]),
        'maitre': fields.many2one('res.partner',u'Maitre'),
        'chef': fields.many2one('res.partner',u'Chef d\'entreprise'),
        'allocation': fields.float(u'Allocation'),
        'trial': fields.integer(u'période essai'),
        'periode_contrat': fields.integer(u'Période Contrat'),
        'periode_company': fields.integer(u'Période Entreprise'),
        'periode_cfa': fields.integer(u'Période CFA'),
        'periode_work': fields.integer(u'Période Travail'),
        'nbr_inscrit': fields.integer(u'عدد المتدرجين'),
        'maitre_titre': fields.char(u'الصـــــفة'),
        
        'cfa': fields.many2one('sfp.cfa',u'CFA'),
        'province': fields.many2one('sfp.province',u'Province',domain="[('cfa','=',cfa)]"),
        'annexe': fields.many2one('sfp.annexe',u'Annexe',domain="[('cfa','=',cfa)]"),
        'vacataire': fields.many2one('res.partner',u'Vacataire',domain=[('vacataire_ok','=',True)]),
        'nbr_visite' : fields.char(u'Nombre de visites'),
        'description': fields.text(u'Description'),
        'invoice_ids': fields.one2many('account.invoice','contrat_id',u'Les Factures'),
        'state' : fields.selection([('preinscription',u'Préinscription'),('en_formation',u'En formation'),('loreat',u'Lauréat'),('cancel',u'Abandonné')],u'Etat',required=True),
   
    }
    
    _defaults = {  
        'state': lambda *a: 'preinscription',
        'user' : lambda x, y, z, c: z,
        'name': lambda self, cr, uid, context: '/',
        'date_start': lambda *a : time.strftime('%Y-%m-%d'),
        }
    
    def onchange_metier(self,cr,uid,ids,metier,context={}):
        data={}
        if metier:
            object_metier=self.pool.get('sfp.metier').browse(cr,uid,metier)
            if object_metier:
                data['duree'] = object_metier.duree  or False
        return {'value' : data }
        
    
class sfp_tuteur(orm.Model):
    _name = 'sfp.tuteur'
    
    def _get_age(self, cr, uid, ids, name, arg, context={}):
        data={}
        for object_parent in self.browse(cr,uid,ids):
            data[object_parent.id] = 0
            if object_parent.birthdate:
                data[object_parent.id]=(datetime.now()-datetime.strptime(object_parent.birthdate,"%Y-%m-%d")).days/356
        return data
    
    _columns = {
        'name_ar': fields.char(u'الاسم',required=True),        
        'last_name_ar': fields.char(u'النسب', translate=True),
        'birthdate': fields.date(u'تاريخ الازدياد'),
        'lieu_ar': fields.char(u'مكان الازدياد'), 
        'age' : fields.function(_get_age,type='integer',string=u'Age'),
        'na_ar': fields.char(u'الصفة'),   
        'adresse_ar': fields.char(u'عوان محل السكنى'),
        'profession_ar': fields.char(u'المهنة'),    
        'tel_ar': fields.char(u'Tel'), 
        'cin_ar': fields.char(u'CIN',required=True),   
        'description': fields.text(u'Description'),  
    }
    

class sfp_maitre(orm.Model):
    _name = 'sfp.maitre'
    
    def _get_age(self, cr, uid, ids, name, arg, context={}):
        data={}
        for object_parent in self.browse(cr,uid,ids):
            data[object_parent.id] = 0
            if object_parent.birthdate_1:
                data[object_parent.id]=(datetime.now()-datetime.strptime(object_parent.birthdate_1,"%Y-%m-%d")).days/356
        return data
    
    _columns = {
                
        'name': fields.char(u'Nom',required=True),
        'last_name': fields.char(u'Prènom'), 
        'name_ar': fields.char(u'الاسم'),        
        'last_name_ar': fields.char(u'النسب'),
        'encadrant': fields.char(u'بصفته مؤطر بالمقاولة'),
        'gender' : fields.selection([('male',u'Masculin'),('female',u'Féminin')],u'Sexe',required=True),    
        'age': fields.char(u'Age'),
        'maitre': fields.many2one('res.partner',u'Entreprise', domain=[('is_company','=',True)]),    
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
            if object_parent.birthdate_1:
                data[object_parent.id]=(datetime.now()-datetime.strptime(object_parent.birthdate_1,"%Y-%m-%d")).days/356
        return data
 
    _columns = {
            'name': fields.char(u'Nom', required=True, select=True),
            'name_arabic' : fields.char(u'الإسم '),
            'birthdate_1': fields.date(u'Date de Naissance'),
            'lieu_birth' : fields.many2one('birth.place',u'Lieu de naissance'),
            'lieu_birth_ar' : fields.many2one('birth.place',u'مكـــان الازدياد'),
            'age' : fields.function(_get_age,type='integer',string=u'Age'),
            'cin' : fields.char(u'CIN',size=50),
            'gender_' : fields.selection([('male',u'Masculin'),('female',u'Féminin')],u'Sexe'), 
            'gender_ar' : fields.selection([('male',u'دكـــــــر'),('female',u'انــــــتى')],u'الجنــــــس'), 
            'image': fields.binary(u"Image",help="This field holds the image used as avatar for this contact, limited to 1024x1024px"),   
            'street': fields.char(u'Adresse'),
            'street_ar': fields.char(u'Adresse'),
            'street2': fields.char(u'Adresse 2'),
            'zip': fields.char(u'Code Postal', size=24, change_default=True),
            'city': fields.char(u'Ville'),
            'city_ar': fields.char(u'المـــــدينة'),
            'state_id': fields.many2one("res.country.state", 'State', ondelete='restrict'),
            'country_id': fields.many2one('res.country', u'Pays', ondelete='restrict'),
            'email': fields.char(u'Email'),
            'phone': fields.char(u'Tél 1'),
            'mobile': fields.char(u'Tél 2'),
            'website': fields.char(u'Site Web', help="Website of Partner or Company"),   
            'nv_scolaire' : fields.many2one('school.level','Niveau Scolaire',size=50),
            'dure_formation' : fields.char(u'Dure de formation',size=50),
            'user': fields.many2one('res.users',u'Utilisateur'),
            'profession_tuteur_ar' : fields.char(u'مهة الاب او ولي الامر ',size=50),
            'situation_ar' : fields.char(u'الوضعية قبل الانخراط',size=50),
            'contrat_ids': fields.one2many('sfp.contrat','apprenti',u'Les contrats'),
            'description': fields.text(u'Observation', translate=True),
            }
    
    _defaults = {  
        'country_id': 'Maroc',
        }

class school_level(orm.Model):
    _name = 'school.level'
    _columns = {
        'name': fields.char(u'Nom', required=True),
        'name_ar': fields.char(u'الاســـــم', translate=True),
        'description': fields.text(u'Description', translate=True),
   
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
        'name': fields.char(u'Nom', required=True),
        'code': fields.char(u'Code', translate=True),
        'description': fields.text(u'Description', translate=True),
        
    }
    
class birth_place(orm.Model):
    _name = 'birth.place'
    _columns = {
        'name': fields.char(u'Nom', required=True),
        'name_ar': fields.char(u'الاســــــــم', translate=True),
        'description': fields.text(u'Description', translate=True),
        
    }
    
class sfp_metier(orm.Model):
    _name = 'sfp.metier'
    _columns = {
        'name': fields.char(u'Nom', required=True),
        'name_ar': fields.char(u'الاســــــم'),
        'code': fields.char(u'Code', translate=True),      
        'duree': fields.char(u'Durée',required=True),
        'max_age': fields.float(u'Age maximum'),
        'level': fields.many2one('sfp.level', u'Niveau'),
        'sector': fields.many2one('sfp.sector', u'Secteur'),
        'description': fields.text(u'Description'),
        'sect_id': fields.many2one('sfp.sectortraining', u'Secteur de formation'),
        'admission_ids': fields.one2many('admission.level','admission_id', u'Niveau admission'),
    }
    
    def name_get(self, cr, uid, ids, context=None):
        res=[]
        if context is None:
            context = {}
        if not len(ids):
            return []
        if context.get('show_ref'):
            res = [(r['id'], r['ref']) for r in self.read(cr, uid, ids, ['ref'], context)]
        else:
            res = [(r['id'], u'%s' %(r['name_ar'] or '')) for r in self.read(cr, uid, ids, ['name_ar'], context)]
        return res
    
class admission_level(orm.Model):
    _name = 'admission.level'
    _columns = {
        'name': fields.char(u'Nom', required=True),
        'code': fields.char(u'Code', translate=True),    
        'description': fields.text(u'Description', translate=True),  
        'admission_id': fields.many2one('sfp.metier', u'Admission'),   
    }

class sfp_annexe(orm.Model):
    _name = 'sfp.annexe'
    _columns = {
        'name': fields.char(u'Nom', required=True),
        'code': fields.char(u'Code', translate=True),
        'description': fields.text(u'Description', translate=True),    
        'cfa': fields.many2one('sfp.cfa',u'CFA'),
    }


class sfp_province(orm.Model):
    _name = 'sfp.province'
    _columns = {
        'name': fields.char(u'Nom', required=True),
        'code': fields.char(u'Code', translate=True),
        'description': fields.text(u'Description', translate=True),
        'cfa': fields.many2one('sfp.cfa',u'CFA'),
    }

class sfp_cfa(orm.Model):
    _name = 'sfp.cfa'
    _columns = {
        'name': fields.char(u'Nom', required=True),        
        'code': fields.char(u'Code', translate=True),
        'province_ids': fields.one2many('sfp.province','cfa',u'Provinces'),  
        'annexe_ids': fields.one2many('sfp.annexe','cfa',u'Annexes'), 
        'description': fields.text(u'Description', translate=True),
    }


class sfp_groupe(orm.Model):
    _name = 'sfp.groupe'
    _columns = {
        'name': fields.char(u'Nom', required=True),        
        'code': fields.char(u'Code', translate=True),
        'date_start': fields.date(u'Date debut'),
        'date_end': fields.date(u'Date fin'),  
        'contrat_ids': fields.one2many('sfp.contrat','groupe',u'Contrats'), 
        'description': fields.text(u'Description', translate=True),
    }
    
