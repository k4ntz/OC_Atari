"""
Classes and methods to compute metrics on the RAM extraction method, \
    based on the ground truth vision extracted objects.
"""

import numpy as np
from termcolor import colored
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import euclidean, cdist


np.set_printoptions(precision=1)
USE_IPDB = False
MIN_DIST_DETECTION = 5


def format_values(dictionary):
    keys, values = dictionary.keys(), dictionary.values()
    return {key: round(val, 1) for key, val in zip(keys, (np.array(list(values)) * 100))}


class DetectionScores():
    """
    Keeps track of true positives, false positive and false negative of the detected objects.
    Allow to fast compute precision, recall, and f1 scores.
    """

    def __init__(self) -> None:
        self.true_pos = {}
        self.false_pos = {}
        self.false_neg = {}

    def update(self, det_dict):
        """

        """
        for cat, (TP, FP, FN) in det_dict.items():
            if not cat in self.true_pos:
                self.true_pos[cat] = TP
                self.false_pos[cat] = FP
                self.false_neg[cat] = FN
            else:
                self.true_pos[cat] += TP
                self.false_pos[cat] += FP
                self.false_neg[cat] += FN

    @property
    def cat_precisions(self):
        """
        The per cartegory dictionary of the precision
        """
        return {cat: self.true_pos[cat]/(self.true_pos[cat]+self.false_pos[cat]) for cat in self.true_pos if self.true_pos[cat]+self.false_pos[cat]}

    @property
    def cat_recalls(self):
        """
        The per cartegory dictionary of the recall
        """
        return {cat: self.true_pos[cat]/(self.true_pos[cat]+self.false_neg[cat]) for cat in self.true_pos if self.true_pos[cat]+self.false_neg[cat]}

    @property
    def cat_f_scores(self):
        """
        The per cartegory dictionary of the F-scores
        """
        prec, rec = self.cat_precisions, self.cat_recalls
        f_scores = {}
        for cat in prec.keys():
            try:
                if prec[cat] == 0 and rec[cat] == 0:
                    f_scores[cat] = 0
                else:
                    f_scores[cat] = 2 * prec[cat] * \
                        rec[cat] / (prec[cat] + rec[cat])
            except KeyError:
                f_scores[cat] = 0
        return f_scores

    @property
    def mean_precision(self):
        """
        The mean precision on all objects
        """
        return sum(self.true_pos.values())/(sum(self.true_pos.values()) + sum(self.false_pos.values()))

    @property
    def mean_recall(self):
        """
        The mean recall on all objects
        """
        return sum(self.true_pos.values())/(sum(self.true_pos.values()) + sum(self.false_neg.values()))

    @property
    def mean_f_score(self):
        """
        The mean F-score on all objects
        """
        prec, rec = self.mean_precision, self.mean_recall
        return 2 * prec * rec / (prec + rec)

    def __repr__(self) -> str:
        return "Detection stats with Cat. F-scores: \n" + str(self.cat_f_scores)

    @property
    def dict_summary(self):
        """
        The mean precision, recall and F-score on all objects.
        """
        return {"precision": self.mean_precision, "recall": self.mean_recall, "f-score": self.mean_f_score,
                "iou": self.iou}


def print_all_stats(all_stats):
    """
    Nicely prints the stats in the terminal.
    """
    linelength = 39
    print("Mean IOUs: ", round(all_stats['mean_ious'], 2))
    print("-"*linelength)
    print("\nPer class IOU: ")
    for objname, res in all_stats['per_class_ious'].items():
        if res < 0.6:
            print(colored(f"\t| {objname}: {res:.2f}", 'red'))
        elif res < 0.9:
            print(colored(f"\t| {objname}: {res:.2f}", 'yellow'))
        else:
            print(colored(f"\t| {objname}: {res:.2f}", 'green'))
    if all_stats['only_in_ram']:
        print("-"*linelength)
        print("Objects found only in ram version: ")
        for objname, res in all_stats['only_in_ram'].items():
            if eval(res) < 0.6:
                print(colored(f"\t| {objname}: {res}", 'red'))
            elif eval(res) < 0.9:
                print(colored(f"\t| {objname}: {res}", 'yellow'))
            else:
                print(colored(f"\t| {objname}: {res}", 'green'))
    if all_stats['only_in_vision']:
        print("-"*linelength)
        print("Objects found only in vision version: ")
        for objname, res in all_stats['only_in_vision'].items():
            if eval(res) < 0.6:
                print(colored(f"\t| {objname}: {res}", 'red'))
            elif eval(res) < 0.9:
                print(colored(f"\t| {objname}: {res}", 'yellow'))
            else:
                print(colored(f"\t| {objname}: {res}", 'green'))
    print("-"*linelength)


