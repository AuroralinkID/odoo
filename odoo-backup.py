#! /bin/env python3

#    Copyright (C) 2019  @jhbez

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import requests
from datetime import datetime
import argparse

class Odoobackup(object):

    
    host = "http://localhost:8069"
    endpoint = "/web/database/backup"
    master_pwd = "admin"
    db_name= ""
    backup_format = "zip"
    path_backup = "/tmp/"
    
    @classmethod
    def backup(cls, **kwargs ):
        if "host" in kwargs:
            cls.host = kwargs.get("host")
        url = cls.host + cls.endpoint

        if "master_pwd" in kwargs:
            cls.master_pwd = kwargs.get("master_pwd")
        if "db_name" in kwargs:
            cls.db_name = kwargs.get("db_name")
        else:
            raise Exception("Db name is mandatory!")
        data = "master_pwd={}&name={}&backup_format={}".format(
            cls.master_pwd, 
            cls.db_name,
            cls.backup_format)
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(url=url,data=data,headers=headers, stream=True)
        filename = "{}_{}.{}".format(
            cls.db_name,
            datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), 
            cls.backup_format)

        if "path_backup" in kwargs:
            cls.path_backup = kwargs.get("path_backup")
        
        out = cls.path_backup + filename
        if response.status_code == 200 and "attachment;" in response.headers.get('Content-Disposition',""):
            with open(out, 'wb') as local_file:
                for chunk in response.iter_content(chunk_size=128):
                    local_file.write(chunk)
                print ("Backup :), path: {}".format(out))
        else:
            print ("Backup :(")

parser=argparse.ArgumentParser(
    description='''Script Odoo backup''',
    epilog=''' 
    odoo-backup  Copyright (C) 2019  @jhbez
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.
    ''')

parser.add_argument('--name',required=True, help='Database name')
parser.add_argument('--host', default="http://localhost:8069", help='Website URL')
parser.add_argument('--pwd', default="admin", help='Master password')
parser.add_argument('--path', default="/tmp/", help='Path backup')

args=parser.parse_args()
Odoobackup.backup(
    db_name=args.name,
    master_pwd=args.pwd,
    path_backup=args.path,
    host=args.host
)