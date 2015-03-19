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
from openerp.osv import orm, fields, osv
from openerp import tools
from openerp.tools.translate import _
import time
import openerp
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
    
    
    def _get_nbr_month(self, cr, uid, ids, name, arg, context={}):
        data={}
        for object_parent in self.browse(cr,uid,ids):
            data[object_parent.id] = 0
            if object_parent.date_abandon:
                data[object_parent.id]=(datetime.strptime(object_parent.date_abandon,"%Y-%m-%d")-datetime.strptime(object_parent.date_start,"%Y-%m-%d")).days/30
        return data
    
    def _get_age1(self, cr, uid, ids, name, arg, context={}):
        data={}
        for object_parent in self.browse(cr,uid,ids):
            data[object_parent.id] = 0
            if object_parent.apprenti and object_parent.groupe:
                data[object_parent.id]=(datetime.strptime(object_parent.groupe.date_prevu,"%Y-%m-%d")-datetime.strptime(object_parent.apprenti.birthdate_1,"%Y-%m-%d")).days/356
                print data,
        return data
    

    
    def action_processing(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state' : 'processing'})
    
    def action_reject(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state' : 'reject'})
    
    def action_year1(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state' : 'year1'})
    
    def action_year2(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state' : 'year2'})
    
    def action_laureat(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state' : 'laureat'})
    
    def action_abandoned(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state' : 'abandon'})
    
    def action_changed(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state' : 'changed'})
  
    
    _columns = {
        'name': fields.char(u'Numéro', required=True),        
        'declaration': fields.boolean(u'Déclaration'),
        'parent_link': fields.many2one('titre.titre',u'الصــــــفة'),
        'date_start': fields.date(u'Date début de formation'),
        'age' : fields.function(_get_age1,type='integer',string=u'Age admission'),
        'date_end': fields.date(u"Date fin de formation"), 
        'date_abandon': fields.date(u"Date abandon"), 
        'nbr_function': fields.function(_get_nbr_month,type='integer',string=u'Nbr de mois a complis'),
        'motif_abandan': fields.text(u'Motif d\'abandon'),
        'apprenti': fields.many2one('sfp.apprenti',u'Apprenti'),  
        'groupe': fields.many2one('sfp.groupe',u'Groupe'),
        'metier': fields.many2one('sfp.metier',u'الحـــرفة'),
        'duree': fields.integer(u'Periode de contrat'),
        'responsable': fields.many2one('res.partner',u'Tuteur'),
        'user': fields.many2one('res.users',u'Utilisateur'),
        'entreprise': fields.many2one('res.partner',u'Entreprise', domain=[('is_company','=',True)]),
        'maitre': fields.many2one('res.partner',u'Maître'),
        'maitre_descri' : fields.selection([('m1',u'مؤطــــــــــــــر'),('m2',u'مســاعد'),('m3',u'صاحب مقاولة')],u'بصفــته'),
        'chef': fields.many2one('res.partner',u'Chef d\'entreprise'),
        'allocation': fields.float(u'Allocation'),
        'trial': fields.integer(u'Période essai'),
        'periode_company': fields.integer(u'Période entreprise'),
        'periode_cfa': fields.integer(u'Période CQP'),
        'average': fields.float(u'Moyenne'),
        'periode_work': fields.integer(u'Période Travail'),
        'nbr_inscrit': fields.integer(u'عدد المتدرجين'),
        'maitre_titre': fields.many2one('titre.titre',u'الصـــــفة'),
        
        'cfa': fields.many2one('sfp.cfa',u'CQP'),
        'province': fields.many2one('sfp.province',u'Province',domain="[('cfa','=',cfa)]"),
        'annexe': fields.many2one('sfp.annexe',u'Annexe',domain="[('cfa','=',cfa)]"),
        'vacataire': fields.many2one('res.partner',u'Vacataire',domain=[('vacataire_ok','=',True)]),
        'nbr_visite' : fields.char(u'Nombre de visites'),
        'description': fields.text(u'Description'),
        'invoice_ids': fields.one2many('account.invoice','contrat_id',u'Les Factures'),
        
        'age': fields.integer(u'Age d\'apprenti'),
        'age_maitre': fields.integer(u'Age maitre'),
        #'state': fields.selection(AVAILABLE_PRIORITIES, 'Etat', select=True),
        
        'period1': fields.integer(u'Période 1'),
        'period2': fields.integer(u'Période 2'),
        'period3': fields.integer(u'Période 3'),
        'period4': fields.integer(u'Période 4'),
        'total_period': fields.integer(u'Total de mois réalisés'),
        'amount': fields.float(u'Montant alloué'),
        
        'state' : fields.selection([('processing',u'En Traitement'),('reject',u'Réfusé'),('year1',u'1ère Année'),('year2',u'2ème Année'),('laureat',u'Lauréat'),('abandon',u'Abandonnée'),('changed',u'Changé')],u'Etat',required=True),
   
    }
    
    _sql_constraints = [
        ('sfp_contrat_model_uniq', 'unique (name)', u'Le numero de contrat doit être unique'),
    ]
        
    _defaults = {  
        'state': lambda *a: 'processing',
        'user' : lambda x, y, z, c: z,
        'name': lambda self, cr, uid, context: '/',
        'date_start': lambda *a : time.strftime('%Y-%m-%d'),
        }
    
    def onchange_period(self,cr,uid,ids,period1,period2,period3,period4,context={}):
        data={}  
        if period1 or period2 or period3 or period4: 
            if  period1 or period2 or period3 or period4:
                a = period1
                b = period2
                c = period3
                d = period4
                c = a + b + c + d
                data['total_period'] = c
                data['amount'] = c*250
            else :
                raise osv.except_osv(u'Attention', u'Période non valide')
        return {'value' : data }
    
  
    def onchange_apprenti(self,cr,uid,ids,groupe,apprenti,context={}):
        data={}
        object_groupe=self.pool.get('sfp.groupe').browse(cr,uid,groupe)  
        object_apprenti=self.pool.get('sfp.apprenti').browse(cr,uid,apprenti) 
        if apprenti: 
            if  object_apprenti.birthdate_1:
                if object_groupe.date_prevu:
                    data['age'] = (datetime.strptime(object_groupe.date_prevu,"%Y-%m-%d")- datetime.strptime(object_apprenti.birthdate_1,"%Y-%m-%d")).days/356
                else :
                    raise osv.except_osv(u'Attention', u'La date de groupe est non spécifié')
            else :
                raise osv.except_osv(u'Attention', u'La date de l\'apprenti est non spécifié')
        return {'value' : data }
        
    
    def onchange_metier(self,cr,uid,ids,groupe,apprenti,metier,context={}):
        data={}
        if metier:
            object_groupe=self.pool.get('sfp.groupe').browse(cr,uid,groupe)  
            object_apprenti=self.pool.get('sfp.apprenti').browse(cr,uid,apprenti) 
            object_metier=self.pool.get('sfp.metier').browse(cr,uid,metier)
            #object_app=self.browse(cr,uid,age)
            if object_metier.duree:
                data['duree'] = object_metier.duree  or False 
                if  object_apprenti.birthdate_1 and object_groupe.date_prevu:
                    raise osv.except_osv(u'Attention', u'l\'Age de l\'apprenti doit etre superieur ou égale a 15 et inferieur ou égale a 30')
                    """ a=data['age'] = (datetime.strptime(object_groupe.date_prevu,"%Y-%m-%d")- datetime.strptime(object_apprenti.birthdate_1,"%Y-%m-%d")).days/356
                    if a <= 30 and a >= 15:
                        data['condition1'] = True
                    else :
                        raise osv.except_osv(u'Attention', u'Age de metier et superieur a l\'age de l\'apprenti')"""
                else :
                    raise osv.except_osv(u'Attention', u'Date de l\'apprenti ou date previsionnelle de groupe est non specifier')
            else :
                raise osv.except_osv(u'Attention', u'La durée du metier est non spécifié')
        return {'value' : data }
     
    def onchange_maitre(self,cr,uid,ids,maitre,context={}):
        data={}
        #object_groupe=self.pool.get('sfp.groupe').browse(cr,uid,groupe)
        object_maitre=self.pool.get('res.partner').browse(cr,uid,maitre)
        if maitre:
            if object_maitre.birthdate_1:
               # a = datetime.strptime(object_groupe.date_prevu,"%Y-%m-%d")
                a =(datetime.now())
                b = datetime.strptime(object_maitre.birthdate_1,"%Y-%m-%d")
                c = (a - b).days/356
                data['age_maitre']= c
                if c >= 20 :
                    pass
                else :
                    raise osv.except_osv(u'Attention ', u'L\'age de Maitre doit etre superieur ou egale a 20 ans')
        return {'value' : data }
    
    def onchange_chef(self,cr,uid,ids,chef,context={}):
        data={}
        #object_groupe=self.pool.get('sfp.groupe').browse(cr,uid,groupe)
        object_chef=self.pool.get('res.partner').browse(cr,uid,chef)
        if chef:
            if object_chef.birthdate_1:
               # a = datetime.strptime(object_groupe.date_prevu,"%Y-%m-%d")
                a =(datetime.now())
                b = datetime.strptime(object_chef.birthdate_1,"%Y-%m-%d")
                c = (a - b).days/356
                data['chef']= c
                if c >= 20 :
                    pass
                else :
                    raise osv.except_osv(u'Attention ', u'L\'age de Chef d\'entreprise doit etre superieur ou egale a 20 ans')
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
    
    def _count_all(self, cr, uid, ids, field_name, arg, context=None):
        Logintervention = self.pool['sfp.contrat']
        return {
            apprenti: {
                'contrat_count': Logintervention.search_count(cr, uid, [('apprenti', '=', apprenti)], context=context),        
            }
            for apprenti in ids
        }
        
        
    def return_action_to_open(self, cr, uid, ids, context=None):
        """ This opens the xml view specified in xml_id for the current machine """
        if context is None:
            context = {}
        if context.get('xml_id'):
            res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid ,'sifa', context['xml_id'], context=context)
            res['context'] = context
            res['context'].update({'default_apprenti': ids[0]})
            res['domain'] = [('apprenti','=', ids[0])]
            return res
        return False
    
    
 
    _columns = {
            'name': fields.char(u'Nom', required=True, select=True),
            'name_arabic' : fields.char(u'الإسم '),
            'birthdate_1': fields.date(u'Date de Naissance'),
            'lieu_birth' : fields.many2one('birth.place',u'Lieu de naissance'),
            'lieu_birth_ar' : fields.many2one('birth.place',u'مكـــان الازدياد'),
            'age' : fields.function(_get_age,type='integer',string=u'Age'),
            'cin' : fields.char(u'CIN',size=50),
            'gender_' : fields.char(u'Sexe'), 
            'gender_ar' : fields.selection([('male',u'دكـــــــر'),('female',u'انــــــثى')],u'الجنــــــس'), 
            'image': fields.binary(u"Image",help="This field holds the image used as avatar for this contact, limited to 1024x1024px"),   
            'street': fields.char(u'Adresse'),
            'street2': fields.char(u'العـــنوان'),
            'zip': fields.char(u'Code Postal', size=24, change_default=True),
            'city': fields.char(u'Ville'),
            'city_ar': fields.char(u'المـــــدينة'),
            'state_id': fields.many2one("res.country.state", 'State', ondelete='restrict'),
            'country_id': fields.many2one('res.country', u'Pays', ondelete='restrict'),
            'email': fields.char(u'Email'),
            'phone': fields.char(u'Tél 1'),
            'mobile': fields.char(u'Tél 2'),
            'website': fields.char(u'Site Web', help="Website of Partner or Company"),   
            'nv_scolaire' : fields.many2one('school.level',u'المستوى الدراسي',size=50),
            'dure_formation' : fields.char(u'Dure de formation',size=50),
            'user': fields.many2one('res.users',u'Utilisateur'),
            'profession_tuteur_ar' : fields.char(u'مهنة الاب او ولي الامر ',size=50),
            'situation_ar' : fields.many2one('apprenti.situation',u'الوضعية قبل الانخراط',size=50),
            'contrat_ids': fields.one2many('sfp.contrat','apprenti',u'Les contrats'),
            'description': fields.text(u'Observation', translate=True),
            'contrat_count': fields.function(_count_all, type='integer', string='Contrats', multi=True),
            }
    
    def _get_photo(self, cr, uid, context=None):
        photo_path = openerp.modules.get_module_resource('sifa','images','apprenti.png')
        return open(photo_path, 'rb').read().encode('base64')
    
    _defaults = {
        'image' : _get_photo,
        }
        

    
    def onchange_field1(self, cr, uid, ids, gender_ar, gender_, context=None):
        if gender_ar=='male':
            v = {'gender_': 'Masculin'}
            return {'value': v}
        elif gender_ar=='female':
            v = {'gender_': 'Féminin'}
            return {'value': v}
        return {}


class school_level(orm.Model):
    _name = 'school.level'
    _columns = {
        'name': fields.char(u'Niveau', required=True),
        'name_ar': fields.char(u'الاســـــم', translate=True),
        'code': fields.char(u'Code', translate=True),
        'description': fields.text(u'Description', translate=True),
   
    }
        
class sfp_matier(orm.Model):
    _name = 'sfp.matier'
    _columns = {
        'name': fields.char(u'Matière', required=True),
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
        'name_ar': fields.char(u'الاســــم'),
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
    
    
class sfp_metier(orm.Model):
    _name = 'sfp.metier'
    _columns = {
        'name': fields.char(u'Métier', required=True),
        'name_ar': fields.char(u'الحـــرفة'),
        'qualification': fields.char(u'Métier et Qualification'),
        'qualification_ar': fields.char(u'الحرفة و التأهيل'),
        'code': fields.char(u'Code', translate=True),      
        'duree': fields.char(u'Durée de formation',required=True),
        'level': fields.many2one('sfp.level', u'Niveau de formation'),
        'sector': fields.many2one('sfp.sector', u'Secteur'),
        'description': fields.text(u'Description'),
        'sect_id': fields.many2one('sfp.sectortraining', u'Secteur de formation'),
        'admission_id': fields.many2one('admission.level', u'Niveau admission'),
    }
    
    _defaults = {  
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
        'name': fields.char(u'Niveau', required=True),
        'code': fields.char(u'Code', translate=True),    
        'description': fields.text(u'Description', translate=True),  
        'admission_id': fields.many2one('sfp.metier', u'Admission'),   
    }

class sfp_annexe(orm.Model):
    _name = 'sfp.annexe'
    _columns = {
        'name': fields.char(u'Nom', required=True),
        'name_ar' : fields.char(u'الإسم '), 
        'code': fields.char(u'Code', translate=True),
        'description': fields.text(u'Description', translate=True),    
        'cfa': fields.many2one('sfp.cfa',u'CQP'),
    }


class sfp_province(orm.Model):
    _name = 'sfp.province'
    _columns = {
        'name': fields.char(u'Nom', required=True),
        'name_ar' : fields.char(u'الإسم '), 
        'code': fields.char(u'Code', translate=True),
        'description': fields.text(u'Description', translate=True),
        'cfa': fields.many2one('sfp.cfa',u'CQP'),
    }

class sfp_cfa(orm.Model):
    _name = 'sfp.cfa'
    _columns = {
        'name': fields.char(u'Nom', required=True),    
        'name_ar' : fields.char(u'الإسم '),    
        'code': fields.char(u'Code', translate=True),
        'provinces': fields.char(u'Provinces', translate=True),
        'province_ids': fields.one2many('sfp.province','cfa',u'Provinces'),  
        'annexe_ids': fields.one2many('sfp.annexe','cfa',u'Annexes'), 
        'description': fields.text(u'Description', translate=True),
    }


class sfp_groupe(orm.Model):
    _name = 'sfp.groupe'
    
    def action_processing(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state' : 'processing'})
    
    def action_year1(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state' : 'year1'})
    
    def action_year2(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state' : 'year2'})
    
    def action_done(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state' : 'done'})
    
    
    
    _columns = {
        'name': fields.char(u'Nom', required=True),        
        'code': fields.char(u'Code', translate=True),
        'date_start': fields.date(u'Date debut'),
        'year': fields.char(u'Année'),
        'date_prevu': fields.date(u'Date previsionnel'),
        'date_end': fields.date(u'Date fin'),  
        'contrat_ids': fields.one2many('sfp.contrat','groupe',u'Contrats'), 
        'description': fields.text(u'Description', translate=True),
        'state' : fields.selection([('processing',u'En Preparation'),('year1',u'1ere Année'),('year2',u'2eme Année'),('done',u'Terminé')],u'Etat',required=True),
    }
    
    _defaults = {  
        'state': lambda *a: 'processing',
        'date_start': lambda *a : time.strftime('%Y-%m-%d'),
        }
class apprenti_situation(orm.Model):
    _name = 'apprenti.situation'
    _columns = {
        'name': fields.char(u'Situation', required=True),
        'name_ar': fields.char(u'وضعية', translate=True),
        'description': fields.text(u'Description', translate=True),
    }
