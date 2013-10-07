#!/usr/bin/env python

"""csv2asana

Script to import csv file to Asana <http://asana.com>. 
This script is not affiliated with or endorsed by Asana.

Copyright (c) 2013 Witchakorn Kamolpornwijit <me@chalet16.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import csv

# Please change this to match with your need.
api_key = '!!!CHANGEME!!!'
workspace_name = "Personal Project"
project_name = "MIT Exam"
csv_file = "exam_data.csv"
csv_dialect = csv.excel
asana_fields = {
          'name': '{subject}',
          'due_on': '{start_date}',
          'notes': '{description}',
          }
date_format = '%m/%d/%Y'
tag_prefix = 'csv2asana' 

from asana import asana
import datetime, time

def get_project_and_workspace_id(asana_api, name , object_type='project'):
    if object_type == 'project':
        asana_object = asana_api.list_projects()
    else:
        asana_object = asana_api.list_workspaces()
    print asana_object
    selected_object = [item['id'] for item in asana_object if item['name'] == name]
    if len(selected_object) != 1:
        raise Exception('No /More than one %s(s) found.' % (object_type))
    return selected_object[0]
    
# Find Project
asana_api = asana.AsanaAPI(api_key, debug=True)

workspace_id = get_project_and_workspace_id(asana_api, workspace_name, 'workspace')
project_id = get_project_and_workspace_id(asana_api, project_name, 'project')

tag = asana_api.create_tag('%s-%s' % (tag_prefix, datetime.datetime.utcnow()), workspace_id)
# CSV
with open(csv_file, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, dialect=csv_dialect)
    header = []
    for row in spamreader:
        if header == []:
            header = [col.strip().lower().replace(" ", "_") for col in row] 
            print header
        else:
            task = {}
            for csv_col_id, value in enumerate(row):
                    task[header[csv_col_id]] = value
            asana_task = {}
            for field, format_string in asana_fields.iteritems():
                # print field, task
                asana_task[field] = format_string.format(**task)
            asana_task['due_on'] = time.strftime('%Y-%m-%d', time.strptime(asana_task['due_on'], date_format))
            res = asana_api.create_task(workspace=workspace_id, **asana_task)
            asana_api.add_project_task(res['id'], project_id)
            asana_api.add_tag_task(res['id'], tag['id'])
            print "AA", task
            exit()
