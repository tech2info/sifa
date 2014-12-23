# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2014 Iminoika Services Consulting (Ait Mlouk Addi / 0672977726 / aitmlouk@gmail.com).
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
from openerp.osv import osv


class ParticularReport(osv.AbstractModel):
    _name = 'report.sfa.report_saleorder2'
    def render_html(self, cr, uid, ids, data=None, context=None):
        report_obj = self.pool['report']
        report = report_obj._get_report_from_name(
            cr, uid, 'sfa.report_saleorder2'
        )
        docargs = {
            'doc_ids': ids,
            'doc_model': report.model,
            'docs': self.pool[report.model].browse(
                cr, uid, ids, context=context
            ),
        }
        return report_obj.render(
            cr, uid, ids, 'sfa.report_saleorder2',
            docargs, context=context
        )