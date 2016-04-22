from django.db import models

# Create your models here.

class DebtType(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    slung = models.SlugField(unique=True)

    # text = RichTextField(null=True, blank=True)
    # date_added = models.DateTimeField(auto_now_add=True)
    # date_modified = models.DateTimeField(auto_now=True)
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    # favorites = models.BooleanField(default=False)
    # category = models.ForeignKey(Category, blank=True,
    #                              null=True, related_name='cat')
    # publish = models.BooleanField(default=False)

    def __str__(self):
        return self.name
