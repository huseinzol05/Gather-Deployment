import tensorflow as tf
import numpy as np
from utils import label_map_util
from utils import visualization_utils as vis_util
from scipy.misc import imread, imsave
import os

MODEL_NAME = 'ssd_mobilenet'
PATH_TO_CKPT = os.path.join(MODEL_NAME, 'frozen_inference_graph.pb')
PATH_TO_LABELS = 'mscoco_label_map.pbtxt'
NUM_CLASSES = 90

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name = '')
        sess = tf.InteractiveSession()
        sess.run(tf.global_variables_initializer())

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(
    label_map, max_num_classes = NUM_CLASSES, use_display_name = True
)
category_index = label_map_util.create_category_index(categories)


def detect_object(img):
    image_np_expanded = np.expand_dims(img, axis = 0)
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    scores = detection_graph.get_tensor_by_name('detection_scores:0')
    classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
    (boxes, scores, classes, num_detections) = sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict = {image_tensor: image_np_expanded},
    )
    vis_util.visualize_boxes_and_labels_on_image_array(
        img,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates = True,
        line_thickness = 8,
    )
    return img
