import json
import requests_mock
import unittest

from peace import PeaceMaker, status_code_exceptions


@requests_mock.Mocker()
class PeaceTest(unittest.TestCase):
    def setUp(self):
        super(PeaceTest, self).setUp()

        self.maker = PeaceMaker('http://localhost')
        self.Employee = self.maker.make(
            'Employee',
            '/employees',
            has={
                'company': self.maker.make('Company')
            },
        )

        self.employees = {
            '5': {
                'data': {
                    'id':   '5',
                    'name': 'Bob',
                    'dob':  '1980-01-01',
                },
                'links': {
                    # TODO make relative URLs work, too
                    'self': {'href': 'http://localhost/employees/5'},
                    'company': {'href': 'http://localhost/companies/100', 'data': {'name': 'Bob Enterprises'}},
                },
            },
            '6': {
                'data': {
                    'id':   '6',
                    'name': 'Jim',
                    'dob':  '1985-02-01',
                },
                'links': {
                    # TODO make relative URLs work, too
                    'self': {'href': 'http://localhost/employees/6'},
                    'company': {'href': 'http://localhost/companies/200', 'data': {'name': 'Jim Industries'}},
                },
            },
        }
        self.last_employee_id = 6
        self.companies = {
            '100': {
                'data': {
                    'id':   '100',
                    'name': 'Bob Enterprises',
                    'tax_number': '12345',
                },
                'links': {
                    'self': {'href': 'http://localhost/companies/100'},
                },
            },
            '200': {
                'data': {
                    'id':   '200',
                    'name': 'Jim Industries',
                    'tax_number': '67890',
                },
                'links': {
                    'self': {'href': 'http://localhost/companies/200'},
                },
            },
        }


    def test_get(self, m):
        m.get('http://localhost/employees/5', text=json.dumps(self.employees['5']))
        m.get('http://localhost/employees/6', text=json.dumps(self.employees['6']))

        bob = self.Employee.get(5)
        jim = self.Employee.get(6)

        self.assertEqual(bob.name, 'Bob')
        self.assertEqual(bob.dob, '1980-01-01')

        self.assertEqual(jim.name, 'Jim')
        self.assertEqual(jim.dob, '1985-02-01')

        with self.assertRaises(AttributeError):
            bob.country
        with self.assertRaises(AttributeError):
            jim.country

        for code in status_code_exceptions.keys():
            m.get('http://localhost/employees/5', status_code=code)
            with self.assertRaises(status_code_exceptions[code]):
                bob.refresh()
            try:
                jim.refresh()
            except:
                self.assertTrue(False)
            else:
                self.assertTrue(True)
            with self.assertRaises(status_code_exceptions[code]):
                self.Employee.get(5)

    def test_search(self, m):
        m.get('http://localhost/employees', complete_qs=True, text=json.dumps({'data': [self.employees[id] for id in sorted(self.employees.keys())]}))
        m.get('http://localhost/employees?id=5', complete_qs=True, text=json.dumps({'data': [self.employees['5']]}))
        m.get('http://localhost/employees?id=6', complete_qs=True, text=json.dumps({'data': [self.employees['6']]}))

        found = self.Employee.search()
        self.assertEqual(
            [[emp.name, emp.dob] for emp in found],
            [['Bob', '1980-01-01'], ['Jim', '1985-02-01']]
        )

        found = self.Employee.search(id=5)
        self.assertEqual(
            [[emp.name, emp.dob] for emp in found],
            [['Bob', '1980-01-01']]
        )

        found = self.Employee.search(id=6)
        self.assertEqual(
            [[emp.name, emp.dob] for emp in found],
            [['Jim', '1985-02-01']]
        )

    def test_refresh(self, m):
        m.get('http://localhost/employees/5', text=json.dumps(self.employees['5']))
        m.get('http://localhost/employees/6', text=json.dumps(self.employees['6']))

        bob = self.Employee.get(5)
        jim = self.Employee.get(6)

        self.employees['5']['data']['name'] = 'Bobarino'
        self.employees['6']['data']['name'] = 'Jim-bob'

        # Grab latest versions when requesting
        m.get('http://localhost/employees/5', text=json.dumps(self.employees['5']))
        m.get('http://localhost/employees/6', text=json.dumps(self.employees['6']))

        self.assertEqual(bob.name, 'Bob')
        bob.refresh()
        self.assertEqual(bob.name, 'Bobarino')

        self.assertEqual(jim.name, 'Jim')
        jim.refresh()
        self.assertEqual(jim.name, 'Jim-bob')

    def test_links(self, m):
        m.get('http://localhost/employees/5', text=json.dumps(self.employees['5']))
        m.get('http://localhost/employees/6', text=json.dumps(self.employees['6']))
        m.get('http://localhost/companies/100', text=json.dumps(self.companies['100']))
        m.get('http://localhost/companies/200', text=json.dumps(self.companies['200']))

        bob = self.Employee.get(5)
        jim = self.Employee.get(6)

        bob_company = bob.company
        jim_company = jim.company
        # Ensure provided data is immediately available
        self.assertEqual(bob_company.name, 'Bob Enterprises')
        self.assertEqual(jim_company.name, 'Jim Industries')
        # Ensure other data is loaded on access
        self.assertEqual(bob_company.tax_number, '12345')
        self.assertEqual(jim_company.tax_number, '67890')

        with self.assertRaises(AttributeError):
            bob_company.ceo
        with self.assertRaises(AttributeError):
            jim_company.ceo

    def test_save(self, m):
        def save_new(request, context):
            data = request.json()

            self.last_employee_id = self.last_employee_id + 1
            data['id'] = str(self.last_employee_id)
            self.employees[str(self.last_employee_id)] = {
                'data': data,
                'links': {
                    'self': {'href': 'http://localhost/employees/{0}'.format(self.last_employee_id)},
                },
            }
            return json.dumps(self.employees[str(self.last_employee_id)])
        def save_existing(request, context):
            data = request.json()
            self.employees[data['id']]['data'] = data
            return json.dumps(self.employees[data['id']])

        m.post('http://localhost/employees', text=save_new)
        m.put('http://localhost/employees/7', text=save_existing)

        nate = self.Employee(attributes={'name': 'Nate'})

        self.assertEqual(nate.name, 'Nate')

        nate.save()

        self.assertEqual(nate.id, str(self.last_employee_id))
        self.assertEqual(nate.name, 'Nate')

        nate.name = 'NATO'
        nate.save()

        m.get('http://localhost/employees/7', text=json.dumps(self.employees['7']))

        new_nate = self.Employee.get(nate.id)
        self.assertEqual(nate.id, str(self.last_employee_id))
        self.assertEqual(nate.name, 'NATO')

        # Test for conflicts

        bob = self.Employee(attributes={'name': 'bob'})
        bob.save()

        m.post('http://localhost/employees', text='', status_code=409)

        nato = self.Employee(attributes={'name': 'NATO'})
        with self.assertRaises(status_code_exceptions[409]):
            nato.save()

        m.put('http://localhost/employees/{0}'.format(bob.id), text='', status_code=409)
        bob.name = 'NATO'
        with self.assertRaises(status_code_exceptions[409]):
            bob.save()

    def test_intercept(self, m):
        def intercept(request):
            request.headers['Authorization'] = 'Let me in!'
            return request
        self.headers = {}
        def check_intercept(request, context):
            self.headers = request.headers
            return json.dumps({'data': []})

        m.get('http://localhost/employees', text=check_intercept)

        employees = self.Employee.search()
        self.assertTrue('Authorization' not in self.headers)

        AuthEmployee = self.maker.make(
            'AuthEmployee',
            '/employees',
            intercept=intercept,
        )
        employees = AuthEmployee.search()
        self.assertEqual(self.headers['Authorization'], 'Let me in!')

        employees = self.Employee.search()
        self.assertTrue('Authorization' not in self.headers)
