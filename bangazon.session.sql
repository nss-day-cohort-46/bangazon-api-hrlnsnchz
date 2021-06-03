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
    seller.id = Bang_C.user_id;