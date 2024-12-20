# Create 3d model from video 

## with erasing background to improve the model

videofile should be placed in the directory data/input

run process:
./run.sh <name_videofile> [<frames_from_sec>]

name_videofile - name of videofile without path (places in data/input)
frames_from_sec - extra parameter. How many images from 1 sec of the video should be extracted. Default value is 1.


Models 
http://download.tensorflow.org/models/object_detection/mask_rcnn_inception_v2_coco_2018_01_28.tar.gz





```frozen_inference_graph.pb```
from http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz

```frozen_inference_graph.pb```
from https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/ssd_mobilenet_v2_coco_2018_03_29.pbtxt