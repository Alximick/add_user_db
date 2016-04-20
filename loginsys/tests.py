from django.test import TestCase
from loginsys.admin import UserCreationForm


class NotesModelTest(TestCase):
    email = 'create@ye.rt'
    house_number = 2
    password = 'qwerty123'

    def setUp(self):
        pass


    def test_filter(self):
        form = UserCreationForm({
            'email': self.email,
            'house_number': self.house_number,
            'password1': self.password,
            'password2': self.password,
        })
        self.assertTrue(form.is_valid())
        comment = form.save()
        self.assertEqual(print(comment.email), print(self.email))
        self.assertEqual(comment.house_number, self.house_number)