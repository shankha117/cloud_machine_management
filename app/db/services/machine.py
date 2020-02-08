from app.db.mongo_db_model import Model
from flask import current_app


class Instance_Data_Layer(Model):

    def __init__(self):

        self._collection = 'instance'

    def create_cluster(self, data):

        try:
            data = self.save(data)
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

    def make_match_query_for_search(self,cluster_id: str,tags: list, type: str):
        match = {}

        if cluster_id:
            match['cluster_id'] = cluster_id
        if tags:
            all_array = []
            for i in eval(tags):
                all_array.append({"$elemMatch": i})

            match["properties.Tags"] = {"$all": all_array}

        if type:
            match["type"] = type

        return match

    def get_all_machine(self, cluster_id: str, order: str, tags: list, type: str, page: int, limit: int, project: dict):

        try:

            match = self.make_match_query(cluster_id=cluster_id,tags=tags,type=type)

            data, count = self.search_bulk(match=match, order=order, page=page, limit=limit, project= dict)

            return data, count

        except Exception as e:
            current_app.logger.error(e)
            raise Exception(e)

    def delete_machine(self,cluster_id: str):

        pass



