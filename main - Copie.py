import unittest
from app import app, db, User

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_user(self):
        response = self.app.post('/adduser', json={'login': 'test_user', 'pwd': 'test_pwd', 'nom': 'Test', 'prenom': 'User'})
        self.assertEqual(response.status_code, 201)

    def test_check_user(self):
        self.app.post('/adduser', json={'login': 'test_user', 'pwd': 'test_pwd', 'nom': 'Test', 'prenom': 'User'})
        response = self.app.post('/checkuser', json={'login': 'test_user', 'pwd': 'test_pwd'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'nom': 'Test', 'prenom': 'User'})

if __name__ == '__main__':
    unittest.main()
