"""Module for generating sellers by user report"""
import sqlite3
from django.shortcuts import render
from bangazonapi.models import Favorite
from bangazonreports.views import Connection


def user_fav_seller_list(request):
    """Function to build an HTML report of sellers by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all sellers, with related user info.
            db_cursor.execute("""
                SELECT
                    fav_table.id fav_table_id,
                    fav_table.customer_id,
                    fav_table.seller_id,
                    u.first_name || ' ' || u.last_name customer_full_name,
                    seller.first_name || ' ' || seller.last_name seller_full_name
                FROM
                    bangazonapi_favorite fav_table
                JOIN 
                    bangazonapi_customer BC 
                ON 
                    fav_table.customer_id = BC.id
                JOIN 
                    bangazonapi_customer Bang_C
                ON 
                    fav_table.seller_id = Bang_C.id
                JOIN 
                    auth_user u
                ON 
                    u.id = BC.user_id
                JOIN 
                    auth_user seller
                ON 
                    seller.id = Bang_C.user_id
            """)

            dataset = db_cursor.fetchall()

            # Take the flat data from the database, and build the
            # following data structure for each user.
            #
            # {
            #     1: {
            #         "customer_id": 1,
            #         "customer_full_name": "Brenda Mathews",
            #         "sellers": [
            #             {
            #                 "seller_id": 5,
            #                 "seller_full_name": "Joe Shepherd",
            #             }
            #         ]
            #     }
            # }

            fav_sellers_by_customer = {}

            for row in dataset:
                # Crete a seller instance and set its properties
                seller = Favorite()
                seller.seller_full_name = row["seller_full_name"]
                # Store the user's id
                uid = row["customer_id"]

                # If the user's id is already a key in the dictionary...
                if uid in fav_sellers_by_customer:

                    # Add the current seller to the `sellers` list for it
                    fav_sellers_by_customer[uid]['sellers'].append(seller)

                else:
                    # Otherwise, create the key and dictionary value
                    fav_sellers_by_customer[uid] = {}
                    fav_sellers_by_customer[uid]["id"] = uid
                    fav_sellers_by_customer[uid]["customer_full_name"] = row["customer_full_name"]
                    fav_sellers_by_customer[uid]["sellers"] = [seller]

        # Get only the values from the dictionary and create a list from them
        list_of_users_with_sellers = fav_sellers_by_customer.values()

        # Specify the Django template and provide data context
        template = 'users/list_with_sellers.html'
        context = {
            'user_fav_seller_list': list_of_users_with_sellers
        }

        return render(request, template, context)
