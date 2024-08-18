import mysql.connector
from datetime import datetime
from decouple import config
import re

frip_db = mysql.connector.connect(
  host=config('DB_HOST'),
  user=config('DB_USERNAME'),
  passwd=config('DB_PASSWORD'),
  database=config('DB_DATABASE')
)


# categories
# category_filterable_attributes
# category_translations
# product_categories


def insert_size(products):
    pattern_one = r'^\d+cm/\d+m$'
    pattern_two = r'^\d+cm/\d+-\da$'
    accep=[]
    for line in products:
        # Example usage
        if len(line['name'].split())>2:
            test_string = line['name'].split()[2] 
            match = re.match(pattern_one, test_string)
            if test_string in accep:
                print("doubl")
            else:
                if match:
                    print("Match found!")
                    accep.append(test_string)
                else:
                    print("No match.")
                    match = re.match(pattern_two, test_string)
                    if match:
                        print("Match found!")
                        accep.append(test_string)
                    else:
                        print("No match.daaaamn")
    print(accep)
    
    return accep

def insert_category(products):
    cur = frip_db.cursor(dictionary=True)
    cur.execute("select `cat`.`id` as `category_id`, `ct`.`name`, `cat`.`position`, `cat`.`status`, `ct`.`locale`, COUNT(DISTINCT pc.product_id) as count from `categories` as `cat` left join `category_translations` as `ct` on `cat`.`id` = `ct`.`category_id` and `ct`.`locale` in ('fr') left join `product_categories` as `pc` on `cat`.`id` = `pc`.`category_id` group by `cat`.`id`, `ct`.`locale` order by `category_id` desc limit 10 offset 0")
    existent_category = cur.fetchall()
    #print(existent_category)
    ex_cat =[]
    for cat in existent_category:
        ex_cat.append(cat['name'].lower())
    new_cat=[]
    for line in products:
        if line['name'].split()[0] in existent_category:
            print("found in db or new list")
        elif line['name'].split()[0] in new_cat:
            print("found in db or new list")
        else:
            if(len(line['name'].split())>2):
                print("Cat : " + line['name'].split()[0])
                print("Marque : " + line['name'].split()[1])
                print("Taille : " + line['name'].split()[2])
        cur = frip_db.cursor(dictionary=True)
        cur.execute("SELECT max(`_lft`),max(`_rgt`) FROM `categories` WHERE `parent_id` = 332")
        res = cur.fetchall()
        print(res[0]['max(`_lft`)'])
        print(res[0]['max(`_rgt`)'])

        t = line['name'].split()[0]
        cur = frip_db.cursor(dictionary=True)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql_cat = "INSERT INTO `categories` (`status`,`parent_id`,_lft,_rgt,`position`,`created_at`, `updated_at`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        val_cat = 1,332,res[0]['max(`_lft`)'],res[0]['max(`_rgt`)'],2,current_time,current_time
        cur.execute(sql_cat, val_cat)
        frip_db.commit()
        id_last_cat = cur.lastrowid
        cur = frip_db.cursor(dictionary=True)
        sql_tr = "INSERT INTO `category_filterable_attributes` (`category_id`, `attribute_id`) VALUES (%s,%s)"
        val_tr = id_last_cat,11
        cur.execute(sql_tr, val_tr)
        frip_db.commit()
        cur = frip_db.cursor(dictionary=True)
        sql_tr = "INSERT INTO `category_filterable_attributes` (`category_id`, `attribute_id`) VALUES (%s,%s)"
        val_tr = id_last_cat,23
        cur.execute(sql_tr, val_tr)
        frip_db.commit()
        cur = frip_db.cursor(dictionary=True)
        sql_tr = "INSERT INTO `category_filterable_attributes` (`category_id`, `attribute_id`) VALUES (%s,%s)"
        val_tr = id_last_cat,24
        cur.execute(sql_tr, val_tr)
        frip_db.commit()
        cur = frip_db.cursor(dictionary=True)
        sql_tr = "INSERT INTO `category_filterable_attributes` (`category_id`, `attribute_id`) VALUES (%s,%s)"
        val_tr = id_last_cat,25 
        cur.execute(sql_tr, val_tr)
        frip_db.commit()
        #attr end
        cur = frip_db.cursor(dictionary=True)
        sql_tr = "INSERT INTO `category_translations` (`slug`,`description`,`url_path`,`meta_title`,`category_id`, `name`, `locale_id`, `locale`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        val_tr = t.lower(),t,"garcon/vetements/"+t.lower(),t,id_last_cat,t,2,"fr"
        cur.execute(sql_tr, val_tr)
        frip_db.commit()
                    
        cur = frip_db.cursor(dictionary=True)
        sql_cat_prd = "INSERT INTO `product_categories` (`product_id`,`category_id`) VALUES (%s,%s)"
        val_cat_prd = line['product_id'],id_last_cat
        cur.execute(sql_cat_prd, val_cat_prd)
        frip_db.commit()

        #second exec for girl
        cur = frip_db.cursor(dictionary=True)
        cur.execute("SELECT max(`_lft`),max(`_rgt`) FROM `categories` WHERE `parent_id` = 334")
        res = cur.fetchall()
        print(res[0]['max(`_lft`)'])
        print(res[0]['max(`_rgt`)'])
        

        cur = frip_db.cursor(dictionary=True)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql_cat = "INSERT INTO `categories` (`status`,`parent_id`,_lft,_rgt,`position`,`created_at`, `updated_at`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        val_cat = 1,334,res[0]['max(`_lft`)'],res[0]['max(`_rgt`)'],2,current_time,current_time
        cur.execute(sql_cat, val_cat)
        frip_db.commit()
        id_last_cat = cur.lastrowid
        
        cur = frip_db.cursor(dictionary=True)
        sql_tr = "INSERT INTO `category_translations` (`slug`,`description`,`url_path`,`meta_title`,`category_id`, `name`, `locale_id`, `locale`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        val_tr = t.lower(),t,"fille/vetements-fille/"+t.lower(),t,id_last_cat,t,2,"fr"
        cur.execute(sql_tr, val_tr)
        frip_db.commit()
        #attribute        
        cur = frip_db.cursor(dictionary=True)
        sql_tr = "INSERT INTO `category_filterable_attributes` (`category_id`, `attribute_id`) VALUES (%s,%s)"
        val_tr = id_last_cat,11
        cur.execute(sql_tr, val_tr)
        frip_db.commit()
        cur = frip_db.cursor(dictionary=True)
        sql_tr = "INSERT INTO `category_filterable_attributes` (`category_id`, `attribute_id`) VALUES (%s,%s)"
        val_tr = id_last_cat,23
        cur.execute(sql_tr, val_tr)
        frip_db.commit()
        cur = frip_db.cursor(dictionary=True)
        sql_tr = "INSERT INTO `category_filterable_attributes` (`category_id`, `attribute_id`) VALUES (%s,%s)"
        val_tr = id_last_cat,24
        cur.execute(sql_tr, val_tr)
        frip_db.commit()
        cur = frip_db.cursor(dictionary=True)
        sql_tr = "INSERT INTO `category_filterable_attributes` (`category_id`, `attribute_id`) VALUES (%s,%s)"
        val_tr = id_last_cat,25 
        cur.execute(sql_tr, val_tr)
        frip_db.commit()
        #attr end
        
        cur = frip_db.cursor(dictionary=True)
        sql_cat_prd = "INSERT INTO `product_categories` (`product_id`,`category_id`) VALUES (%s,%s)"
        val_cat_prd = line['product_id'],id_last_cat
        cur.execute(sql_cat_prd, val_cat_prd)
        frip_db.commit()



