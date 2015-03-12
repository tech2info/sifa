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


class admn_certificate(orm.Model):
    _name = 'admin.certificate'
    
    def create(self, cr, user, vals, context=None):
        u"""méthode créer"""
        if ('name' not in vals) or (vals.get('name')=='/'):
            vals['name'] = self.pool.get('ir.sequence').get(cr, user, 'admin.certificate')
        return super(admn_certificate, self).create(cr, user, vals, context) 
    
    def action_print(self,cr,uid,ids,context={}):
        if context is None:
            context = {}
        datas = {'ids': context.get('active_ids', [])}
        res = self.read(cr, uid, ids, ['id'], context=context)
        res = res and res[0] or {}
        datas['form'] = res
        if res.get('id',False):
            datas['ids']=[res['id']]
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'sifa.report_admin_certificate',
            'datas': datas,
        }
        
    _columns = {
        'name': fields.char(u'Numero', required=True),
        'partner': fields.many2one('res.partner',u'Nom'),   
        'adresse': fields.char(u'العنــــوان'),
        'cin': fields.char(u'CIN'),
        'birth_date': fields.char(u'Date de naissance'), 
        'date': fields.date(u'Date création'),
        'metier': fields.many2one('sfp.metier',u'حـــــرفة'),  
        'locale' : fields.selection([('local1',u'العالــم القروي'),('local2',u'ممتلكات الأحبــاس'),('local3',u'مجمع الصناعة التقليدية'),('local4',u'الأحياء والجماعات المستهدفـة')],u'مكان النشاط',required=True),
        'description': fields.text(u'Description'),     
    }
    
    _defaults = {  
        'name': lambda self, cr, uid, context: '/',
        'date': lambda *a : time.strftime('%Y-%m-%d'),
        }
    
    _sql_constraints = [
        ('admn_certificate_model_uniq', 'unique (name)', u'Le numero de l\'attestation administratif doit être unique'),
    ]
    
    def onchange_partner(self,cr,uid,ids,partner,context={}):
        data={}
        if partner:
            object_partner=self.pool.get('res.partner').browse(cr,uid,partner)
            if object_partner:
                data['birth_date'] = object_partner.birthdate_1  or False
                data['cin'] = object_partner.cin  or False
                data['adresse'] = object_partner.street  or False
        return {'value' : data }
    
    
class apprenti_certif(orm.Model):
    _name = 'apprenti.certif'
    
    def create(self, cr, user, vals, context=None):
        u"""méthode créer"""
        if ('name' not in vals) or (vals.get('name')=='/'):
            vals['name'] = self.pool.get('ir.sequence').get(cr, user, 'apprenti.certif')
        return super(apprenti_certif, self).create(cr, user, vals, context) 
    
    def action_print(self,cr,uid,ids,context={}):
        if context is None:
            context = {}
        datas = {'ids': context.get('active_ids', [])}
        res = self.read(cr, uid, ids, ['id'], context=context)
        res = res and res[0] or {}
        datas['form'] = res
        if res.get('id',False):
            datas['ids']=[res['id']]
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'sifa.report_apprenti_certificate',
            'datas': datas,
        }
    
        
    _columns = {
        'name': fields.char(u'Numero', required=True),
        'contract': fields.many2one('sfp.contrat',u'Contrat'),    
        'date': fields.date(u'Date signature'),  
        'birth_day': fields.char(u'Date de naissance'),
        'birth_place': fields.char(u'مكان الازدياد'),
        'date_end': fields.char(u'Date Lauréat'),
        'full_name': fields.char(u'اســـم المتدرج'),
        'cin': fields.char(u'CIN'),
        'cfa': fields.char(u'CQP'),
        'metier': fields.char(u'حـــــرفة', translate=True),  
        'branche': fields.char(u'شعــــبة', translate=True),
        'date': fields.date(u'Date creation'),
        'adresse': fields.char(u'العنــوان'),
        'description': fields.text(u'Description'),     
    }
    
    _defaults = {  
        'name': lambda self, cr, uid, context: '/',
        'date': lambda *a : time.strftime('%Y-%m-%d'),
        }
    
    _sql_constraints = [
        ('apprenti_certif_model_uniq', 'unique (name)', u'Le numero de l\'attestation administratif doit être unique'),
    ]
    
    def onchange_contract(self,cr,uid,ids,contract,context={}):
        data={}
        if contract:
            object_contrat=self.pool.get('sfp.contrat').browse(cr,uid,contract)
            if object_contrat:
                data['birth_day'] = object_contrat.apprenti.birthdate_1  or False
                data['birth_place'] = object_contrat.apprenti.lieu_birth.name_ar  or False
                data['cin'] = object_contrat.apprenti.cin  or False
                data['full_name'] = object_contrat.apprenti.name_arabic  or False
                data['metier'] = object_contrat.metier.name_ar  or False
                data['date_end'] = object_contrat.date_end  or False
                data['adresse'] = object_contrat.apprenti.street  or False
                data['cfa'] = object_contrat.cfa.name_ar  or False
                data['branche'] = object_contrat.metier.sect_id.name_ar  or False
                
        return {'value' : data }
    
