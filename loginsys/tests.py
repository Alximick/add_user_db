from django.test import TestCase
from loginsys.admin import UserCreationForm


class loginsys(TestCase):
    name = 'create'
    phone_number = 2
    password = 'qwerty123'

    def setUp(self):
        pass


    def test_filter(self):
        form = UserCreationForm({
            'username': self.name,
            'phone_number': self.phone_number,
            'password1': self.password,
            'password2': self.password,
        })
        self.assertTrue(form.is_valid())
        form.is_valid()
        comment = form.save()
        self.assertEqual(print(comment.username), print(self.name))
        # self.assertEqual(comment.phone_number, self.phone_number)