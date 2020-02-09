from flask import current_app, jsonify, abort
import random, socket, struct
import json
from app.db.services.instance import Instance_Data_Layer
from app.db.services.cluster import Cluster_Data_Layer
from app.db.fields.instance import Instance


class Instance_Service(object):

    def __init__(self):
        self.available_operations = ["ON", "OFF", "REBOOT"]

    def create_instance(self, cluster_id: str, type: str, instancename: str, keypair: dict, instancetype: str,
                        image: dict, tags: list, securitygroups: dict):
        try:

            if not Cluster_Data_Layer().get_cluster_details(cluster_id):
                return jsonify({'error': 'no cluster with the id {0} exists'.format(cluster_id)}), 400

            region = Cluster_Data_Layer().get_cluster_details(cluster_id=cluster_id)['region']

            random_ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

            data, count = Instance_Data_Layer().get_all_instance(state=None, cluster_id=cluster_id,
                                                                 instance_name=instancename,
                                                                 order=None, tags=None, instance_type=None, page=None,
                                                                 limit=None,
                                                                 project=None)

            if count > 0:
                raise Exception('the instance name {0} exists in cluster {1}'.format(instancename, cluster_id))

            return Instance_Data_Layer().create_instance(cluster_id=cluster_id, state="OFF", region=region, type=type,
                                                         instancename=instancename,
                                                         keypair=keypair, instancetype=instancetype,
                                                         ip=random_ip, image=image, tags=tags,
                                                         securitygroups=securitygroups)

        except Exception as e:
            raise Exception(str(e))

    def get_instance(self, instance_id):

        try:
            instance_id = instance_id

            data = Instance_Data_Layer().get_instance_details(instance_id=instance_id)
            if data:
                return data
            return {"message": "no instance found"}

        except Exception as e:
            raise Exception(e)

    def get_all_instances(self, order: str, tags: str, cluster_id: str, state: str, instance_type: str, page: int,
                          limit: int):

        try:
            data, count = Instance_Data_Layer().get_all_instance(order=order, cluster_id=cluster_id, state=state,
                                                                 tags=tags, instance_type=instance_type, page=page - 1,
                                                                 limit=limit, instance_name=None, project=None)
            next = True if count > (limit * page) else False

            res = {"data": data, "count": count, "more": next}

            return res

        except Exception as e:
            import traceback
            current_app.logger.error(traceback.format_exc())
            raise Exception(e)

    def validate_instance(self, instance_id):
        try:
            if not Instance_Data_Layer().get_instance_details(instance_id):
                abort(400, 'no instance with the id {0} exists'.format(instance_id))

        except Exception as e:
            import traceback
            current_app.logger.error(traceback.format_exc())
            raise Exception(e)

    def validate_operation(self, state):
        if state not in self.available_operations:
            abort(400, 'Available operations are {0}'.format(self.available_operations))

    def delete_instance(self, instance_id: str):
        try:
            self.validate_instance(instance_id=instance_id)
            return Instance_Data_Layer().delete_instance(instance_id=instance_id)

        except Exception as e:
            import traceback
            current_app.logger.error(traceback.format_exc())
            raise Exception(e)

    def delete_all_instance_by_cluster_id(self, cluster_id: str):
        try:
            if not Cluster_Data_Layer().get_cluster_details(cluster_id):
                return jsonify({'error': 'no cluster with the id {0} exists'.format(cluster_id)}), 400

            return Instance_Data_Layer().delete_all_instance_by_cluster_id(cluster_id=cluster_id)

        except Exception as e:
            import traceback
            current_app.logger.error(traceback.format_exc())
            raise Exception(e)

    def perform_task(self, instance_id: str, state: str):

        try:
            instance_data = Instance_Data_Layer().get_instance_details(instance_id=instance_id)

            if not instance_data:
                return jsonify({'error': 'no instance with the id {0} exists'.format(instance_id)}), 400

            self.validate_operation(state=state)

            if instance_data[Instance.state.value] == state:
                return jsonify({'error': 'instance {0} already in state {1}'.format(instance_id, state)}), 400

            result = Instance_Data_Layer().upadate_state(instance_id=instance_id, state=state)

            if result != 0:
                return jsonify({'error': 'Operation {0} performed on {1}'.format(state, instance_id)}), 200

        except Exception as e:
            import traceback
            current_app.logger.error(traceback.format_exc())
            raise Exception(e)

    def perform_bulk_task(self, tags: str, is_async: bool, operation: str, cluster_id: str, state: str,
                          instance_type: str):
        try:
            self.validate_operation(operation)

            if json.loads(is_async.lower()):
                return jsonify({'message': 'bulk operation accepted'}), 202

            data = Instance_Data_Layer().bulk_update(cluster_id=cluster_id, tags=tags, state=state, operation=operation,
                                                     instance_type=instance_type)

            if data != 0:
                return jsonify({'message': 'operation ``{0}`` successfully performed on total-{1} instances'.format(
                    operation, data)}), 200

            return jsonify({'error': '0 operations performed'}), 500

        except Exception as e:
            import traceback
            current_app.logger.error(traceback.format_exc())
            raise Exception(e)

    def add_tags(self, instance_id: str, tags: list):

        try:
            self.validate_instance(instance_id=instance_id)

            result = Instance_Data_Layer().add_tags(instance_id=instance_id, tags=tags)

            if result != 0:
                return jsonify({'message': '{0} instance updated'.format(result)}), 200

            return jsonify({'error': 'Some tags might already be present.If you wish to update tags use the UPDATE '
                                     'TAG API .  {0} instance '
                                     'updated'.format(result)}), 200

        except Exception as e:
            import traceback
            current_app.logger.error(traceback.format_exc())
            raise Exception(e)


    def update_tags(self, instance_id: str, key: str, value: str):

        try:
            self.validate_instance(instance_id=instance_id)

            result = Instance_Data_Layer().update_tag(instance_id=instance_id, key=key, value=value)

            if result != 0:
                return jsonify({'message': '{0} instance updated'.format(result)}), 200

            return jsonify({'error': 'key to be updated not present Or has the same value provide.  {0} instance '
                                     'updated .'.format(result)}), 200

        except Exception as e:
            import traceback
            current_app.logger.error(traceback.format_exc())
            raise Exception(e)


    def delete_tags(self, instance_id: str, keys: list):

        try:
            self.validate_instance(instance_id=instance_id)

            result = Instance_Data_Layer().delete_tag(instance_id=instance_id, key_list=keys)

            if result != 0:
                return jsonify({'message': '{0} instance updated'.format(result)}), 200

            return jsonify({'error': 'key or keys to be deleted not present.  {0} instance '
                                     'updated .'.format(result)}), 200

        except Exception as e:
            import traceback
            current_app.logger.error(traceback.format_exc())
            raise Exception(e)