class spesialized_apprenti_certif(orm.Model):
    _name = 'specialized.apprenti.certif'
    
    def create(self, cr, user, vals, context=None):
        u"""méthode créer"""
        if ('name' not in vals) or (vals.get('name')=='/'):
            vals['name'] = self.pool.get('ir.sequence').get(cr, user, 'specialized.apprenti.certif')
        return super(spesialized_apprenti_certif, self).create(cr, user, vals, context) 
    
    def action_print(self,cr,uid,ids,context={}):
        if context is None:
            context = {}
        datas = {'ids': context.get('active_ids', [])}
        res = self.read(cr, uid, ids, ['id'], context=context)
        res = res and res[0] or {}
        datas['form'] = res
        if res.get('id',False):
            datas['ids']=[res['id']]
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'sifa.report_specialized_certificate',
            'datas': datas,
        }
    
        
    _columns = {
        'name': fields.char(u'Numero', required=True),
        'contract': fields.many2one('sfp.contrat',u'Contrat'),    
        'date': fields.date(u'Date signature'),  
        'birth_day': fields.char(u'Date de naissance'),
        'birth_place': fields.char(u'مكان الازدياد'),
        'date_end': fields.char(u'Date Lauréat'),
        'full_name': fields.char(u'اســـم المتدرج'),
        'cin': fields.char(u'CIN'),
        'cfa': fields.char(u'CQP'),
        'metier': fields.char(u'حـــــرفة', translate=True),  
        'branche': fields.char(u'شعــــبة', translate=True),
        'date': fields.date(u'Date creation'),
        'adresse': fields.char(u'العنــوان'),
        'description': fields.text(u'Description'),     
    }
    
    _defaults = {  
        'name': lambda self, cr, uid, context: '/',
        'date': lambda *a : time.strftime('%Y-%m-%d'),
        }
    
    _sql_constraints = [
        ('specialized_apprenti_certif_model_uniq', 'unique (name)', u'Le numero de l\'attestation administratif doit être unique'),
    ]
    
    def onchange_contract(self,cr,uid,ids,contract,context={}):
        data={}
        if contract:
            object_contrat=self.pool.get('sfp.contrat').browse(cr,uid,contract)
            if object_contrat:
                data['birth_day'] = object_contrat.apprenti.birthdate_1  or False
                data['birth_place'] = object_contrat.apprenti.lieu_birth_ar.name_ar  or False
                data['cin'] = object_contrat.apprenti.cin  or False
                data['full_name'] = object_contrat.apprenti.name_arabic  or False
                data['metier'] = object_contrat.metier.name_ar  or False
                data['date_end'] = object_contrat.date_end  or False
                data['cfa'] = object_contrat.cfa.name_ar  or False
                data['adresse'] = object_contrat.apprenti.street  or False
                data['branche'] = object_contrat.metier.sect_id.name_ar  or False
                
        return {'value' : data }