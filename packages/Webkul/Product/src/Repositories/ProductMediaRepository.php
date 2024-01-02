<?php

namespace Webkul\Product\Repositories;

use Exception;
use Illuminate\Support\Str;
use Illuminate\Support\Facades\Storage;
use Illuminate\Http\UploadedFile;
use Intervention\Image\ImageManager;
use Webkul\Core\Eloquent\Repository;

class ProductMediaRepository extends Repository
{
    /**
     * Specify model class name.
     *
     * @return string
     */
    public function model()
    {
        /**
         * This repository is extended to `ProductImageRepository` and `ProductVideoRepository`
         * repository.
         *
         * And currently no model is assigned to this repo.
         */
    }

    /**
     * Get product directory.
     *
     * @param  \Webkul\Product\Contracts\Product $product
     * @return string
     */
    public function getProductDirectory($product): string
    {
        return 'product/' . $product->id;
    }
    
    /**
     * Upload.
     *
     * @param  array  $data
     * @param  \Webkul\Product\Contracts\Product  $product
     * @param  string  $uploadFileType
     * @return void
     */
    public function upload($data, $product, string $uploadFileType): void
    {
        /**
         * Previous model ids for filtering.
         */
        
        $previousIds = $this->resolveFileTypeQueryBuilder($product, $uploadFileType)->pluck('id');
  
        $position = 0;
        if (!empty($data[$uploadFileType]['files'])) {
            $c=0;
            foreach ($data[$uploadFileType]['files'] as $indexOrModelId => $file) {
                if ($file instanceof UploadedFile) {
                    if (Str::contains($file->getMimeType(), 'image')) {
                        $deg =  $data["img"][$indexOrModelId];
                        $manager = new ImageManager();
                        
                        $path = $this->getProductDirectory($product) . '/' . Str::random(40) . '.webp';
                        if($deg!=""){    
                            $l=(explode(":",$deg));
                    
                            $image = $manager->make($file)
                            ->rotate(-intval($l[1]))
                            ->save("./storage/".$path);
                        }else{    
                            $image = $manager->make($file)
                            ->save("./storage/".$path);
                        }
                       
                        // #Storage::put($path, $image)
                        // Storage::put("ole/tstew.jpg", $image);
                    } else {
                        $deg =  $data["img"][$c];
                      
                        $manager = new ImageManager();
                        
                        $path = $this->getProductDirectory($product) . '/' . Str::random(40) . '.webp';
                        if($deg!=""){    
                            $l=(explode(":",$deg));
                            $image = $manager->make($file)
                            ->rotate(-intval($l[1]))
                            ->save("./storage/".$path);
                        }else{    
                        
                            $image = $manager->make($file)
                            ->save("./storage/".$path);
                        }
                        
                    }

                    $this->create([
                        'type'       => $uploadFileType,
                        'path'        => $path,
                        'product_id' => $product->id,
                        'position'   => ++$position,
                    ]);
                } else {
                    if (is_numeric($index = $previousIds->search($indexOrModelId))) {
                        $previousIds->forget($index);
                    }
                   
                    $deg =  $data["img"][$c];
                    $c++;
                    $manager = new ImageManager();
                    $path = $this->getProductDirectory($product) . '/' . Str::random(40) . '.webp';
                   
                    if($deg!=""){    
                        $l=(explode(":",$deg));
                        $path = "./storage/".$l[0];
                        
                        $image = $manager->make($path)
                        ->rotate(-intval($l[1]))
                        ->save($path);
                        $this->update([
                            'path'=>$l[0],
                            'position' => ++$position,
                        ], $indexOrModelId);
                    }else{    
                    
                        $this->update([
                            'position' => ++$position,
                        ], $indexOrModelId);
                    }
                    
                }
            }
        }

        foreach ($previousIds as $indexOrModelId) {
            if (! $model = $this->find($indexOrModelId)) {
                continue;
            }

            Storage::delete($model->path);

            $this->delete($indexOrModelId);
        }
    }

    /**
     * Resolve file type query builder.
     *
     * @param  \Webkul\Product\Contracts\Product $product
     * @param  string  $uploadFileType
     * @return mixed
     *
     * @throws \Exception
     */
    private function resolveFileTypeQueryBuilder($product, string $uploadFileType)
    {
        if ($uploadFileType === 'images') {
            return $product->images();
        } elseif ($uploadFileType === 'videos') {
            return $product->videos();
        }

        throw new Exception('Unsupported file type.');
    }
}
