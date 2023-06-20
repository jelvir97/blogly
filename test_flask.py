from unittest import TestCase
from app import app
from models import User, db

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class BloglyTests(TestCase):
    def setUp(self):
        "Clean up existing users and add sample user"
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
        app.config['SQLALCHEMY_ECHO'] = True
        User.query.delete()
        user = User(first_name="John",last_name="Doe")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        "Clean up session"
        db.session.rollback()

    def test_users_list(self):
        """Tests /users route"""
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)
            users = User.query.all()

            self.assertEqual(resp.status_code,200)
            self.assertIn('John Doe',html)
            self.assertEqual(len(users),1)

    def test_user_details(self):
        """Tests /user/<user_id> route. Responds with user details page."""
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('First Name: John',html)
            self.assertIn('Last Name: Doe',html)
            self.assertIn('<img',html)

    def test_add_user(self):
        """Tests /users/new route"""
        with app.test_client() as client:
            d ={"first-name": "Bob","last-name": "Dylan","img-url":""}
            resp = client.post('/users/new',data=d,follow_redirects=True)
            html = resp.get_data(as_text=True)
            users = User.query.all()

            self.assertEqual(resp.status_code,200)
            self.assertIn('Bob Dylan',html)
            self.assertEqual(len(users),2)

    def test_user_edit(self):
        """Tests /user/<user_id>/edit route"""
        with app.test_client() as client:
            d ={"first-name": "Bob","last-name": "Dylan","img-url":""}
            resp = client.post(f'/users/{self.user_id}/edit',data=d,follow_redirects=True)
            html = resp.get_data(as_text=True)
            users = User.query.all()

            self.assertEqual(resp.status_code,200)
            self.assertIn('First Name: Bob',html)
            self.assertIn('Last Name: Dylan',html)
            self.assertEqual(len(users),1)