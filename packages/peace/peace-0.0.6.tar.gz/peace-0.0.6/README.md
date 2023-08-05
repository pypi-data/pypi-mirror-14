# Peace

A REST client - inspired by restmod for javascript.

## Test status

[ ![Codeship Status for garymonson/peace](https://codeship.com/projects/3308e5a0-b522-0133-3191-1af10c27659b/status?branch=master)](https://codeship.com/projects/134053)

## Quick start for contributing

    virtualenv -p `which python3` virtualenv
    source virtualenv/bin/activate
    pip install -r requirements.txt
    pip install -r dev_requirements.txt
    nosetests

## Usage

```
from peace import PeaceMaker

def set_authorization_header(request):
    request.headers['Authorization'] = authorization_value
    return request

maker = PeaceMaker('http://api.example.com')
Employee = maker.make(
    'Employee',
    '/employees'
    has: {
        'user': maker.make('Company'),
    },
    intercept: set_authorization_header,
)

employees = Employee.search(last_name='Smith')
bob = Employee.get('100')
bob.last_name = 'Smith-Jones'
bob.save()
bob.refresh()
company = bob.company
print(company.name) # prints name
```

Peace requires the REST API to conform to a particular structure.  A JSON
response should look something like this:

```
{
  "data": {
    "id": 100,
    "first_name": "Bob",
    "last_name": "Smith",
  },
  "links": {
    "self": {"href": "/employees/100"},
    "company": {
      "href": "/companies/5",
      "data": {
        "name": "Big Corp",
      },
    },
  },
}
```

Links can be followed (e.g. bob.company).  Initially, the data returned in the
original request will be immediately available, but if you try to access other
fields that a direct load is required to make available, (i.e. were not in the
original response), then a load of the linked object will be done first (e.g.
GET /companies/5).
