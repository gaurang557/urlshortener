from django.db import models
import string
import random

def generate_unique_code():
    while True:
        code = generate_short_code()
        if not URL.objects.filter(short_code=code).exists():
            return code
        
def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

class URL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = generate_unique_code()
        super().save(*args, **kwargs)