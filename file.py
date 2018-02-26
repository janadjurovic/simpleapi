from flask import Flask, jsonify, request, abort
import json

app = Flask(__name__)

def as_json(object):
    return object.__dict__

class Employee:

    def __init__(self, params): 
        self.id = params['id']
        self.name = params['name']
        self.position = params['position']
        self.department_id = params['department_id']    
    
class Department:
    
    def __init__(self, params):
        self.id = params['id']
        self.name = params['name']

def get_employee_params(request):
    if 'content-type' in request.headers and request.headers['content-type'] == 'application/json':
        return {
            'id': request.json['id'],
            'name': request.json['name'],
            'position': request.json['position'],
            'department_id': request.json['department_id']
        }
        
    return {
        'id': request.args.get('id').encode('utf-8'),
        'name': request.args.get('name').encode('utf-8'),
        'position': request.args.get('position').encode('utf-8'),
        'department_id': request.args.get('department_id').encode('utf-8')
    }



def get_department_params(request):
    if 'content-type' in request.headers and request.headers['content-type'] == 'application/json':
        return {
            'id' : request.json['id'],
            'name' : request.json['name']
        }
    return {
        'id': request.args.get('id').encode('utf-8'),
        'name': request.args.get('name').encode('utf-8')
    }

def authentificate(request):
    if not request.args.get('token'):
        abort(401)
    elif request.args.get('token') != '123':
        abort(403)

employees=[]
departments=[]

def get_department_ids():
    department_ids = []
    for dep in departments:
        department_ids.append(dep.id)
    return department_ids    

def check_employee_params(params):
    if params["name"] == "":
        raise RuntimeError('Invalid arguments')
    if not params["department_id"] in get_department_ids():
        raise RuntimeError('Invalid arguments')

def check_department_params(params):
    if params["name"] == "":
        raise RuntimeError('Invalid arguments')

@app.route('/employee', methods=['GET'])
def get_employees():
    authentificate(request)
    return json.dumps(employees,default = as_json)

@app.route('/department', methods=['GET'])
def get_departments():
    authentificate(request)
    return json.dumps(departments,default = as_json)

@app.route('/employee', methods=['POST'])
def create_employee():
    try:
        authentificate(request)
        params = get_employee_params(request)
        check_employee_params(params)
        employee = Employee(params)
        employees.append(employee)
        return json.dumps(employee, default = as_json)
    except:
        abort(400)

@app.route('/department', methods=['POST'])
def create_department():
    try:
        authentificate(request)
        params = get_department_params(request)
        check_department_params(params)
        department = Department(params)
        departments.append(department)
        return json.dumps(department, default = as_json)
    except:
        abort(400)
        
@app.route('/', defaults={'path': ''}, methods = ['GET', 'POST'])
@app.route('/<path:path>',methods = ['GET', 'POST'])
def catch_all(path):
    abort(403)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5001)

