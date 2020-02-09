from datetime import datetime
from app.db.mongo_db_model import Model
from flask import current_app
from app.db.fields.instance import Instance
from bson.objectid import ObjectId


class Instance_Data_Layer(Model):

    def __init__(self):

        self._collection = 'instance'

    def create_instance(self, cluster_id: str, type: str, region: str, instancename: str, keypair: dict,
                        instancetype: str, state: str,
                        ip: str, image: dict, tags: list, securitygroups: dict):
        try:

            doc = {
                Instance.cluster_id.value: ObjectId(cluster_id),
                Instance.region.value: region,
                Instance.instancename.value: instancename,
                Instance.type.value: type,
                Instance.state.value: state,
                Instance.properties.value: {
                    Instance.image.value['rel']: image,
                    Instance.keypair.value['rel']: keypair,
                    Instance.instancetype.value['rel']: instancetype,
                    Instance.securitygroups.value['rel']: securitygroups,
                    Instance.tags.value['rel']: tags,
                    Instance.ip.value['rel']: ip
                },
                Instance.created_date.value: datetime.now(),
                Instance.updated_date.value: datetime.now()

            }
            data = self.save(doc, index=None)
            instance_id = data.inserted_id

            current_app.logger.info("instance created {0}".format(instance_id))
            return instance_id

        except Exception as e:
            import traceback
            current_app.logger.error(traceback.format_exc())
            raise Exception(e)

    def get_instance_details(self, instance_id):

        try:

            data = self.search_one(instance_id)
            return data

        except Exception as e:
            current_app.logger.error(e)
            raise Exception(e)

    def make_match_query_for_search(self, cluster_id: str, tags: list, state: str, instance_type: str,
                                    instance_name: str):
        match = {}
        if state:
            match[Instance.state.value] = state
        if instance_name:
            match[Instance.instancename.value] = instance_name
        if cluster_id:
            match[Instance.cluster_id.value] = ObjectId(cluster_id)
        if tags:
            all_array = []
            for i in eval(tags):
                all_array.append({"$elemMatch": i})

            match[Instance.tags.value['abs']] = {"$all": all_array}

        if instance_type:
            match[Instance.instancetype.value['abs']] = instance_type

        return match

    def get_all_instance(self, cluster_id: str, state: str, order: str, tags: list, instance_type: str,
                         instance_name: str, page: int,
                         limit: int, project: dict):

        try:

            match = self.make_match_query_for_search(cluster_id=cluster_id, state=state, tags=tags,
                                                     instance_type=instance_type,
                                                     instance_name=instance_name)

            data, count = self.search_bulk(match=match, order=order, page=page, limit=limit, project=project)

            return data, count

        except Exception as e:
            current_app.logger.error(e)
            raise Exception(e)

    def delete_instance(self, instance_id: str):

        try:

            query = {"_id": ObjectId(instance_id)}

            return self.delete_one(query)

        except Exception as e:
            current_app.logger.error(e)
            raise Exception(e)

    def delete_all_instance_by_cluster_id(self, cluster_id):
        try:
            query = {Instance.cluster_id.value: ObjectId(cluster_id)}

            return self.delete_many(query)

        except Exception as e:
            current_app.logger.error(e)
            raise Exception(e)

    """
    update the instance state
    """

    def upadate_state(self, instance_id: str, state: str):

        try:
            set_query = {"$set": {Instance.state.value: state}}

            return self.update_one(id=instance_id, match_query={}, set_query=set_query)

        except Exception as e:
            current_app.logger.error(e)
            raise Exception(e)

    def bulk_update(self, cluster_id: str, tags: list, state: str, operation: str, instance_type: str):
        try:
            match_query = self.make_match_query_for_search(cluster_id=cluster_id, state=state, tags=tags,
                                                           instance_type=instance_type,
                                                           instance_name=None)

            set_query = {"$set": {Instance.state.value: operation}}

            return self.update_many(search_query=match_query, set_query=set_query)

        except Exception as e:
            current_app.logger.error(e)
            raise Exception(e)

    def add_tags(self, instance_id: str, tags: list):

        try:
            tags_list = list(i[Instance.tags_key.value['rel']] for i in tags)

            query_string = {Instance.tags_key.value['abs']: {"$nin": tags_list}}

            set_query = {"$addToSet": {Instance.tags.value['abs']: {"$each": tags}}}

            return self.update_one(id=instance_id, match_query=query_string, set_query=set_query)

        except Exception as e:
            current_app.logger.error(e)
            raise Exception(e)


    def update_tag(self, instance_id: str, key: str, value: str):

        try:
            query_string = {Instance.tags.value['abs']: {"$elemMatch": {Instance.tags_key.value['rel']: key}}}

            set_query = {"$set": {Instance.tags.value['abs'] + ".$." + Instance.tags_value.value['rel']: value}}

            return self.update_one(id=instance_id, match_query=query_string, set_query=set_query)

        except Exception as e:
            current_app.logger.error(e)
            raise Exception(e)


    def delete_tag(self, instance_id: str, key_list: list):

        try:
            query_string = {}

            set_query = {"$pull": {Instance.tags.value['abs']: {Instance.tags_key.value['rel']:
                                                                   {"$in": key_list}}}}

            return self.update_one(id=instance_id, match_query=query_string, set_query=set_query)

        except Exception as e:
            current_app.logger.error(e)
            raise Exception(e)