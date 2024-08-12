import rembg
import numpy as np
from PIL import Image
import mysql.connector
from datetime import datetime
from decouple import config

reset = True

frip_db = mysql.connector.connect(
  host=config('DB_HOST'),
  user=config('DB_USERNAME'),
  passwd=config('DB_PASSWORD'),
  database=config('DB_DATABASE')
)

import os
rootdir = 'storage/app/public/product/'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if not "_blank" in file:
            if not os.path.isfile(os.path.join(subdir, file.replace('.webp','_blank.webp'))):
                print(os.path.join(subdir, file.replace('.webp','_blank.webp')))
                print(subdir.replace('storage/app/public/product/',''))
                # Load the input image
                input_image = Image.open(os.path.join(subdir, file))

                # Convert the input image to a numpy array
                input_array = np.array(input_image)

                # Apply background removal using rembg
                output_array = rembg.remove(input_array,bgcolor=[255,255,255,255])

                # Create a PIL Image from the output array
                output_image = Image.fromarray(output_array)

                # Save the output image
                rb = output_image.convert('RGB')
                print(os.path.join(subdir, file.replace('.webp','_blank.webp')))
                rb.save(os.path.join(subdir, file.replace('.webp','_blank.webp')))

                cur = frip_db.cursor(dictionary=True)
                cur.execute("SELECT * FROM `product_images` WHERE `path` LIKE %s",(os.path.join(subdir, file.replace('.webp','_blank.webp')).replace('storage/app/public/',''),))
                res = cur.fetchall()
                if not res:
                    
                    cur.execute("SELECT * FROM `product_images` WHERE `path` LIKE %s",(os.path.join(subdir, file).replace('storage/app/public/',''),))
                    res = cur.fetchall()
                    if res:

                        print(res)
                    
                        last_pos = res['position']
                        sql = "UPDATE product_images SET `position` = %s WHERE `id` = %s"
                        val_cat_up = last_pos+1,res['id']
                        cur.execute(sql, val_cat_up)
                        frip_db.commit()


                        cur = frip_db.cursor(dictionary=True)
                        sql = "INSERT INTO `product_images` (`type`,`path`,`product_id`,`position`) VALUES (%s,%s,%s,%s)"
                        val_cat_prd = 'images',os.path.join(subdir, file.replace('.webp','_blank.webp')).replace('storage/app/public/',''),subdir.replace('storage/app/public/product/',''),last_pos
                        cur.execute(sql, val_cat_prd)
                        frip_db.commit()
                        print("blank image added")
                    else:
                        print("image not in db, u weird bro")
                else:
                    print("op")
            else:
                print("done_file")
                if reset:
                    cur = frip_db.cursor(dictionary=True)
                    sql = "DELETE FROM product_images WHERE `path` = %s"
                    val_cat_up = os.path.join(subdir, file.replace('.webp','_blank.webp')).replace('storage/app/public/',''),
                    cur.execute(sql, val_cat_up)
                    frip_db.commit()
                    os.remove(os.path.join(subdir, file.replace('.webp','_blank.webp')))
        else:
            if reset:
                if os.path.isfile(os.path.join(subdir, file.replace('.webp','_blank.webp'))):
                    os.remove(os.path.join(subdir, file.replace('.webp','_blank.webp')))
                else:
                    print("")
            else:
                print("dont touch blank file, reset=false")