import mysql.connector
from datetime import datetime
from decouple import config

frip_db = mysql.connector.connect(
  host=config('DB_HOST'),
  user=config('DB_USERNAME'),
  passwd=config('DB_PASSWORD'),
  database=config('DB_DATABASE')
)

#  sql = "INSERT INTO orders (order_id,filled,price,symbol_id,side,quantity,created_at,updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
#     val = order_id,"false",order['price'],pair_id,side,config('QUANTITY'),current_time,current_time
    
    
#      sql_b = "SELECT symbols.id,orders.filled FROM orders LEFT JOIN symbols ON orders.symbol_id = symbols.id   WHERE orders.filled = 'false'"
#     cur.execute(sql_b)


#     new_cat.append(t.lower())
# categories
# category_filterable_attributes
# category_translations
# product_categories

# tax_categories
# tax_categories_tax_rates

cur = frip_db.cursor(dictionary=True)
cur.execute("select `cat`.`id` as `category_id`, `ct`.`name`, `cat`.`position`, `cat`.`status`, `ct`.`locale`, COUNT(DISTINCT pc.product_id) as count from `categories` as `cat` left join `category_translations` as `ct` on `cat`.`id` = `ct`.`category_id` and `ct`.`locale` in ('fr') left join `product_categories` as `pc` on `cat`.`id` = `pc`.`category_id` group by `cat`.`id`, `ct`.`locale` order by `category_id` desc limit 10 offset 0")
existent_category = cur.fetchall()
#print(existent_category)
ex_cat =[]
for line in existent_category:
    ex_cat.append(line['name'].lower())
    
cur = frip_db.cursor(dictionary=True)
cur.execute("select distinct `product_flat`.`locale`,`product_flat`.`product_id`, `product_flat`.`channel`, `product_images`.`path` as `base_image`, `pc`.`category_id`, `ct`.`name` as `category_name`, `product_flat`.`product_id`, `product_flat`.`sku`, `product_flat`.`name`, `product_flat`.`type`, `product_flat`.`status`, `product_flat`.`price`, `product_flat`.`url_key`, `product_flat`.`visible_individually`, `af`.`name` as `attribute_family`, SUM(DISTINCT product_inventories.qty) as quantity, COUNT(DISTINCT product_images.id) as images_count from `product_flat` left join `attribute_families` as `af` on `product_flat`.`attribute_family_id` = `af`.`id` left join `product_inventories` on `product_flat`.`product_id` = `product_inventories`.`product_id` left join `product_images` on `product_flat`.`product_id` = `product_images`.`product_id` left join `product_categories` as `pc` on `product_flat`.`product_id` = `pc`.`product_id` left join `category_translations` as `ct` on `pc`.`category_id` = `ct`.`category_id` and `ct`.`locale` in ('fr') where `product_flat`.`locale` in ('fr') and `product_flat`.`channel` in ('default') group by `product_flat`.`product_id`, `product_flat`.`locale`, `product_flat`.`channel` order by `product_id` desc")
number_of_rows = cur.fetchall()
new_cat = []
i = int(existent_category[-1]['position'])+1
for line in number_of_rows:
    print(line)
    cur.execute("SELECT * FROM `product_categories` WHERE `product_id`=%s",(line['product_id'],))
    bol = False
    homme = False
    femme = False
    for prd_cat in cur.fetchall():
        print(prd_cat)
        if(prd_cat['category_id']>3):
            bol = True
        elif prd_cat['category_id']==2:
            homme=True
        elif prd_cat['category_id']==3:
            femme = True
    if not bol :
        if isinstance(line['name'], str):
            t = line['name'].split()[0]
            for cat in existent_category:
                print(cat)
                if t.lower() == cat['name'].lower() :
                    print("cat exist")
                    if homme :
                        print("add cat pour homme")
                        cur = frip_db.cursor(dictionary=True)
                        sql = "INSERT INTO `product_categories` (`product_id`,`category_id`) VALUES (%s,%s)"
                        val_cat_prd = line['product_id'],cat['category_id']
                        cur.execute(sql, val_cat_prd)
                        frip_db.commit()
                    if femme :
                        cur.execute("SELECT * FROM `category_translations` WHERE `slug` LIKE %s",(cat['name'].lower()+"-fille",))
                        res = cur.fetchall()[0]
                        print(res)
                        cur = frip_db.cursor(dictionary=True)
                        sql = "INSERT INTO `product_categories` (`product_id`,`category_id`) VALUES (%s,%s)"
                        val_cat_prd = line['product_id'],res['category_id']
                        cur.execute(sql, val_cat_prd)
                        frip_db.commit()
                        print("add cat pour femme")
    #           print("existing")ex_cat.append()
                else:
                    print("cat not exist")
    # if isinstance(line['name'], str):
    #     t = line['name'].split()[0]
    #     if t.lower() in new_cat or t.lower() in ex_cat :
    #         print("existing")
           
#         else:   
#             i = i+ 1
#             print(i)
#             cur = frip_db.cursor(dictionary=True)
#             current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             sql_cat = "INSERT INTO `categories` (`status`,`parent_id`,`position`,`created_at`, `updated_at`) VALUES (%s,%s,%s,%s,%s)"
#             val_cat = 1,1,i,current_time,current_time
#             cur.execute(sql_cat, val_cat)
#             frip_db.commit()
#             id_last_cat = cur.lastrowid
        
            
            
#             cur = frip_db.cursor(dictionary=True)
#             sql_tr = "INSERT INTO `category_translations` (`slug`,`description`,`url_path`,`category_id`, `name`, `locale_id`, `locale`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
#             val_tr = t.lower(),line['name'].split()[0],t.lower(),id_last_cat,line['name'].split()[0],2,"fr"
#             cur.execute(sql_tr, val_tr)
#             new_cat.append(t.lower())
#             frip_db.commit()
                      
#             cur = frip_db.cursor(dictionary=True)
#             sql_cat_prd = "INSERT INTO `product_categories` (`product_id`,`category_id`) VALUES (%s,%s)"
#             val_cat_prd = line['product_id'],id_last_cat
#             cur.execute(sql_cat_prd, val_cat_prd)
#             frip_db.commit()
            
           
#  # if(line['category_id']==2):
#             #     id_last = 
#             # else:
            
#     # Removing empty strings from the list
#             # val = datetime.fromtimestamp(line[0]/1000),id, line[1], line[2], line[3], line[4],line[5],datetime.fromtimestamp(line[0]/1000),datetime.fromtimestamp(line[0]/1000)
#             # cur.execute(sql, val)
#             # immune_db.commit()
