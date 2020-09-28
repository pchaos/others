# -*- coding: utf-8 -*-
import sys
import json
import os
import jinja2
from jinja2 import Environment, Template

def render(tpl_path, page):
    path, filename = os.path.split(tpl_path)
    env = Environment(
        loader=jinja2.FileSystemLoader(path or './')
    )
    env.filters['jsonify'] = json.dumps
    return env.get_template(filename).render(page=page)


# load json from file
jsonConfigName = "templates/example.json"
print("jsonConfigName: " + jsonConfigName)
with open(jsonConfigName) as json_file:
    json_data = json.load(json_file)
    #print(json_data)

page = {
  'title': 'Jinja Example Page',
	'tags': ['jinja', 'python', 'migration'],
	'description': 'This is an example page created using Jinja2 with a JSON template.'
}

print(render(jsonConfigName, page=page))



