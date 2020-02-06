from app.db.dbmanager import db

def get_movie(id):
    """
    Given a movie ID, return a movie with that ID, with the comments for that
    movie embedded in the movie document. The comments are joined from the
    comments collection using expressive $lookup.
    """
    try:

        """
        Ticket: Get Comments
        Please implement a $lookup stage in this pipeline to find all the
        comments for the given movie. The movie_id in the `comments` collection
        can be used to refer to the _id from the `movies` collection.
        Embed the joined comments in a new field called "comments".
        """

        # : Get Comments
        # implement the required pipeline
        pipeline = [
            {
                "$match": {
                    "_id": ObjectId(id)
                }
            },
            {
                "$lookup": {
                    "from": 'comments',
                    "let": {'id': '$_id'},
                    "pipeline": [
                        {'$match':
                             {'$expr': {'$eq': ['$movie_id', '$$id']}}
                         }
                    ],
                    "as": 'comments'
                }
            }
        ]

        movie = db.movies.aggregate(pipeline).next()
        movie["comments"] = sorted(
            movie.get("comments", []),
            key=lambda c: c.get("date"),
            reverse=True
        )
        return movie


    # TODO: Error Handling
    # If an invalid ID is passed to `get_movie`, it should return None.
    except (StopIteration) as _:

        """
        Ticket: Error Handling

        Handle the InvalidId exception from the BSON library the same way as the
        StopIteration exception is handled. Both exceptions should result in
        `get_movie` returning None.
        """

        return None
    except InvalidId as _:
        return None

    except DuplicateKeyError as e:
        return None


    except Exception as e:
        return {}


def get_all_genres():
    """
    Returns list of all genres in the database.
    """
    return list(db.movies.aggregate([
        {"$unwind": "$genres"},
        {"$group": {"_id": None, "genres": {"$addToSet": "$genres"}}}
    ]))[0]["genres"]


"""
Ticket: Create/Update Comments

For this ticket, you will need to implement the following two methods:

- add_comment
- update_comment

You can find these methods below this docstring. Make sure to read the comments
to better understand the task.
"""


def add_comment(movie_id, user, comment, date):
    """
    Inserts a comment into the comments collection, with the following fields:
    - "name"
    - "email"
    - "movie_id"
    - "text"
    - "date"
    Name and email must be retrieved from the "user" object.
    """
    # : Create/Update Comments
    # construct the comment document to be inserted into MongoDB
    comment_doc = {
        "movie_id": ObjectId(movie_id),
        "name": user.name,
        "email": user.email,
        "text": comment,
        "date": date
    }

    return db.comments.insert_one(comment_doc)


def update_comment(comment_id, user_email, text, date):
    """
    Updates the comment in the comment collection. Queries for the comment
    based by both comment _id field as well as the email field to doubly ensure
    the user has permission to edit this comment.
    """
    # : Create/Update Comments
    # use the user_email and comment_id to select the proper comment
    # then update the "text" and "date" of the selected comment
    return db.comments.update_one(
        {"_id": comment_id, "email": user_email},
        {"$set": {"text": text, "date": date}}
    )


def delete_comment(comment_id, user_email):
    """
    Given a user's email and a comment ID, deletes a comment from the comments
    collection
    """

    """
    Ticket: Delete Comments

    Match the comment_id and user_email with the correct fields, to make sure
    this user has permission to delete this comment, and then delete it.
    """

    # TODO: Delete Comments
    # Use the user_email and comment_id to delete the proper comment.
    response = db.comments.delete_one({"_id": comment_id, "email": user_email})
    print("THIS IS FROM DELETE", response.deleted_count)
    return response


"""
Ticket: User Management

For this ticket, you will need to implement the following six methods:

- get_user
- add_user
- login_user
- logout_user
- get_user_session
- delete_user

You can find these methods below this docstring. Make sure to read the comments
to better understand the task.
"""


def get_user(email):
    """
    Given an email, returns a document from the `users` collection.
    """
    # TODO: User Management
    # Retrieve the user document corresponding with the user's email.
    return db.users.find_one({"email": email})


