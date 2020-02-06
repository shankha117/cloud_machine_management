from flask import jsonify, make_response, current_app
from . import cloud_manager


@cloud_manager.route('/cluster', methods=['POST'])
def create_cluster():
    current_app.logger.error('grolsh')
    return jsonify({'message': 'New user created!'})


@cloud_manager.route('/example/<cluster_id>', methods=['GET'])
def cluster_details(cluster_id):
    return make_response('Gooddsda Going', 200)


@cloud_manager.route('/example/<cluster_id>', methods=['DELETE'])
def delete_cluster(cluster_id):
    return make_response('Gooddsda Going', 200)
