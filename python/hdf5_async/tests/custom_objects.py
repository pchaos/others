import json

class Person:
    def __init__(self, name: str, age: int, city: str = "Unknown"):
        self.name = name
        self.age = age
        self.city = city

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "city": self.city
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name"),
            age=data.get("age"),
            city=data.get("city")
        )

    def __eq__(self, other):
        if not isinstance(other, Person):
            return NotImplemented
        return self.name == other.name and self.age == other.age and self.city == other.city

class Json:
    def __init__(self, data):
        self.data = data

    def to_json_string(self):
        return json.dumps(self.data)

    @classmethod
    def from_json_string(cls, json_string):
        return cls(json.loads(json_string))

    def __eq__(self, other):
        if not isinstance(other, Json):
            return NotImplemented
        return self.data == other.data
