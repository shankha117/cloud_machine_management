from app.db.services.cluster import Cluster_Data_Layer
from app.db.services.instance import Instance_Data_Layer
from flask import current_app, jsonify


class Cluster_Service(object):

    def create_cluster(self, template: str, type: str, clustername: str,region: str, properties: dict):
        try:

            return Cluster_Data_Layer().create_cluster(template=template, type=type,region=region, clustername=clustername,
                                                       properties=properties)

        except Exception as e:
            raise Exception(str(e))

    def get_cluster(self, cluster_id):

        try:
            cluster_id = cluster_id

            data = Cluster_Data_Layer().get_cluster_details(cluster_id)
            if data:
                return data
            return {"message": "no cluster found"}

        except Exception as e:
            raise Exception(e)

    def get_all_clusters(self, order: str, tags: str, cluster_type: str, page: int, limit: int):

        try:
            data, count = Cluster_Data_Layer().get_all_cluster(order=order, tags=tags, type=cluster_type, page=page - 1,
                                                               limit=limit)
            next = True if count > (limit * page) else False

            res = {"data": data, "count": count, "more": next}

            return res

        except Exception as e:
            import traceback
            current_app.logger.error(traceback.format_exc())
            raise Exception(e)

    def delete_cluster(self, cluster_id: str):

        try:
            if not Cluster_Data_Layer().get_cluster_details(cluster_id):
                return jsonify({'error': 'no cluster with the id {0} exists'.format(cluster_id)}), 400

            # delete all child clusters
            Instance_Data_Layer().delete_all_instance_by_cluster_id(cluster_id=cluster_id)

            # delete the cluster document
            return Cluster_Data_Layer().delete_cluster(cluster_id=cluster_id)

        except Exception as e:
            import traceback
            current_app.logger.error(traceback.format_exc())
            raise Exception(e)

    def add_tags(self, cluster_id: str, tags: list):

        try:
            if not Cluster_Data_Layer().get_cluster_details(cluster_id):
                return jsonify({'error': 'no cluster with the id {0} exists'.format(cluster_id)}), 400

            result = Cluster_Data_Layer().add_tags(cluster_id=cluster_id, tags=tags)

            if result != 0:
                return jsonify({'message': '{0} cluster updated'.format(result)}), 200

            return jsonify({'error': 'Some tags might already be present. {0} cluster '
                                     'updated'.format(result)}), 200

        except Exception as e:
            import traceback
            current_app.logger.error(traceback.format_exc())
            raise Exception(e)

    def update_tags(self, cluster_id: str, key: str, value: str):

        try:
            if not Cluster_Data_Layer().get_cluster_details(cluster_id):
                return jsonify({'error': 'no cluster with the id {0} exists'.format(cluster_id)}), 400

            result = Cluster_Data_Layer().update_tag(cluster_id=cluster_id, key=key, value=value)

            if result != 0:
                return jsonify({'message': '{0} cluster updated'.format(result)}), 200

            return jsonify({'error': 'key to be updated not present Or has the same value provide.  {0} cluster '
                                     'updated .'.format(result)}), 200

        except Exception as e:
            import traceback
            current_app.logger.error(traceback.format_exc())
            raise Exception(e)

    def delete_tags(self, cluster_id: str, keys: list):

        try:
            if not Cluster_Data_Layer().get_cluster_details(cluster_id):
                return jsonify({'error': 'no cluster with the id {0} exists'.format(cluster_id)}), 400

            result = Cluster_Data_Layer().delete_tag(cluster_id=cluster_id, key_list=keys)

            if result != 0:
                return jsonify({'message': '{0} cluster updated'.format(result)}), 200

            return jsonify({'error': 'key or keys to be deleted not present.  {0} cluster '
                                     'updated .'.format(result)}), 200

        except Exception as e:
            import traceback
            current_app.logger.error(traceback.format_exc())
            raise Exception(e)
