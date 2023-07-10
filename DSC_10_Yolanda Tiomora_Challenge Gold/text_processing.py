import re
from flask import request, jsonify

def text_processing():
    text = request.form.get('text')

    json_response = {
        'status_code': 200,
        'description': "Teks yang telah diproses",
        'data': re.sub(r'[^a-zA-Z0-9]', ' ', text),
    }

    create_database_text(text)

    # membuat response JSON
    response = jsonify(json_response)
    return response