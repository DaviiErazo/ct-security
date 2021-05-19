import os
import requests

from logging import info
from flask import Blueprint, jsonify, request, make_response
from flask_cors import CORS

bp = Blueprint("api", __name__, url_prefix="/api")
CORS(bp)

V1_VERIFY_RECAPTCHA = "v1/verify/recaptcha"
URI_GOOGLE = os.environ.get('URI_GOOGLE') or 'https://www.google.com/recaptcha/api/siteverify?secret='
SECRET_KEY = os.environ.get('SECRET_KEY') or ''


@bp.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@bp.route(V1_VERIFY_RECAPTCHA, methods=["POST"])
def verify_recaptcha():
    try:
        token = request.form.get('token')

        if not token:
            return make_response({'message': 'Token not provider'}), 400

        recaptcha_url = f'{URI_GOOGLE}{SECRET_KEY}&response={token}'
        response = requests.post(recaptcha_url)

        info(response.json())
        return make_response({'message': 'success'})

    except Exception as e:
        error = str(e.args)
        return make_response({'Error': error}), 500



