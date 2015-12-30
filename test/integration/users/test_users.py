# -*- coding: utf-8 -*-

from mock import Mock, patch
from flask.ext.login import login_user

from test.test_base import BaseTestCase
from beacon.models.users import User
from beacon.models.public import AcceptedEmailDomains
from test.factories import DepartmentFactory, UserFactory, RoleFactory

class TestUserAuth(BaseTestCase):
    render_template = True

    def setUp(self):
        super(TestUserAuth, self).setUp()
        self.email = 'foo@foo.com'
        user = UserFactory.create(email=self.email)
        user.save()
        AcceptedEmailDomains.create(domain='foo.com')
        DepartmentFactory.create(name='New User').save()
        self.department1 = DepartmentFactory.create(name='Test').save()

    def test_thispage(self):
        request = self.client.get('/admin', follow_redirects=True)
        self.assertTrue('?next=%2Fadmin%2F' in request.data)

    @patch('urllib2.urlopen')
    def test_auth_persona_failure(self, urlopen):
        mock_open = Mock()
        mock_open.read.side_effect = ['{"status": "error"}']
        urlopen.return_value = mock_open

        post = self.client.post('/users/auth', data=dict(
            assertion='test'
        ))

        self.assert403(post)

    @patch('urllib2.urlopen')
    def test_auth_no_user(self, urlopen):
        mock_open = Mock()
        mock_open.read.side_effect = ['{"status": "okay", "email": "not_a_valid_email"}']
        urlopen.return_value = mock_open

        post = self.client.post('/users/auth', data=dict(
            assertion='test'
        ))

        self.assert403(post)

    @patch('urllib2.urlopen')
    def test_auth_success(self, urlopen):
        mock_open = Mock()
        mock_open.read.side_effect = [
            '{"status": "okay", "email": "' + self.email + '"}',
            '{"status": "okay", "email": "' + self.email + '"}'
        ]
        urlopen.return_value = mock_open

        post = self.client.post('/users/auth?next=/explore/', data=dict(
            assertion='test'
        ))

        self.assert200(post)
        self.assertEquals(post.data, '/explore/')

        self.client.get('/users/logout')

    @patch('urllib2.urlopen')
    def test_new_user_success(self, urlopen):
        # insert all of our roles
        RoleFactory.create(name='superadmin')
        RoleFactory.create(name='admin')
        RoleFactory.create(name='staff')

        # assert we have only one user
        self.assertEquals(User.query.count(), 1)

        mock_open = Mock()
        mock_open.read.side_effect = [
            '{"status": "okay", "email": "new@foo.com"}'
        ]
        urlopen.return_value = mock_open

        post = self.client.post('/users/auth?next=/explore/', data=dict(
            assertion='test'
        ))

        # assert we add a new user and redirect to the register page
        self.assertEquals(User.query.count(), 2)
        self.assertEquals(post.status_code, 200)
        self.assertEquals(post.data, '/users/profile')

        # assert we get the new user message
        register = self.client.get('/users/profile')
        self.assertTrue('Welcome to the Pittsbugh Purchasing Suite!' in register.data)
        self.assert_template_used('users/profile.html')

        # assert that you cannot update with junk information
        bad_update = self.client.post('/users/profile', data=dict(
            department='THIS IS NOT A VALID DEPARTMENT'
        ), follow_redirects=True)
        self.assertTrue(
            'THIS IS NOT A VALID DEPARTMENT' not in [i.department for i in User.query.all()]
        )
        self.assertTrue('Not a valid choice' in bad_update.data)

        # update the user successfully
        update = self.client.post('/users/profile', data=dict(
            first_name='foo', last_name='bar', department=str(self.department1.id)
        ))

        # assert we successfully update
        self.assertEquals(update.status_code, 302)
        self.assertEquals(update.location, 'http://localhost/users/profile')
        self.assert_flashes('Updated your profile!', 'alert-success')

        # make sure the new user message is gone
        updated = self.client.get('/users/profile')

        self.assertTrue('Welcome to the Pittsbugh Purchasing Suite!' not in updated.data)
        self.assert_template_used('users/profile.html')

    @patch('urllib2.urlopen')
    def test_logout(self, urlopen):
        login_user(User.query.all()[0])

        logout = self.client.get('/users/logout', follow_redirects=True)
        self.assertTrue('Logged out successfully' in logout.data)
        self.assert_template_used('users/logout.html')

        login_user(User.query.all()[0])
        logout = self.client.post('/users/logout?persona=True', follow_redirects=True)
        self.assertTrue(logout.data, 'OK')
