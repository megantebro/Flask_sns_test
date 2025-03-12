import os
import time

from werkzeug.utils import secure_filename


def save_file(file,filename):
    filename = str(int(time.time())) + filename
    file.save(f"./static/uploads/{filename}")
    return filename