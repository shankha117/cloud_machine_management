from app.db.dbmanager import db
from bson.objectid import ObjectId
from bson.errors import InvalidId
from pymongo import DESCENDING, ASCENDING, errors
from flask import current_app
from werkzeug.local import LocalProxy


class Model(object):

    def __init__(self, collection_name):
        self._collection = None

    def save(self, data, index, query=None) -> object:
        try:
            if index:
                db[self._collection].create_index(index, unique=True)

            return db[self._collection].insert_one(data)

        except errors.DuplicateKeyError:
            raise Exception('{0} -  {1} already exists'.format(index, data[index]))

    def bulk_save(self, data):
        pass

    def search_one(self, id) -> dict:

        try:
            pipeline = [
                {
                    "$match": {
                        "_id": ObjectId(id)
                    }
                }]

            return db[self._collection].aggregate(pipeline).next()

        except (StopIteration) as _:
            return None
        except InvalidId as e:
            raise Exception(str(e))

    def search_bulk(self, order: str, match: dict, page: int, limit: int, project: dict):
        try:
            pipeline = []
            count = 0
            sort = {"created_date": DESCENDING}
            if order == 'asc':
                sort["created_date"] = ASCENDING

            # match aggregation pipe
            pipeline.extend([
                {
                    "$match": match
                },
                {
                    "$sort": sort
                }
            ])
            if project:
                pipeline.append(
                    {
                        "$project": project
                    }
                )

            # count stage pipeline
            counting = pipeline[:]
            count_stage = {"$count": "count"}
            counting.append(count_stage)

            # pagination stage
            if limit != None and page != None:
                skip_stage = {"$skip": limit * page}

                limit_stage = {"$limit": limit}

                pipeline.append(skip_stage)
                pipeline.append(limit_stage)

            current_app.logger.info("this is the pipeline--->{0}".format(pipeline))

            data = list(db[self._collection].aggregate(pipeline, allowDiskUse=True))
            if data:
                count = list(db[self._collection].aggregate(counting, allowDiskUse=True))[
                    0].get("count")

            return data, count

        except (StopIteration) as _:
            return None

        except Exception as e:
            import traceback
            current_app.logger.error(traceback.format_exc())
            raise Exception(e)

    def update_one(self, id: str, match_query: dict, set_query: dict):

        try:
            query = {"_id": ObjectId(id)}
            if match_query:
                query.update(match_query)

            updated = db[self._collection].update_one(query, set_query, False, True)

            return updated.modified_count

        except Exception as e:
            import traceback
            current_app.logger.error(traceback.format_exc())
            raise Exception(e)

    def update_many(self, search_query: dict, set_query: dict):
        try:

            result = db[self._collection].update_many(search_query, set_query)

            return result.modified_count

        except Exception as e:
            raise Exception(e)

    def delete_one(self, query: dict):
        try:
            db[self._collection].delete_one(query)
            return True
        except Exception as e:
            raise Exception(e)

    def delete_many(self, query: dict):
        try:
            db[self._collection].delete_many(query)
            return True
        except Exception as e:
            raise Exception(e)
