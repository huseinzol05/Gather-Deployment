import tensorflow as tf

EVAL_SIZE = (512, 512)
R, G, B = 123.0, 117.0, 104.0

def preprocess_for_eval(image, out_shape = EVAL_SIZE, data_format = 'NHWC'):
	image = tf.to_float(image)
	mean = tf.constant([R, G, B], dtype = image.dtype)
	image = image - mean

    # Add image rectangle to bboxes.
	bbox_img = tf.constant([[0., 0., 1., 1.]])
	bboxes = bbox_img
	
	height, width, channels = image.shape
	image = tf.expand_dims(image, 0)
	image = tf.image.resize_images(image, out_shape, tf.image.ResizeMethod.BILINEAR, False)
	image = tf.reshape(image, tf.stack([out_shape[0], out_shape[1], channels]))

    # Split back bounding boxes.
	bbox_img = bboxes[0]
	bboxes = bboxes[1:]
	
    # Image data format.
	if data_format == 'NCHW':
		image = tf.transpose(image, perm = (2, 0, 1))
	return image, bboxes, bbox_img


