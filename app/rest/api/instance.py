from flask import jsonify, make_response
from . import cloud_manager


@cloud_manager.route('/machine', methods=['POST'])
def create_machine():
    current_user = "Shankha"
    public_id = "1236"
    return make_response(jsonify({'user': current_user, 'id': public_id, 'params_id': id}), 200)


@cloud_manager.route('/machine/<machine_id>', methods=['POST'])
def perform_task(machine_id):
    current_user = "Shankha"
    public_id = "1236"
    return make_response(jsonify({'user': current_user, 'id': public_id, 'params_id': id}), 200)


@cloud_manager.route('/machine/<machine_id>', methods=['GET'])
def machine_details(machine_id):
    current_user = "Shankha"
    public_id = "1236"
    return make_response(jsonify({'user': current_user, 'id': public_id, 'params_id': id}), 200)


@cloud_manager.route('/machine/<machine_id>', methods=['DELETE'])
def delete_machine(machine_id):
    current_user = "Shankha"
    public_id = "1236"
    return make_response(jsonify({'user': current_user, 'id': public_id, 'params_id': id}), 200)


@cloud_manager.route('/machine/<machine_id>', methods=['PUT'])
def modify_machine(machine_id):
    current_user = "Shankha"
    public_id = "1236"
    return make_response(jsonify({'user': current_user, 'id': public_id, 'params_id': id}), 200)
