from app.db.mongo_db_model import Model
from flask import current_app
from datetime import datetime
from app.db.services.machine import Instance_Data_Layer
from bson.objectid import ObjectId

# TODO read all the cluster keys from ENUM, this is must


class Cluster_Data_Layer(Model):

    def __init__(self):

        self._collection = 'cluster'

    def create_cluster(self, template: str, type: str, clustername: str, properties: dict):

        try:
            doc = {
                "template": template,
                "type": type,
                "clustername": clustername,
                "properties": properties,
                "created_date": datetime.now(),
                "updated_date": datetime.now()
            }

            data = self.save(doc,index="clustername")

            cluster_id = data.inserted_id

            current_app.logger.info("cluster created {0}".format(cluster_id))

            return cluster_id

        except Exception as e:
            current_app.logger.error(e)
            raise Exception(e)

    def get_cluster_details(self, cluster_id):

        try:

            data = self.search_one(cluster_id)
            return data

        except Exception as e:
            current_app.logger.error(e)
            raise Exception(e)

    def get_all_cluster(self, order: str, tags: list, type: str, page: int, limit: int):

        try:
            match = {}

            if tags:
                all_array = []
                for i in eval(tags):
                    all_array.append({"$elemMatch": i})

                match["properties.Tags"] = {"$all": all_array}

            if type:
                match["type"] = type

            data, count = self.search_bulk(match=match, order=order, page=page, limit=limit, project={})

            return data, count

        except Exception as e:
            current_app.logger.error(e)
            raise Exception(e)

    def delete_cluster(self,cluster_id: str):

        try:

            query = {"_id":ObjectId(cluster_id)}

            return self.delete_one(query)

        except Exception as e:
            current_app.logger.error(e)
            raise Exception(e)

    def add_tags(self,cluster_id: str, tags: list):

        try:
            tags_list = list(i["key"] for i in tags)

            query_string  = {"properties.Tags.key" : {"$nin" : tags_list }}

            set_query ={"$addToSet" : {"properties.Tags" :{"$each": tags } } }

            return self.update_one(id=cluster_id, match_query=query_string,set_query=set_query)

        except Exception as e:
            current_app.logger.error(e)
            raise Exception(e)

    def update_tag(self,cluster_id: str, key: str,value: str):

        try:
            query_string  = {"properties.Tags": { "$elemMatch": { "Key": key} }}

            set_query = { "$set": { "properties.Tags.$.Value" : value } }

            return self.update_one(cluster_id=cluster_id, match_query=query_string,set_query=set_query)

        except Exception as e:
            current_app.logger.error(e)
            raise Exception(e)