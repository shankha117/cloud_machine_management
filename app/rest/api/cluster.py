from flask import jsonify, make_response, request, current_app
from . import cloud_manager
from werkzeug.exceptions import BadRequest, MethodNotAllowed
from app.rest.utils import expect, required_body, required_params
from app.rest.services.cluster_service import Cluster_Service
from app.db.services.cluster import Cluster

@cloud_manager.route('/cluster', methods=['POST'])
@required_body(fields=['type', 'clustername','region'])
def create_cluster():
    try:
        post_data = request.get_json()

        template = expect(post_data.get('templateformat'), str, 'templateformat')

        cluster_type = expect(post_data.get('type'), str, 'type')

        region = expect(post_data.get('region'),str,'region')

        clustername = expect(post_data.get('clustername'), str, 'clustername')

        properties = expect(post_data.get('properties'), dict, 'properties')

        inserted_id = Cluster_Service().create_cluster(template=template, type=cluster_type,region=region,
                                                       clustername=clustername, properties=properties)

        return jsonify({'message': 'cluster created', 'cluster_id': inserted_id}), 200

    except BadRequest as ex:

        return jsonify({'message': str(ex)}), 400

    except Exception as ex:

        return jsonify({'message': str(ex)}), 500


@cloud_manager.route('/cluster', methods=['GET'])
@required_params(fields=["page", "limit"])
def get_all_cluster():
    try:

        order = expect(request.args.get('order', default='desc'), str, 'order')

        tags = expect(request.args.get('tags'), str, 'tags')

        limit = expect(int(request.args.get('limit')), int, 'limit')

        page = expect(int(request.args.get('page')), int, 'page')

        cluster_type = expect(request.args.get('type'), str, 'type')

        res = Cluster_Service().get_all_clusters(order=order, tags=tags, page=page, limit=limit,
                                                 cluster_type=cluster_type)

        return jsonify(res), 200

    except BadRequest as ex:

        return jsonify({'message': str(ex)}), 400

    except Exception as ex:
        import traceback

        return jsonify({'message': str(ex)}), 500


@cloud_manager.route('/cluster/<cluster_id>', methods=['GET'])
def cluster_details(cluster_id):
    try:
        cluster_id = expect(cluster_id, str, 'cluster_id')

        cluster_details = Cluster_Service().get_cluster(cluster_id)

        return jsonify(cluster_details), 200

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@cloud_manager.route('/cluster/<cluster_id>', methods=['DELETE'])
def delete_cluster(cluster_id):
    try:
        res = Cluster_Service().delete_cluster(cluster_id=cluster_id)

        if res:
            return jsonify({'message': 'cluster {0} deleted'.format(cluster_id)}), 200

    except Exception as ex:

        return jsonify({'message': str(ex)}), 500


@cloud_manager.route('/cluster/<cluster_id>/tags', methods=['POST'])
@required_body(fields=['tags'])
def add_cluster_tags(cluster_id):
    try:
        post_data = request.get_json()

        tags = expect(post_data.get('tags'), list, 'tags')

        return Cluster_Service().add_tags(cluster_id=cluster_id, tags=tags)

    except Exception as ex:

        return jsonify({'message': str(ex)}), 500


@cloud_manager.route('/cluster/<cluster_id>/tags', methods=['PUT'])
@required_body(fields=['key','value'])
def update_cluster_tags(cluster_id):
    try:
        post_data = request.get_json()

        key = expect(post_data.get('key'), str, 'key')

        value = expect(post_data.get('value'), str, 'value')

        return Cluster_Service().update_tags(cluster_id=cluster_id, key=key, value=value)

    except Exception as ex:

        return jsonify({'message': str(ex)}), 500


@cloud_manager.route('/cluster/<cluster_id>/tags', methods=['DELETE'])
def delete_cluster_tags(cluster_id):
    try:
        keys = expect(request.args.get('tags'), str, 'tags')

        return Cluster_Service().delete_tags(cluster_id=cluster_id, keys=eval(keys))

    except Exception as ex:

        return jsonify({'message': str(ex)}), 500