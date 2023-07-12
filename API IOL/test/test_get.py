import requests
import unittest

class get(unittest.TestCase):
    def setUp(self):
        self.server = "http://127.0.0.1:8000/"
        
    def test_get_happy_path(self):
        response = requests.get(url=self.server)
        status_code = 200
        self.assertEqual(response.status_code,\
                         status_code,\
                         "Error de Conexion a la API")
        data = response.text
        expected_response="Bienvenidos a la API"
        
        self.assertTrue(expected_response in str(data),\
                        "No dio la bienvenida la API" )
    
if __name__ == '__main__':
    unittest.main()