from flask_app.config.mysqlconnection import connectToMySQL
from flask import session 
from flask_app.models.user_model import User
from flask_app import DATABASE

class Excel:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.created_at = data['created_at'] 
        self.updated_at = data ['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def create(cls, form):

        data= {
            **form,
            'user_id' : session['uid']
        }

        query = """
        INSERT INTO movies
        (
            title,
            user_id
        )

        VALUES(
            %(title)s,
            %(user_id)s
        )
        """

        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_with_users(cls):

        query = """
        SELECT * FROM excels 
        JOIN users ON users.id=excels.user_id;
"""

        results = connectToMySQL(DATABASE).query_db(query)

        excels = []
        for result in results:
            excel = cls(result)

            user_data = {
                **result,
                'id' : result['users.id'],
                'created_at' : result['users.created_at'],
                'updated_at' : result['users.updated_at']
            }


            excel.user = User(user_data)
            excels.append(excel)

        return excels


    @classmethod
    def find_one_by_id(cls, id):

        data = {
            'id' : id
        }

        query = """
        SELECT * FROM excels 
        WHERE id  = %(id)s
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            return cls(results[0])
        else:
            return False
        

    @classmethod
    def delete_by_id(cls, id):

        data = {
            'id' : id
        }

        query = """
        DELETE FROM excels WHERE id = %(id)s
        """

        return  connectToMySQL(DATABASE).query_db(query, data)
    @classmethod
    def save(cls, data):

        query = """
            UPDATE excels SET 
            title = %(title)s,
            WHERE id = %(id)s
        """
        return  connectToMySQL(DATABASE).query_db(query, data)