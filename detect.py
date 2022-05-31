from skimage import io,transform
import tensorflow as tf
import numpy as np
import time

from config import cfg
from utils import *

def detect(imgNamePath, desktopPath):

        flower_labels = get_labels(cfg.data_path)

        images = read_one_image(imgNamePath, cfg.width, cfg.height)
        reimages = tf.reshape(images, [1, 100, 100, 3])

        with tf.Session() as sess:
                saver = tf.train.import_meta_graph('../checkpoints/flower_model_0500.meta')
                saver.restore(sess, tf.train.latest_checkpoint('../checkpoints/'))

                graph = tf.get_default_graph()
                x = graph.get_tensor_by_name("x:0")
                feed_dict = {x: reimages.eval()}

                logits = graph.get_tensor_by_name("logits_eval:0")
                classification_result = sess.run(logits, feed_dict)
                output = tf.argmax(classification_result, 1).eval()
                draw_img_path, saved = pil_draw_image(desktopPath, imgNamePath, flower_labels[output[0]])

        return draw_img_path, flower_labels[output[0]], saved