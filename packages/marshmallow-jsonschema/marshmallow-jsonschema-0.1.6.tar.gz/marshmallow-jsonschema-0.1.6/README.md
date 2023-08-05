## marshmallow-jsonschema: JSON Schema formatting with marshmallow

[![Build Status](https://travis-ci.org/fuhrysteve/marshmallow-jsonschema.svg?branch=master)](https://travis-ci.org/fuhrysteve/marshmallow-jsonschema)

 marshmallow-jsonschema translates marshmallow schemas into
 JSON Schema Draft v4 compliant jsonschema. See http://json-schema.org/

#### Why would I want my schema translated to JSON?

What are the use cases for this? Let's say you have a
marshmallow schema in python, but you want to render your
schema as a form in another system (for example: a web browser
or mobile device).

#### Installation

```
pip install marshmallow-jsonschema
```

#### Some Client tools can render forms using JSON Schema

* https://github.com/brutusin/json-forms
* https://github.com/jdorn/json-editor
* https://github.com/ulion/jsonform


#### Simple Example

```python
from marshmallow_jsonschema import JSONSchema
from tests import UserSchema

user_schema = UserSchema()

json_schema = JSONSchema()
json_schema.dump(user_schema).data
```
Yields:
```python
{'properties': {'addresses': {'items': {'properties': {'city': {'title': 'city',
                                                                'type': 'string'},
                                                       'floor': {'title': 'floor',
                                                                 'type': 'string'},
                                                       'id': {'default': 'no-id',
                                                              'title': 'id',
                                                              'type': 'string'},
                                                       'number': {'title': 'number',
                                                                  'type': 'string'},
                                                       'street': {'title': 'street',
                                                                  'type': 'string'}},
                                        'required': ['city',
                                                     'number',
                                                     'street'],
                                        'type': 'object'},
                              'type': ['array', 'null']},
                'age': {'format': 'float', 'title': 'age', 'type': 'number'},
                'balance': {'format': 'decimal',
                            'title': 'balance',
                            'type': 'number'},
                'birthdate': {'format': 'date',
                              'title': 'birthdate',
                              'type': 'string'},
                'created': {'format': 'date-time',
                            'title': 'created',
                            'type': 'string'},
                'created_formatted': {'format': 'date-time',
                                      'title': 'created',
                                      'type': 'string'},
                'created_iso': {'format': 'date-time',
                                'title': 'created',
                                'type': 'string'},
                'email': {'title': 'email', 'type': 'string'},
                'finger_count': {'format': 'integer',
                                 'title': 'finger_count',
                                 'type': 'number'},
                'github': {'properties': {'uri': {'title': 'uri',
                                                  'type': 'string'}},
                           'required': ['uri'],
                           'type': 'object'},
                'hair_colors': {'title': 'hair_colors', 'type': 'array'},
                'homepage': {'title': 'homepage', 'type': 'string'},
                'id': {'default': 'no-id', 'title': 'id', 'type': 'string'},
                'name': {'title': 'name', 'type': 'string'},
                'registered': {'title': 'registered', 'type': 'boolean'},
                'sex': {'title': 'sex', 'type': 'string'},
                'sex_choices': {'title': 'sex_choices', 'type': 'array'},
                'since_created': {'title': 'since_created', 'type': 'string'},
                'species': {'title': 'SPECIES', 'type': 'string'},
                'time_registered': {'format': 'time',
                                    'title': 'time_registered',
                                    'type': 'string'},
                'uid': {'format': 'uuid', 'title': 'uid', 'type': 'string'},
                'updated': {'format': 'date-time',
                            'title': 'updated',
                            'type': 'string'},
                'updated_local': {'format': 'date-time',
                                  'title': 'updated',
                                  'type': 'string'},
                'various_data': {'title': 'various_data', 'type': 'object'}},
 'required': ['name'],
 'type': 'object'}
```

#### Nested Example

```python
from marshmallow import Schema, fields
from marshmallow_jsonschema import JSONSchema
from tests import UserSchema


class Athlete(object):
    user_schema = UserSchema()

    def __init__(self):
        self.name = 'sam'


class AthleteSchema(Schema):
    user_schema = fields.Nested(JSONSchema)
    name = fields.String()

    
athlete = Athlete()
athlete_schema = AthleteSchema()

athlete_schema.dump(athlete).data
```
