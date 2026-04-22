import random
import os
from django.db import models


# code "method" for filepath
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1,39989876678)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "myPage/{new_filename}/{final_filename}".format(new_filename=new_filename,final_filename=final_filename)




# ============== myPage Models=====================
class myPage(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_image_path,null=True, blank=True)
    
    def __str__(self): 
        return self.title
