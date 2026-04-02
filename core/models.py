from django.db import models, connection
import string
import random
import os

def generate_unique_code():
    while True:
        code = generate_short_code()
        if not URL.objects.filter(short_code=code).exists():
            return code
        
def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

BASE62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
Offset = int(os.environ.get("SECRETOFFSET", 100000))

def encode_base62(num: int) -> str:
    if num == 0:
        return BASE62[0]
    
    result = []
    while num:
        result.append(BASE62[num % 62])
        num //= 62
    return ''.join(reversed(result))
class URL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.IntegerField(default=0)

    def get_next_id(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT nextval('core_url_id_seq')")
            return cursor.fetchone()[0]
    
    def save(self, *args, **kwargs):
        if not self.short_code:
            next_id = self.get_next_id()
            self.short_code = encode_base62(next_id + Offset)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)