# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
##############################################################################
from openerp.osv import osv,fields
from openerp.tools.translate import _
import time
from datetime import date

class sfp_apprenti(osv.osv):
    
    _name='sfp.apprenti'
    _inherit = 'res.partner' 
       
    def _get_age(self, cr, uid, ids, name, arg, context={}):
        data={}
        for object_parent in self.browse(cr,uid,ids):
            data[object_parent.id] = 0
            today = date.today()
            if object_parent.birthdate:
                date_birth=time.strptime(object_parent.birthdate, '%Y-%m-%d')
                data[object_parent.id]=today.year-date_birth.tm_year
        return data
    
    def _get_name(self,cr,uid,ids,name,args,context={}):
        data = {}
        for data_read in self.read(cr,uid,ids,['name','first_name','title']):
           if data_read['first_name']:
                data['first_name'] =True
                data[data_read['id']] = u"%s %s %s" %(data_read['title'] and ('%s ' %data_read['title'][1]) or '',data_read['name'],data_read['first_name'])
           else:  
                data[data_read['id']] = u"%s %s" %(data_read['title'] and ('%s ' %data_read['title'][1]) or '',data_read['name'])
        return data
    
    _columns = {
            'first_name' : fields.char(u'Prénom',size=50),
            'nv_scolaire' : fields.char(u'Niveau scolaire',size=50),
            'dure_formation' : fields.char(u'Dure de formation',size=50),
            'date_start' : fields.datetime(u'Date debut',size=50),
            'date_end' : fields.datetime(u'Date fin',size=50),
            'diplom' : fields.char(u'Diplom',size=50),
            'en_formation': fields.boolean('En formation'),
            'abandon': fields.boolean('Abandon'),
            'date_abandon' : fields.datetime(u'Date Abandon',size=50),
            'laureat': fields.boolean('Laureat'),
            'lieu_birth' : fields.char(u'lieu de naissance',size=50),
            
            'name_arabic' : fields.char(u'الإسم العائلي',size=50),
            'first_name_arabic' : fields.char(u'الإسم الشخصي',size=50),
            'function_ar' : fields.char(u'الحرفة',size=50),
            'parental_ar' : fields.char(u'القرابة العائلية',size=50),
            'adresse_ar' : fields.char(u'عنوان السكى',size=50),
            'dure_ar' : fields.char(u'مدة التكوين',size=50),
            'profession_tuteur_ar' : fields.char(u'مهة الاب',size=50),
            'situation_ar' : fields.char(u'الوضعية قبل الانخراط',size=50),
            'gender' : fields.selection([('male',u'Masculin'),('female',u'Féminin')],u'Sexe',required=True), 
            'cin' : fields.char(u'CIN',size=50),
            'groupe' : fields.many2one('sfp.groupe', u'Groupe'),
            'cfa' :fields.many2one('sfp.groupe', u'CFA'),
            'contrat' :fields.many2one('sfp.groupe', u'Contrat'),
            'province' :fields.many2one('sfp.province', u'Province'),
            'age' : fields.function(_get_age,type='integer',string=u'âge'),
            'all_name' : fields.function(_get_name,type='char',string=u'Nom complet'),
            }
    
    _defaults = {
        
        }
    
    
class sfp_tuteur(osv.osv):
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
    

class sfp_maitre(osv.osv):
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
    
    
class sfp_vacataire(osv.osv):
    
    _name='sfp.vacataire'
    _inherit = 'res.partner' 


    def _get_name(self,cr,uid,ids,name,args,context={}):
        data = {}
        for data_read in self.read(cr,uid,ids,['name','first_name','title']):
           if data_read['first_name']:
                data['first_name'] =True
                data[data_read['id']] = u"%s %s %s" %(data_read['title'] and ('%s ' %data_read['title'][1]) or '',data_read['name'],data_read['first_name'])
           else:  
                data[data_read['id']] = u"%s %s" %(data_read['title'] and ('%s ' %data_read['title'][1]) or '',data_read['name'])
        return data
    
    
    _columns = {
            'first_name' : fields.char(u'Prénom'),
            'vac_year' : fields.char(u'Année de vacation'),
            'nbr_visite' : fields.char(u'Nombre de visites'),
            'masse_horaire' : fields.char(u'Masse horaire'),
            'lieu_birth' : fields.char(u'lieu de naissance'),
            'cin' : fields.char(u'CIN'),
            'gender' : fields.selection([('male',u'Masculin'),('female',u'Féminin')],u'Sexe',required=True), 
            'contrat' : fields.many2one('sfp.groupe',u'N contrat',size=50),
            'cfa' : fields.many2one('sfp.cfa',u'CFA',size=50),
            'groupe' : fields.many2one('sfp.groupe',u'Groupe',size=50),
            'grade_ids': fields.many2many('sfp.grade','sfp_grade_rel','vacataire_id','grade_id',u'Grades'), 
            'matier_ids': fields.many2many('sfp.matier','sfp_matier_rel','vacataire_id','matier_id',u'Matières'), 
            'description' :fields.text(u'Description'),
            'all_name' : fields.function(_get_name,type='char',string=u'Nom complet'),

            }
    
    _defaults = {
        
        }
    