def get_iou(obj1, obj2):
    """
    Computes the intersection over union between two GameObjects.

    :param obj1: The bouding box of the detected object in (x, y, w, h) format
    :type obj1: ocatari.ram.game_objects.GameObject or ocatari.vision.game_objects.GameObject
    :param obj2: The ground truth bouding box
    :type obj2: ocatari.ram.game_objects.GameObject or ocatari.vision.game_objects.GameObject
    """
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(obj1.x, obj2.x)
    yA = max(obj1.y, obj2.y)
    xB = min(obj1.x+obj1.w, obj2.x+obj2.w)
    yB = min(obj1.y+obj1.h, obj2.y+obj2.h)
    # compute the area of intersection rectangle
    interArea = max(0, xB - xA) * max(0, yB - yA)
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (obj1.w) * (obj1.h)
    boxBArea = (obj2.w) * (obj2.h)
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)
    # return the intersection over union value
    return iou


def _make_class_lists(ram_list, vision_list):
    """
    Creates a dictionary of object category liked with both the ram objs of this
    category and then the vision objs of this category.

    :param ram_list: The list of objects detected by the RAM extraction method
    :type ram_list: list of ocatari.ram.game_objects.GameObject
    :param ram_list: The list of objects detected by the RAM extraction method
    :type ram_list: list of ocatari.vision.game_objects.GameObject

    :return: A dictionary containing the per class metrics.
    :rtype: dict
    """
    categories = set([obj.category for obj in ram_list+vision_list])
    cat_lists = {}
    for cat in categories:
        cat_lists[cat] = ([obj.center for obj in ram_list if obj.category == cat],
                          [obj.center for obj in vision_list if obj.category == cat])
    return cat_lists


def detection_stats(ram_list, vision_list):
    """
    Returns the Precision, Recall and F1_score via comparing the RAM and vision lists.
    These metrics are computed based on MIN_DIST_DETECTION (default =5).

    :param ram_list: The list of objects detected by the RAM extraction method
    :type ram_list: list of ocatari.ram.game_objects.GameObject
    :param ram_list: The list of objects detected by the RAM extraction method
    :type ram_list: list of ocatari.vision.game_objects.GameObject

    :return: A dictionary containing the per class metrics.
    :rtype: dict
    """
    cat_lists = _make_class_lists(ram_list, vision_list)
    dets = {}
    for cat, (rlist, vlist) in cat_lists.items():
        TrueP = 0
        FalseP = max(0, len(rlist) - len(vlist))
        FalseN = max(0, len(vlist) - len(rlist))
        if len(rlist) > 1 and len(vlist) > 1:
            cost_m = cdist(rlist, vlist)
            row_ind, col_ind = linear_sum_assignment(cost_m)
            # reassign
            rlist = [rlist[i] for i in row_ind]
            vlist = [vlist[i] for i in col_ind]
        for ro, vo in zip(rlist, vlist):
            if euclidean(ro, vo) < MIN_DIST_DETECTION:
                TrueP += 1
            else:
                FalseN += 1
                FalseP += 1
        dets[cat] = (TrueP, FalseP, FalseN)
    return dets


def get_all_metrics(ram_list, vision_list):
    """
    Computes the:

     * mean_iou
     * per_class_ious
     * only_in_ram
     * only_in_vision
     * objs_in_ram
     * objs_in_vision
     * dets ()

    two lists of GameObjects (from the RAM extraction and from the vision extraction methods).

    :param ram_list: The list of objects detected by the RAM extraction method
    :type ram_list: list of ocatari.ram.game_objects.GameObject
    :param ram_list: The list of objects detected by the RAM extraction method
    :type ram_list: list of ocatari.vision.game_objects.GameObject

    :return: A dictionary containing the per class metrics.
    :rtype: dict
    """
    only_in_ram = []
    only_in_vision = []
    per_class_ious = {}
    ious = []
    dets = detection_stats(ram_list, vision_list)
    if abs(len(vision_list) - len(ram_list)) > 10 and USE_IPDB:
        import ipdb
        ipdb.set_trace()
    for vobj in vision_list:
        vobj._is_in_ram = False
    for robj in ram_list:
        robj._is_in_image = False
        for vobj in vision_list:
            if robj.__class__.__name__ == vobj.__class__.__name__:
                objname = robj.__class__.__name__
                iou = get_iou(robj, vobj)
                if iou > 0:
                    ious.append(iou)
                    if objname not in per_class_ious:
                        per_class_ious[objname] = [iou]
                    else:
                        per_class_ious[objname].append(iou)
                    vobj._is_in_ram = True
                    robj._is_in_image = True
                    break
    for name, li in per_class_ious.items():
        per_class_ious[name] = np.mean(li)
    for robj in ram_list:
        if not robj._is_in_image:
            only_in_ram.append(str(robj))
    for vobj in vision_list:
        if not vobj._is_in_ram:
            only_in_vision.append(str(vobj))
    return {"mean_iou": np.mean(ious), "per_class_ious": per_class_ious,
            "only_in_ram": only_in_ram, "only_in_vision": only_in_vision,
            "objs_in_ram": [str(o) for o in ram_list],
            "objs_in_vision": [str(o) for o in vision_list],
            "dets": dets}
