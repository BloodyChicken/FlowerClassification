from skimage import io, transform
import glob
import os
import numpy as np
from PIL import Image, ImageFont, ImageDraw


def read_img(path, w, h):
    print("reading images ...")
    cate = [(path + x) for x in os.listdir(path) if os.path.isdir(path + x)]
    imgs = []
    labels = []

    type = 0
    num = 0
    for idx, folder in enumerate(cate):
        for im in glob.glob(folder + '/*.jpg'):
            img = io.imread(im)
            img = transform.resize(img, (w, h))
            imgs.append(img)
            labels.append(idx)
            num = num + 1
        type = type + 1
    print("read images type: %d, total num: %d" % (type, num))
    return np.asarray(imgs, np.float32), np.asarray(labels, np.int32)


def get_batch_data(path, w, h, ratio):
    data, label = read_img(path, w, h)
    num_example = data.shape[0]
    arr = np.arange(num_example)
    np.random.shuffle(arr)
    data = data[arr]
    label = label[arr]
    s = np.int(num_example * ratio)
    x_train = data[:s]
    y_train = label[:s]
    x_val = data[s:]
    y_val = label[s:]
    return x_train, y_train, x_val, y_val


def minibatches(inputs=None, targets=None, batch_size=None, shuffle=False):
    assert len(inputs) == len(targets)
    if shuffle:
        np.random.shuffle(indices)

    for start_idx in range(0, (len(inputs) - batch_size + 1), batch_size):
        if shuffle:
            excerpt = indices[start_idx: (start_idx + batch_size)]
        else:
            excerpt = slice(start_idx, (start_idx + batch_size))
        yield inputs[excerpt], targets[excerpt]


def get_labels(path):
    cate = [(path + x) for x in os.listdir(path) if os.path.isdir(path + x)]
    labels = []
    for folder in cate:
        idx = folder.rfind("/")
        label = folder[(idx + 1):len(folder)]
        if label == "daisy":
            label = label + "/雏菊"
        elif label == "dandelion":
            label = label + "/蒲公英"
        elif label == "roses":
            label = label + "/玫瑰"
        elif label == "sunflowers":
            label = label + "/向日葵"
        elif label == "tulips":
            label = label + "/郁金香"
        labels.append(label)
    return labels


def read_one_image(path, w, h):
    img = io.imread(path)
    img = transform.resize(img, (w, h))
    return np.asarray(img)


def del_file(path):
    for i in os.listdir(path):
        path_file = os.path.join(path, i)
        if os.path.isfile(path_file):
            os.remove(path_file)
        else:
            del_file(path_file)


def pil_draw_image(desktopPath, img_path, text):
    Open_img = Image.open(img_path)
    font = ImageFont.truetype('./simhei.ttf', 24)

    x, y = (0, 0)
    draw = ImageDraw.Draw(Open_img)
    draw.text((x, y), text, font=font, fill=(255, 0, 0, 255))

    idx = text.find("/")
    label = text[0:idx]
    suffix = img_path.split(".")[1]

    out_file_path = desktopPath + "\\" + label + "." + suffix

    Open_img.save(out_file_path)

    saved = True

    return out_file_path, saved

