import os

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def save_uploaded_file(file):
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join('uploads', filename))
        return filename
    else:
        return None
