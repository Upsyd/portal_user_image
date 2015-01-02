# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014-Today BrowseInfo (<http://www.browseinfo.in>)
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

{
    'name': 'Portal User Image',
    'author': 'Browseinfo',
    'website': 'www.browseinfo.in',
    'version': '0.1',
    'depends': ['base','sale','web'],
    'category' : 'Tools',
    'summary': 'Portal User Image',
    'data': [
        'portal_user_image.xml',
        'views/portal_image_templates.xml',
    ],
    'demo': [],
    'installable': True,
    'application' : True,
    'certificate' : '',
}
