from telnetlib import STATUS
from django.db import models

# Create your models here.
class Task(models.Model):

    STATUS =(
        ('fazendo', 'Fazendo'),
        ('pronto', 'Pronto'),
    )

    title = models.CharField(max_length=255)
    descricao = models.TextField()
    done = models.CharField(
        max_length=7,
        choices=STATUS
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
