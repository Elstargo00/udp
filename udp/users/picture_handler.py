# udp/users/picture_handler.py

import os
from PIL import Image
from flask import url_for, current_app

def add_profile_picture(upload_picture, email):
    fn = upload_picture.filename
    ext_type = fn.split('.')[-1]
    storage_filename = str(email) + '.' + ext_type
    filepath = os.path.join(current_app.root_path, 'static/profile_pictures', storage_filename)
    output_size = (200,200)
    pic = Image.open(upload_picture)
    pic.thumbnail(output_size)
    pic.save(filepath)
    return storage_filename
