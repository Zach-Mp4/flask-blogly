from unittest import TestCase

from app import app
from models import db, User
# python -m unittest test_app.py
# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///testblogly'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

ctx = app.app_context()
ctx.push()

db.drop_all()
db.create_all()
url = 'https://static.wikia.nocookie.net/naruto/images/d/d6/Naruto_Part_I.png/revision/latest/scale-to-width-down/1200?cb=20210223094656'
class UserTestViews(TestCase):
    """tests views for Users"""

    def setUp(self):
        User.query.delete()
        user = User(first_name = 'Joe', last_name = 'Mama', image_url = url)

        db.session.add(user)
        db.session.commit()
        
        self.user_id = user.id
    
    def tearDown(self):
        db.session.rollback()
    
    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Joe', html)
    
    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li>first name: Joe</li>', html)
    
    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "Joe2", "last_name": "Mama2", "image_url": url}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Joe2", html)

    
