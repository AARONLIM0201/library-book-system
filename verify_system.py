import unittest
import json
from app import app
from database import db
from models import Book, Borrower, Transaction, AuditLog

class TestLibrarySystem(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.secret_key = 'test_secret'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_auth_protection(self):
        # 1. Access Dashboard without login (Should fail/redirect)
        print("Testing: Access Dashboard Protected")
        res = self.client.get('/', follow_redirects=True)
        self.assertIn(b'Sign In', res.data)

        # 2. Login with wrong credentials
        print("Testing: Login Failure")
        res = self.login('admin', 'wrongpass')
        self.assertIn(b'Invalid Credentials', res.data)

        # 3. Login with correct credentials
        print("Testing: Login Success")
        res = self.login('admin', 'pa$$wOrd')
        # Should see Dashboard text
        self.assertIn(b'Library Book Tracking System', res.data)

        # 4. Access Protected Route (Books)
        print("Testing: Access Protected Route")
        res = self.client.get('/books')
        self.assertEqual(res.status_code, 200)

        # 5. Logout
        print("Testing: Logout")
        res = self.logout()
        self.assertIn(b'Sign In', res.data)

if __name__ == '__main__':
    unittest.main()
