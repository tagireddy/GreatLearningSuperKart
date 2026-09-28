import io
import unittest

from app import app


class SuperKartApiTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload['status'], 'ok')
        self.assertTrue(payload['model_loaded'])

    def test_model_info_endpoint(self):
        response = self.client.get('/model-info')
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn('expected_features', payload)
        self.assertIn('model_path', payload)

    def test_predict_requires_fields(self):
        response = self.client.post('/v1/predict', json={'Product_Weight': 10.0})
        self.assertEqual(response.status_code, 400)
        payload = response.get_json()
        self.assertIn('error', payload)

    def test_predict_success(self):
        payload = {
            'Product_Weight': 9.3,
            'Product_Sugar_Content': 'Low Sugar',
            'Product_Allocated_Area': 0.12,
            'Product_MRP': 150.0,
            'Store_Size': 'Medium',
            'Store_Location_City_Type': 'Tier 2',
            'Store_Type': 'Supermarket Type 1',
            'Product_Id_char': 'FD',
            'Store_Age_Years': 12,
            'Product_Type_Category': 'Snack Foods',
        }
        response = self.client.post('/v1/predict', json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('sales', data)
        self.assertIsInstance(data['sales'], float)

    def test_predict_batch_success(self):
        csv_data = (
            'Product_Id,Product_Weight,Product_Sugar_Content,Product_Allocated_Area,'
            'Product_Type,Product_MRP,Store_Id,Store_Establishment_Year,Store_Size,'
            'Store_Location_City_Type,Store_Type\n'
            'FD11,11.1,Low Sugar,0.021,Non Perishables,99.0,S6,2016,Medium,Tier 2,Supermarket Type1\n'
            'FD12,13.2,Regular,0.026,Non Perishables,125.0,S7,2012,High,Tier 1,Departmental Store\n'
        )

        response = self.client.post(
            '/v1/predictbatch',
            data={'file': (io.BytesIO(csv_data.encode('utf-8')), 'batch.csv')},
            content_type='multipart/form-data',
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)


if __name__ == '__main__':
    unittest.main()
