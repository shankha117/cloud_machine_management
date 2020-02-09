from flask import jsonify, make_response, request, current_app
from . import cloud_manager
from werkzeug.exceptions import BadRequest, MethodNotAllowed
from app.rest.utils import expect, required_body, required_params
from app.rest.services.instance_service import Instance_Service


@cloud_manager.route('/instance', methods=['POST'])
@required_body(fields=["cluster_id", "type", "instance_name", "keypair"])
def create_instance():
    try:
        post_data = request.get_json()

        cluster_id = expect(post_data.get('cluster_id'), str, 'cluster_id')

        type = expect(post_data.get('type'), str, 'type')

        instance_type = expect(post_data.get('instance_type'), str, 'instance_type')

        instance_name = expect(post_data.get('instance_name'), str, 'instance_name')

        keypair = expect(post_data.get('keypair'), dict, 'keypair')

        image = expect(post_data.get('image'), dict, 'image')

        tags = expect(post_data.get('tags'), list, 'tags')

        security_groups = expect(post_data.get('security_groups'), dict, 'security_groups', {"name": "Default"})

        instance_id = Instance_Service().create_instance(cluster_id=cluster_id, type=type, instancetype=instance_type,
                                                         instancename=instance_name,
                                                         keypair=keypair, image=image, tags=tags,
                                                         securitygroups=security_groups)

        return jsonify({'message': 'instance created', 'instance_id': instance_id}), 200

    except BadRequest as ex:

        return jsonify({'message': str(ex)}), 400

    except Exception as ex:

        return jsonify({'error': str(ex)}), 500


@cloud_manager.route('/instance', methods=['GET'])
@required_params(fields=["page", "limit"])
def get_all_instance():
    try:

        order = expect(request.args.get('order', default='desc'), str, 'order')

        cluster_id = expect(request.args.get('cluster_id'), str, 'cluster_id')

        tags = expect(request.args.get('tags'), str, 'tags')

        state = expect(request.args.get('state'), str, 'state')

        limit = expect(int(request.args.get('limit')), int, 'limit')

        page = expect(int(request.args.get('page')), int, 'page')

        instance_type = expect(request.args.get('type'), str, 'type')

        res = Instance_Service().get_all_instances(cluster_id=cluster_id,
                                                   state=state,
                                                   order=order, tags=tags, page=page, limit=limit,
                                                   instance_type=instance_type)

        return jsonify(res), 200

    except BadRequest as ex:

        return jsonify({'message': str(ex)}), 400

    except Exception as ex:
        import traceback

        return jsonify({'message': str(ex)}), 500


@cloud_manager.route('/instance/<instance_id>', methods=['GET'])
def instance_details(instance_id):
    try:
        instance_id = expect(instance_id, str, 'instance_id')

        instance_details = Instance_Service().get_instance(instance_id=instance_id)

        return jsonify(instance_details), 200

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@cloud_manager.route('/instance/<instance_id>', methods=['DELETE'])
def delete_instance(instance_id):
    try:
        res = Instance_Service().delete_instance(instance_id=instance_id)

        if res:
            return jsonify({'message': 'instance {0} deleted'.format(instance_id)}), 200

    except Exception as ex:

        return jsonify({'message': str(ex)}), 500


@cloud_manager.route('/instance/<instance_id>', methods=['POST'])
@required_body(fields=["task"])
def perform_task(instance_id):
    try:
        post_data = request.get_json()

        task = expect(post_data.get('task'), str, 'task')

        return Instance_Service().perform_task(instance_id=instance_id, state=task)

    except Exception as ex:

        return jsonify({'message': str(ex)}), 500


@cloud_manager.route('/instance/bulk', methods=['POST'])
@required_params(fields=["operation"])
def perform_bulk_task():
    try:

        is_async = expect(request.args.get('is_async', default="True"), str, 'is_async')

        operation = expect(request.args.get('operation'), str, 'operation')

        cluster_id = expect(request.args.get('cluster_id'), str, 'cluster_id')

        tags = expect(request.args.get('tags'), str, 'tags')

        state = expect(request.args.get('state'), str, 'state')

        instance_type = expect(request.args.get('type'), str, 'type')

        res = Instance_Service().perform_bulk_task(cluster_id=cluster_id, is_async=is_async,
                                                   state=state, operation=operation,
                                                   tags=tags, instance_type=instance_type)

        return res

    except BadRequest as ex:

        return jsonify({'message': str(ex)}), 400

    except Exception as ex:
        import traceback

        return jsonify({'message': str(ex)}), 500


@cloud_manager.route('/instance/<instance_id>/tags', methods=['POST'])
@required_body(fields=['tags'])
def add_instance_tags(instance_id):
    try:
        post_data = request.get_json()

        tags = expect(post_data.get('tags'), list, 'tags')

        return Instance_Service().add_tags(instance_id=instance_id, tags=tags)

    except Exception as ex:

        return jsonify({'message': str(ex)}), 500

@cloud_manager.route('/instance/<instance_id>/tags', methods=['PUT'])
@required_body(fields=['key','value'])
def update_instance_tags(instance_id):
    try:
        post_data = request.get_json()

        key = expect(post_data.get('key'), str, 'key')

        value = expect(post_data.get('value'), str, 'value')

        return Instance_Service().update_tags(instance_id=instance_id, key=key, value=value)

    except Exception as ex:

        return jsonify({'message': str(ex)}), 500


@cloud_manager.route('/instance/<instance_id>/tags', methods=['DELETE'])
def delete_instance_tags(instance_id):
    try:

        keys = expect(request.args.get('tags'), str, 'tags')

        return Instance_Service().delete_tags(instance_id=instance_id, keys=eval(keys))

    except Exception as ex:

        return jsonify({'message': str(ex)}), 500