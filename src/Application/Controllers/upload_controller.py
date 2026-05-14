from flask import request, jsonify, make_response, current_app
from flask_jwt_extended import jwt_required
import os, uuid

ALLOWED = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED

class UploadController:

    @staticmethod
    @jwt_required()
    def upload_image():
        if 'file' not in request.files:
            return make_response(jsonify({"erro": "Nenhum arquivo enviado"}), 400)

        file = request.files['file']

        if file.filename == '':
            return make_response(jsonify({"erro": "Arquivo inválido"}), 400)

        if not allowed(file.filename):
            return make_response(jsonify({"erro": "Formato não permitido. Use PNG, JPG, JPEG, GIF ou WEBP"}), 400)

        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(path)

        url = f"/static/uploads/{filename}"
        return make_response(jsonify({"url": url}), 201)
