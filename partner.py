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
from openerp.osv import orm, fields
from openerp.tools.translate import _
import time
from datetime import date

class res_partner(orm.Model):
    
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
    
    
    _columns = {
            'name_arabic' : fields.char(u'الإسم '),
            'first_name_arabic' : fields.char(u'النسب'),
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
            'gender_' : fields.selection([('male',u'Masculin'),('female',u'Féminin')],u'Sexe'), 
            'gender_ar' : fields.selection([('male',u'دكر'),('female',u'انتى')],u'الجنس'), 
            'groupe' : fields.many2one('sfp.groupe', u'Groupe'),
            'cfa' :fields.many2one('sfp.groupe', u'CFA'),
            'contrat' :fields.many2one('sfp.groupe', u'Contrat'),

            'vacataire_ok': fields.boolean('Vacataire'),
            'entreprise_ok': fields.boolean('Entreprise'),
           
            #vacataire
            'vac_year' : fields.char(u'Année de vacation'),
            'nbr_visite' : fields.char(u'Nombre de visites'),
            'masse_horaire' : fields.char(u'Masse horaire'),
            'grade_ids': fields.many2many('sfp.grade','sfp_grade_rel','vacataire_id','grade_id',u'Grades'), 
            'matier_ids': fields.many2many('sfp.matier','sfp_matier_rel','vacataire_id','matier_id',u'Matières'), 


            }
    