cur = frip_db.cursor(dictionary=True)
cur.execute("select distinct `product_flat`.`locale`,`product_flat`.`product_id`, `product_flat`.`channel`, `product_images`.`path` as `base_image`, `pc`.`category_id`, `ct`.`name` as `category_name`, `product_flat`.`product_id`, `product_flat`.`sku`, `product_flat`.`name`, `product_flat`.`type`, `product_flat`.`status`, `product_flat`.`price`, `product_flat`.`url_key`, `product_flat`.`visible_individually`, `af`.`name` as `attribute_family`, SUM(DISTINCT product_inventories.qty) as quantity, COUNT(DISTINCT product_images.id) as images_count from `product_flat` left join `attribute_families` as `af` on `product_flat`.`attribute_family_id` = `af`.`id` left join `product_inventories` on `product_flat`.`product_id` = `product_inventories`.`product_id` left join `product_images` on `product_flat`.`product_id` = `product_images`.`product_id` left join `product_categories` as `pc` on `product_flat`.`product_id` = `pc`.`product_id` left join `category_translations` as `ct` on `pc`.`category_id` = `ct`.`category_id` and `ct`.`locale` in ('fr') where `product_flat`.`locale` in ('fr') and `product_flat`.`channel` in ('default') group by `product_flat`.`product_id`, `product_flat`.`locale`, `product_flat`.`channel` order by `product_id` desc")
products = cur.fetchall()

#insert_category(products,existent_category)
insert_size(products)
    
    

            
        

    
    
       
   