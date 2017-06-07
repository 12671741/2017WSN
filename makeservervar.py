from ubidots import ApiClient
api = ApiClient(token='qbK1CZWTKKlLd71Dq1WosAxiRpf3AK')
new_datasource = api.create_datasource({"name": "SmartGym", "tags": ["firstDs", "new"], "description": "any des"})
new_variable = new_datasource.create_variable({"name": "heartrate", "unit": "times/m"})
new_variable = new_datasource.create_variable({"name": "pushups", "unit": "times"})
new_variable = new_datasource.create_variable({"name": "tempreture", "unit": "C"})
