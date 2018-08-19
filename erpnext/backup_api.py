# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
import frappe
import os
from frappe.model.document import Document
from frappe.utils import get_site_base_path
from frappe.utils.data import flt, nowdate, getdate, cint
from frappe.utils.csvutils import read_csv_content_from_uploaded_file
from frappe.utils.password import update_password as _update_password
from frappe.utils import cint, cstr, flt, nowdate, comma_and, date_diff, getdate, get_datetime
from frappe.utils import date_diff
from datetime import timedelta
import datetime
# from umalqurra.hijri_date import HijriDate
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
# from client.hr_services.doctype.end_of_service_award.end_of_service_award import get_award
from frappe.utils.backups import backup
# from frappe.database import connect,sql,check_transaction_status,get_db_login




def get_newest_file():
    import os
    path = '/home/vini/frappe-bench/sites/sundinepro.com/private/backups'
    os.chdir(path)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    if files:
        oldest = files[0]
        newest = files[-1]
        return newest


def transfer_files():
    import paramiko

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('74.208.40.77', username='root', password='HeyRam108')

    print "connected successfully!"

    sftp = ssh.open_sftp()


    # createFolder('/home/vini/frappe-bench/production_backups/')

    filesInRemoteArtifacts = sftp.listdir(path='/home/vini/frappe-bench/production_backups/')
    if len(filesInRemoteArtifacts)<5:
        pass
    else:
        sftp.remove('/home/vini/frappe-bench/production_backups/'+filesInRemoteArtifacts[-1])
   
    print sftp

    import os

    sftp.put('/home/vini/frappe-bench/sites/sundinepro.com/private/backups/'+get_newest_file(),'/home/vini/frappe-bench/production_backups/'+get_newest_file())
    
    sftp.close()
    print "copied successfully!"

    ssh.close()
    exit()


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)



# ------------------------------------------------------------



