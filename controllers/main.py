# -*- coding: utf-8 -*-
import ast
import base64
import csv
import functools
import glob
import itertools
import jinja2
import logging
import operator
import datetime
import hashlib
import os
import re
import simplejson
import sys
import time
import urllib2
import zlib
from xml.etree import ElementTree
from cStringIO import StringIO

import babel.messages.pofile
import werkzeug.utils
import werkzeug.wrappers
try:
    import xlwt
except ImportError:
    xlwt = None

import openerp
import openerp.modules.registry
from openerp.addons.base.ir.ir_qweb import AssetsBundle, QWebTemplateNotFound
from openerp.modules import get_module_resource
from openerp.tools import topological_sort
from openerp.tools.translate import _
from openerp import http

from openerp.http import request, serialize_exception as _serialize_exception

_logger = logging.getLogger(__name__)


# 1 week cache for asset bundles as advised by Google Page Speed
BUNDLE_MAXAGE = 60 * 60 * 24 * 7

#----------------------------------------------------------
# OpenERP Web helpers
#----------------------------------------------------------

db_list = http.db_list

db_monodb = http.db_monodb

class Binary(http.Controller):

    @http.route([
        '/portal_user_image/binary/company_logo',
        '/portal_user_image/logo',
        '/portal_user_image/logo.png',
    ], type='http', auth="none", cors="*")
    def company_logo(self, dbname=None, **kw):
        imgname = 'logo.png'
        placeholder = functools.partial(get_module_resource, 'web', 'static', 'src', 'img')
        uid = None
        if request.session.db:
            dbname = request.session.db
            uid = request.session.uid
        elif dbname is None:
            dbname = db_monodb()

        if not uid:
            uid = openerp.SUPERUSER_ID

        groups_obj = request.registry.get('res.groups')
        groups_id = groups_obj.search(request.cr,openerp.SUPERUSER_ID,[('name','=','Portal')])
        pid = None
        if groups_id:
            group_browse = groups_obj.browse(request.cr, openerp.SUPERUSER_ID, groups_id, context=request.context)
            if group_browse.users:
                for user in group_browse.users:
                    if uid == user.id:
                        pid = uid

        if not dbname:
            response = http.send_file(placeholder(imgname))
        else:
            try:
                if pid:
                    # create an empty registry
                    registry = openerp.modules.registry.Registry(dbname)
                    with registry.cursor() as cr:
                        cr.execute("""SELECT c.portal_image, c.write_date
                                        FROM res_users u
                                   LEFT JOIN res_company c
                                          ON c.id = u.company_id
                                       WHERE u.id = %s
                                   """, (uid,))
                        row = cr.fetchone()
                        if row and row[0]:
                            image_data = StringIO(str(row[0]).decode('base64'))
                            response = http.send_file(image_data, filename=imgname, mtime=row[1])
                        else:
                            response = http.send_file(placeholder('nologo.png'))
                else:
                    registry = openerp.modules.registry.Registry(dbname)
                    with registry.cursor() as cr:
                        cr.execute("""SELECT c.logo_web, c.write_date
                                        FROM res_users u
                                   LEFT JOIN res_company c
                                          ON c.id = u.company_id
                                       WHERE u.id = %s
                                   """, (uid,))
                        row = cr.fetchone()
                        if row and row[0]:
                            image_data = StringIO(str(row[0]).decode('base64'))
                            response = http.send_file(image_data, filename=imgname, mtime=row[1])
                        else:
                            response = http.send_file(placeholder('nologo.png'))
            except Exception:
                response = http.send_file(placeholder(imgname))

        return response

# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
