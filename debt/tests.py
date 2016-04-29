from django.test import TestCase
from debt.models import DebtType, Debt
# Create your tests here.



class Debt_test(TestCase):
    title = 'create_note'
    text = '<p> good </p>'
    category_name = 'TODO'
    def setUp(self):
        DebtType.objects.create(name=self.category_name, slung='test')
        Debt.objects.create(
             type=DebtType.objects.get(name=self.category_name),
             year=2014,
             month=2,
             amount='1020.32',
        )




    def test_filter(self):
        # print(self.title)
        self.assertEqual(print(Debt.objects.get(year='2014')),
                         print('2014'))
        self.assertEqual(print(DebtType.objects.get(name=self.category_name)),
                         print(self.category_name))