class res_partner(osv.osv):
    
    _name='res.partner'
    _inherit = 'res.partner' 
       
    def _get_age(self, cr, uid, ids, name, arg, context={}):
        data={}
        for object_parent in self.browse(cr,uid,ids):
            data[object_parent.id] = 0
            today = date.today()
            if object_parent.birthdate:
                date_birth=time.strptime(object_parent.birthdate, '%Y-%m-%d')
                data[object_parent.id]=today.year-date_birth.tm_year
        return data
    
    def _get_name(self,cr,uid,ids,name,args,context={}):
        data = {}
        for data_read in self.read(cr,uid,ids,['name','first_name','title']):
           if data_read['first_name']:
                data['first_name'] =True
                data[data_read['id']] = u"%s %s %s" %(data_read['title'] and ('%s ' %data_read['title'][1]) or '',data_read['name'],data_read['first_name'])
           else:  
                data[data_read['id']] = u"%s %s" %(data_read['title'] and ('%s ' %data_read['title'][1]) or '',data_read['name'])
        return data
    
    _columns = {
            'first_name' : fields.char(u'Prénom'),
            'name_arabic' : fields.char(u'الإسم '),
            'first_name_arabic' : fields.char(u'السب'),
            'lieu_birth' : fields.char(u'lieu de naissance'),
            'age' : fields.function(_get_age,type='integer',string=u'âge'),
            'cin' : fields.char(u'CIN',size=50),
            'experience' :fields.many2one('sfp.metier', u'Metier'),
            'metier' :fields.many2one('sfp.metier', u'Metier'),
            'parental_ar' : fields.char(u'القرابة العائلية'),
            'province' :fields.many2one('sfp.province', u'Province'),
            'taxe_pro' : fields.char(u'Taxe professionnel'),
            'name_entreprise' : fields.char(u'اسم المقاولة'),
            'domaine_travail' : fields.char(u'ميدان أو ميادين عمله'),
            'function_ar' : fields.char(u'الحرفة',size=50),
            'resp_entreprise' : fields.char(u'بصفته: صاحب المقاولة'),    
            'activities' : fields.char(u' الصناعة التقليدية بالعالم القروي'), 
            'ahbas' : fields.char(u'ممتلكات الأحباس'),  
            'ensemble_indis' : fields.char(u'مجمع الصناعة التقليدية',size=50),
            'ensemble_ennex' : fields.char(u'الجماعات و الاحياء المستهدفة'),
            'nbr_mois' : fields.char(u'Nombre de mois accompli'),
            'montant_percu' : fields.char(u'Montant Percu'),
            'payment_mode' : fields.char(u'Mode de payement'),
            'employe_nbr' : fields.char(u'عدد العاملين بها'),
            'inscription_nbr' : fields.char(u'عدد المتدرجين بها'),
            'gender' : fields.selection([('male',u'Masculin'),('female',u'Féminin')],u'Sexe',required=True), 
            'groupe' : fields.many2one('sfp.groupe', u'Groupe'),
            'cfa' :fields.many2one('sfp.groupe', u'CFA'),
            'contrat' :fields.many2one('sfp.groupe', u'Contrat'),
            'all_name' : fields.function(_get_name,type='char',string=u'Nom complet'),
            }
    
    _defaults = {
        
        }