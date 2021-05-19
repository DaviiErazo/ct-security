import os
import requests

from logging import info
from flask import Blueprint, request, make_response
from flask_cors import CORS

bp = Blueprint("api", __name__, url_prefix="/api")
CORS(bp)

V1_VERIFY_RECAPTCHA = "v1/verify/recaptcha"
URI_GOOGLE = os.environ.get('URI_GOOGLE') or 'https://www.google.com/recaptcha/api/siteverify'
SECRET_KEY = os.environ.get('SECRET_KEY') or ''


@bp.route(V1_VERIFY_RECAPTCHA, methods=["POST"])
def verify_recaptcha():
    try:
        token = request.get_json()['token']

        if not token:
            return make_response({'message': 'Token not provider'}), 400

        payload = {
            'secret': SECRET_KEY,
            'response': token,
        }

        response = requests.post(URI_GOOGLE, data=payload)
        result = response.json()

        return make_response(result)

    except Exception as e:
        error = str(e.args)
        return make_response({'Error': error}), 500