def add_user(name, email, hashedpw):
    """
    Given a name, email and password, inserts a document with those credentials
    to the `users` collection.
    """

    """
    Ticket: Durable Writes

    Please increase the durability of this method by using a non-default write
    concern with ``insert_one``.
    """

    try:
        # TODO: User Management
        # Insert a user with the "name", "email", and "password" fields.
        # TODO: Durable Writes
        # Use a more durable Write Concern for this operation.
        new_user = {"email": email, "name": name, "password": hashedpw}

        db.users.insert_one(new_user)

        return {"success": True}
    except DuplicateKeyError:
        return {"error": "A user with the given email already exists."}


def login_user(email, jwt):
    """
    Given an email and JWT, logs in a user by updating the JWT corresponding
    with that user's email in the `sessions` collection.

    In `sessions`, each user's email is stored in a field called "user_id".
    """
    try:
        # TODO: User Management
        # Use an UPSERT statement to update the "jwt" field in the document,
        # matching the "user_id" field with the email passed to this function.
        db.sessions.update_one({"user_id": email}, {"$set": {"jwt": jwt}}, upsert=True)
        return {"success": True}
    except Exception as e:
        return {"error": e}


def logout_user(email):
    """
    Given a user's email, logs out that user by deleting their corresponding
    entry in the `sessions` collection.

    In `sessions`, each user's email is stored in a field called "user_id".
    """
    try:
        # TODO: User Management
        # Delete the document in the `sessions` collection matching the email.
        db.sessions.delete_one({"user_id": email})
        return {"success": True}
    except Exception as e:
        return {"error": e}


def get_user_session(email):
    """
    Given a user's email, finds that user's session in `sessions`.

    In `sessions`, each user's email is stored in a field called "user_id".
    """
    try:
        # TODO: User Management
        # Retrieve the session document corresponding with the user's email.
        return db.sessions.find_one({"user_id": email})
    except Exception as e:
        return {"error": e}


def delete_user(email):
    """
    Given a user's email, deletes a user from the `users` collection and deletes
    that user's session from the `sessions` collection.
    """
    try:
        # : User Management
        # delete the corresponding documents from `users` and `sessions`
        db.sessions.delete_one({"user_id": email})
        db.users.delete_one({"email": email})
        if get_user(email) is None:
            return {"success": True}
        else:
            raise ValueError("Deletion unsuccessful")
    except Exception as e:
        return {"error": e}


def update_prefs(email, prefs):
    """
    Given a user's email and a dictionary of preferences, update that user's
    preferences.
    """
    prefs = {} if prefs is None else prefs
    try:

        """
        Ticket: User Preferences

        Update the "preferences" field in the corresponding user's document to
        reflect the information in prefs.
        """

        # TODO: User preferences
        # Use the data in "prefs" to update the user's preferences.
        response = db.users.update_one({"email": email}, {"$set": {"preferences": prefs}})
        if response.matched_count == 0:
            return {'error': 'no user found'}
        else:
            return response
    except Exception as e:
        return {'error': str(e)}


def most_active_commenters():
    """
    Returns a list of the top 20 most frequent commenters.
    """

    """
    Ticket: User Report

    Construct a pipeline to find the users who comment the most on MFlix, sort
    by the number of comments, and then only return the 20 documents with the
    highest values.

    No field projection necessary.
    """
    # TODO: User Report
    # Return the 20 users who have commented the most on MFlix.
    pipeline = []

    rc = db.comments.read_concern  # you may want to change this read concern!
    comments = db.comments.with_options(read_concern=rc)
    result = comments.aggregate(pipeline)
    return list(result)


def make_admin(email):
    """
    Supplied method
    Flags the supplied user an an admin
    """
    db.users.update_one({"email": email}, {"$set": {"isAdmin": True}})


def get_configuration():
    """
    Returns the following information configured for this client:

    - max connection pool size
    - write concern
    - database user role
    """

    try:
        role_info = db.command({'connectionStatus': 1}).get('authInfo').get(
            'authenticatedUserRoles')[0]
        return (db.client.max_pool_size, db.client.write_concern, role_info)
    except IndexError:
        return (db.client.max_pool_size, db.client.write_concern, {})
