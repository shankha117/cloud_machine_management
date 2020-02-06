from flask import jsonify, make_response
from . import cloud_manager


@cloud_manager.route('/bulk/<tag>', methods=['POST'])
def bulk_task(tag):
    current_user = "Shankha"
    public_id = "1236"
    return make_response(jsonify({'user': current_user, 'id': public_id, 'params_id': id}), 200)


