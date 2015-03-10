# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
#    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
from openerp.osv import osv, fields

class sfa_certificate_groups(osv.osv_memory):
    _name = 'sfp.certificate.groupe'
    _columns = {
            #'year' : fields.many2one('madrassa.academic.year',u'Année académique'),
            'all_groups' : fields.boolean(u'Toutes les Groupes'),
            'state' : fields.selection([('processing',u'En Preparation'),('year1',u'1ere Année'),('year2',u'2eme Année'),('done',u'Terminé')],u'Etat'),
            'groupe_ids' : fields.many2many('sfp.groupe', 'sfp_certificate_groupe_rel', 'sfp_certificate_groupe_id', 'groupe_id', u'Groupes'),
        }
    
    def action_print_certificate(self, cr, uid, ids, context=None):
        """
         To get the date and print the report
         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param context: A standard dictionary
         @return : retrun report
        """
        if context is None:
            context = {}
        ids_registration=[]
        for object_certificate in self.browse(cr,uid,ids):
            ids_contrat = [x.id for x in object_certificate.groupe_ids]
            #ids_search_registration = self.pool.get('madrassa.registration').search(cr,uid,[('year','=',object_certificate.year.id),('student','in',tuple(ids_students))])
        #datas = {'ids': ids_search_registration}
        datas = {'ids': ids_contrat}
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'sifa.report_vacataire',
            'datas': datas,
        }
        
    def onchange_all_groups(self,cr,uid,ids,all_groups, state,context={}):
        data={}
        if all_groups:
            
            data['groupe_ids'] = self.pool.get('sfp.groupe').search(cr,uid,[('state','=',state)])
        else:
            data['groupe_ids'] = []
        return {'value' : data}
sfa_certificate_groups()
