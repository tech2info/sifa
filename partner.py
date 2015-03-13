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
from openerp.osv import orm, fields, osv
from openerp.tools.translate import _
import time
from datetime import date
from datetime import datetime
from openerp import addons

class res_partner(orm.Model):
    
    _name='res.partner'
    _inherit = 'res.partner' 
       
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
            entreprise: {
                'contrat_count': Logintervention.search_count(cr, uid, [('entreprise', '=', entreprise)], context=context),        
            }
            for entreprise in ids
        }
            
        
    def return_action_to_open(self, cr, uid, ids, context=None):
        """ This opens the xml view specified in xml_id for the current machine """
        if context is None:
            context = {}
        if context.get('xml_id'):
            res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid ,'sifa', context['xml_id'], context=context)
            res['context'] = context
            res['context'].update({'default_entreprise': ids[0]})
            res['domain'] = [('entreprise','=', ids[0])]
            return res
        return False
    
    
    def _count_vac(self, cr, uid, ids, field_name, arg, context=None):
        Loginterventio = self.pool['sfp.contrat']
        return {
            vacataire: {
                'contrat_count_vac': Loginterventio.search_count(cr, uid, [('vacataire', '=', vacataire)], context=context),        
            }
            for vacataire in ids
        }
        
    def return_action_to_open_vac(self, cr, uid, ids, context=None):
        """ This opens the xml view specified in xml_id for the current machine """
        if context is None:
            context = {}
        if context.get('xml_id'):
            res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid ,'sifa', context['xml_id'], context=context)
            res['context'] = context
            res['context'].update({'default_vacataire': ids[0]})
            res['domain'] = [('vacataire','=', ids[0])]
            return res
        return False
    
    def _count_all_tut(self, cr, uid, ids, field_name, arg, context=None):
        Logintervention = self.pool['sfp.contrat']
        return {
            responsable: {
                'contrat_count_tut': Logintervention.search_count(cr, uid, [('responsable', '=', responsable)], context=context),        
            }
            for responsable in ids
        }
        
    def return_action_to_open_tut(self, cr, uid, ids, context=None):
        """ This opens the xml view specified in xml_id for the current machine """
        if context is None:
            context = {}
        if context.get('xml_id'):
            res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid ,'sifa', context['xml_id'], context=context)
            res['context'] = context
            res['context'].update({'default_responsable': ids[0]})
            res['domain'] = [('responsable','=', ids[0])]
            return res
        return False
    
  
    _columns = {
            'name_arabic' : fields.char(u'الإسم '),
            'company_name_arabic' : fields.char(u'اسم المقاولة '),
            'form' : fields.many2one('commerial.system',u'النظام التجاري  '),
            'lieu_birth_ar' : fields.many2one('birth.place',u'مكـــان الازدياد'),
            'birthdate_1': fields.date(u'Date de Naissance'),
            'lieu_birth' : fields.many2one('birth.place',u'Lieu de naissance'),

            'contrat_count': fields.function(_count_all, type='integer', string='Contrats-entre', multi=True),
            'contrat_count_vac': fields.function(_count_vac, type='integer', string='Contrats-vac', multi=True),
            'contrat_count_tut': fields.function(_count_all_tut, type='integer', string='Contrats-tut', multi=True),
            'age' : fields.char(u'âge'),
            'cin' : fields.char(u'CIN',size=50),
            'street_ar' : fields.char(u'العــنوان'),
            'experience' :fields.many2one('sfp.metier', u'Metier'),
            'metier' :fields.many2one('sfp.metier', u'Metier'),
            'parental_ar' : fields.char(u'القرابة العائلية'),
            'province' :fields.many2one('sfp.province', u'Province d\'implantation'),
            'taxe_pro' : fields.char(u'Taxe professionnel'),
            'name_entreprise' : fields.char(u'اسم المقاولة'),
            'activities' : fields.many2one('company.activities',u'ميدان أو ميادين عملها'),
            'resp_entreprise' : fields.char(u'بصفته: صاحب المقاولة'),     
            'nbr_mois' : fields.char(u'Nombre de mois accompli'),
            'montant_percu' : fields.char(u'Montant Percu'),
            'patente' : fields.char(u'Taxe professionnelle'),
            'payment_mode' : fields.char(u'Mode de payement'),
            'employe_nbr' : fields.integer(u'عدد العاملين بها'),
            'gender_' : fields.char(u'Sexe'), 
            'gender_ar' : fields.selection([('male',u'دكر'),('female',u'انتى')],u'الجنس'), 
            'groupe' : fields.many2one('sfp.groupe', u'Groupe'),
            'cfa' :fields.many2one('sfp.groupe', u'CFA'),
            'contrat_ids' :fields.one2many('sfp.contrat','vacataire', u'Contrat'),
            
            'contrat_ids_company' :fields.one2many('sfp.contrat','entreprise', u'Contrat'),
            'contrat_ids_maitre' :fields.one2many('sfp.contrat','maitre', u'Contrat'),
            'contrat_ids_chef' :fields.one2many('sfp.contrat','chef', u'Contrat'),

            'vacataire_ok': fields.boolean('Vacataire'),
            'is_mono': fields.boolean('Mono'),
            'is_tuteur': fields.boolean('Tuteur'),
            'customer': fields.boolean('Is a Customer', help="Check this box if this contact is a customer."),
            #tuteur
            'titre': fields.many2one('titre.titre',u'الصــــــفة'),
            'profession_ar': fields.char(u'المهنة'),        
            #vacataire
            'vac_year' : fields.char(u'Année de vacation'),
            'maitre_ids' :fields.one2many('sfp.maitre','maitre', u'Maitre'),
            'is_company': fields.boolean('Is a Company', domain=[('is_company','=',True)]),
            'price' : fields.char(u'Taux horaire '),   
            'masse_horaire' : fields.char(u'Masse horaire'),
            'grade': fields.many2one('sfp.grade',u'Grade'), 
            'matiere': fields.many2one('sfp.matier',u'Matières'), 
            


            }

    
    _defaults = {
         'customer': False,
         'supplier': True, 
         
            }
    
    def onchange_birthdate(self,cr,uid,ids,birthdate_1,context={}):
        data={}  
        if birthdate_1: 
            if  birthdate_1 :
                a =(datetime.now())
                b = datetime.strptime(birthdate_1,"%Y-%m-%d")
                c = (a - b).days/356
                print c
                data['age'] = str(c) 
            else :
                raise osv.except_osv(u'Attention', u'La date de naissance non spécifié')
        return {'value' : data }
    
    
    def onchange_field1(self, cr, uid, ids, gender_ar, gender_, context=None):
        if gender_ar=='male':
            v = {'gender_': 'Masculin'}
            return {'value': v}
        elif gender_ar=='female':
            v = {'gender_': 'Féminin'}
            return {'value': v}
        return {}


    def onchange_grade(self,cr,uid,ids,grade,context={}):
        data={}
        if grade:
            object_grade=self.pool.get('sfp.grade').browse(cr,uid,grade)
            if object_grade:
                data['price'] = object_grade.price_h or False
        return {'value' : data }
    
    
class titre_titre(orm.Model):
    _name = 'titre.titre'
    _columns = {
        'name': fields.char(u'Nom', required=True),
        'code': fields.char(u'Code', translate=True),
        'description': fields.text(u'Description', translate=True),
   
    }
    
class comm_system(orm.Model):
    _name = 'commerial.system'
    _columns = {
        'name': fields.char(u'Nom', required=True),
        'code': fields.char(u'Code', translate=True),
        'description': fields.text(u'Description', translate=True),
   
    }
    
class company_activities(orm.Model):
    _name = 'company.activities'
    _columns = {
        'name': fields.char(u'Nom', required=True),
        'code': fields.char(u'Code'),
        'name_ar': fields.char(u'الاســـــم',required=True, translate=True),
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