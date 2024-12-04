# Create 3d model from video 

## with erasing background to improve the model

Running in a docker container

#### Create 'erase-background' image
```
docker build -t erase-background .
```

run project in the docker container
```
docker run --rm -it \
    -v "$(pwd)/data/input:/app/data/input" \
    -v "$(pwd)/data/output:/app/data/output" \
    erase-background \
    --input_video /app/data/input/IMG_0558.MOV \
    --output_dir /app/data/output

```


Models 
http://download.tensorflow.org/models/object_detection/mask_rcnn_inception_v2_coco_2018_01_28.tar.gz





```frozen_inference_graph.pb```
from http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz

```frozen_inference_graph.pb```
from https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/ssd_mobilenet_v2_coco_2018_03_29.pbtxt