from flask import Flask, jsonify, request, abort
import json

app = Flask(__name__)

def as_json(object):
    return object.__dict__

class Employee:

    def __init__(self, params):
        self.id = params["id"]
        self.name = params["name"]
        self.position = params["position"]
        self.department_id = params["department_id"]
 
class Department:
    
    def __init__(self, params):
        self.id = params["id"]
        self.name = params["name"]

def get_employee_params(request):
    return {
        "id" : request.json["id"],
        "name" : request.json["name"],
        "position" : request.json["position"],
        "department_id" : request.json["department_id"]
      }

def get_department_params(request):
    return {
        "id" : request.json["id"],
        "name" : request.json["name"]
    }

def authentificate(request):
    if not request.args.get('token'):
        abort(401)
    elif request.args.get('token') != '123':
        abort(403)

employees=[]
departments=[]

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
    authentificate(request)
    employee = Employee(get_employee_params(request))
    employees.append(employee)
    return json.dumps(employee, default = as_json)

@app.route('/department', methods=['POST'])
def create_department():
    authentificate(request)
    department = Department(get_department_params(request))
    departments.append(department)
    return json.dumps(department, default = as_json)
        
@app.route('/', defaults={'path': ''}, methods = ['GET', 'POST'])
@app.route('/<path:path>',methods = ['GET', 'POST'])
def catch_all(path):
    abort(403)

if __name__ == '__main__':
    app.run(debug = True, port = 5000)

