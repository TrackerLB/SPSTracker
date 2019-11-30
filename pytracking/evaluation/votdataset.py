import numpy as np
from pytracking.evaluation.data import Sequence, BaseDataset, SequenceList


def VOTDataset():
    return VOTDatasetClass().get_sequence_list()


class VOTDatasetClass(BaseDataset):
    """VOT2018 dataset

    Publication:
        The sixth Visual Object Tracking VOT2018 challenge results.
        Matej Kristan, Ales Leonardis, Jiri Matas, Michael Felsberg, Roman Pfugfelder, Luka Cehovin Zajc, Tomas Vojir,
        Goutam Bhat, Alan Lukezic et al.
        ECCV, 2018
        https://prints.vicos.si/publications/365

    Download the dataset from http://www.votchallenge.net/vot2018/dataset.html"""
    def __init__(self):
        super().__init__()
        self.base_path = self.env_settings.vot_path
        print(self.base_path)
        self.sequence_list = self._get_sequence_list()

    def get_sequence_list(self):
        return SequenceList([self._construct_sequence(s) for s in self.sequence_list])

    def _construct_sequence(self, sequence_name):
        sequence_path = sequence_name
        nz = 8
        ext = 'jpg'
        start_frame = 1

        anno_path = '{}/{}/groundtruth.txt'.format(self.base_path, sequence_name)
        try:
            ground_truth_rect = np.loadtxt(str(anno_path), dtype=np.float64)
        except:
            ground_truth_rect = np.loadtxt(str(anno_path), delimiter=',', dtype=np.float64)
        gt = ground_truth_rect
        end_frame = ground_truth_rect.shape[0]
#/color/
        frames = ['{base_path}/{sequence_path}/{frame:0{nz}}.{ext}'.format(base_path=self.base_path,
                  sequence_path=sequence_path, frame=frame_num, nz=nz, ext=ext)
                  for frame_num in range(start_frame, end_frame+1)]
        #print(frames)
        # Convert gt
        if ground_truth_rect.shape[1] > 4:
            gt_x_all = ground_truth_rect[:, [0, 2, 4, 6]]
            gt_y_all = ground_truth_rect[:, [1, 3, 5, 7]]

            x1 = np.amin(gt_x_all, 1).reshape(-1,1)
            y1 = np.amin(gt_y_all, 1).reshape(-1,1)
            x2 = np.amax(gt_x_all, 1).reshape(-1,1)
            y2 = np.amax(gt_y_all, 1).reshape(-1,1)

            ground_truth_rect = np.concatenate((x1, y1, x2-x1, y2-y1), 1)
        return Sequence(sequence_name, frames, ground_truth_rect,gt)

    def __len__(self):
        return len(self.sequence_list)

    def _get_sequence_list(self):
        sequence_list= [ 'ants3',
                        'ants1',
                        'bag',
                        'ball1',
                        'ball2',
                        'basketball',
                        'birds1',
                        'blanket',
                        'bmx',
                        'bolt1',
                        'bolt2',
                        'book',
                        'butterfly',
                        'car1',
                        'conduction1',
                        'crabs1',
                        'crossing',
                        'dinosaur',
                        'drone_across',
                        'drone_flip',
                        'drone1',
                        'fernando',
                        'fish1',
                        'fish2',
                        'fish3',
                        'flamingo1',
                        'frisbee',
                        'girl',
                        'glove',
                        'godfather',
                        'graduate',
                        'gymnastics1',
                        'gymnastics2',
                        'gymnastics3',
                        'hand',
                        'handball1',
                        'handball2',
                        'helicopter',
                        'iceskater1',
                        'iceskater2',
                        'leaves',
                        'matrix',
                        'motocross1',
                        'motocross2',
                        'nature',
                        'pedestrian1',
                        'rabbit',
                        'racing',
                        'road',
                        'shaking',
                        'sheep',
                        'singer2',
                        'singer3',
                        'soccer1',
                        'soccer2',
                        'soldier',
                        'tiger',
                        'traffic',
                        'wiper',
                        'zebrafish1'

                        ]

        return sequence_list

# 'afterrain',
#                         'aftertree',
#                         'baby',
#                         'baginhand',
#                         'baketballwaliking',
#                         'balancebike',
#                         'basketball2',
#                         'bicyclecity',
#                         'bike',
#                         'bikeman',
#                         'bikemove1',
#                         'biketwo',
#                         'blueCar',
#                         'bluebike',
#                         'bus6',
#                         'car',
#                         'car10',
#                         'car20',
#                         'car3',
#                         'car37',
#                         'car4',
#                         'car41',
#                         'car66',
#                         'carLight',
#                         'caraftertree',
#                         'carnotfar',
#                         'carred',
#                         'child',
#                         'child1',
#                         'crossroad',
#                         'crouch',
#                         'cycle1',
#                         'cycle3',
#                         'diamond',
#                         'dog',
#                         'dog11',
#                         'elecbike',
#                         'elecbikechange2',
#                         'face1',
#                         'floor-1',
#                         'flower2',
#                         'fog',
#                         'fog6',
#                         'green',
#                         'greyman',
#                         'greywoman',
#                         'hotkettle',
#                         'man4',
#                         'man88',
#                         'mandrivecar',
#                         'maninblack',
#                         'manwithbasketball',
#                         'redcar',
#                         'supbus',
#                         'takeout',
#                         'tricycle',
#                         'twoelecbike1',
#                         'twowoman',
#                         'walkingnight',
#                         'woman89'
# 'bag',
#                         'ball1',
#                         'ball2',
#                         'basketball',
#                         'birds1',
#                         'birds2',
#                         'blanket',
#                         'bmx',
#                         'bolt1',
#                         'bolt2',
#                         'book',
#                         'butterfly',
#                         'car1',
#                         'car2',
#                         'crossing',
#                         'dinosaur',
#                         'fernando',
#                         'fish1',
#                         'fish2',
#                         'fish3',
#                         'fish4',
#                         'girl',
#                         'glove',
#                         'godfather',
#                         'graduate',
#                         'gymnastics1',
#                         'gymnastics2',
#                         'gymnastics3',
#                         'gymnastics4',
#                         'hand',
#                         'handball1',
#                         'handball2',
#                         'helicopter',
#                         'iceskater1',
#                         'iceskater2',
#                         'leaves',
#                         'marching',
#                         'matrix',
#                         'motocross1',
#                         'motocross2',
#                         'nature',
#                         'octopus',
#                         'pedestrian1',
#                        'pedestrian2',
#                         'rabbit',
#                         'racing',
#                        'road',
#                        'shaking',
#                         'sheep',
#                        'singer1',
#                         'singer2',
#                         'singer3',
#                         'soccer1',
#                        'soccer2',
#                         'soldier',
#                         'sphere',
#                        'tiger',
#                         'traffic',
#                         'tunnel',
#                         'wiper',
# 'ants3',
#                         'ants1',
#                         'bag',
#                         'ball1',
#                         'ball2',
#                         'basketball',
#                         'birds1',
#                         'blanket',
#                         'bmx',
#                         'bolt1',
#                         'bolt2',
#                         'book',
#                         'butterfly',
#                         'car1',
#                         'conduction1',
#                         'crabs1',
#                         'crossing',
#                         'dinosaur',
#                         'drone_across',
#                         'drone_flip',
#                         'drone1',
#                         'fernando',
#                         'fish1',
#                         'fish2',
#                         'fish3',
#                         'flamingo1',
#                         'frisbee',
#                         'girl',
#                         'glove',
#                         'godfather',
#                         'graduate',
#                         'gymnastics1',
#                         'gymnastics2',
#                         'gymnastics3',
#                         'hand',
#                         'handball1',
#                         'handball2',
#                         'helicopter',
#                         'iceskater1',
#                         'iceskater2',
#                         'leaves',
#                         'matrix',
#                         'motocross1',
#                         'motocross2',
#                         'nature',
#                         'pedestrian1',
#                         'rabbit',
#                         'racing',
#                         'road',
#                         'shaking',
#                         'sheep',
#                         'singer2',
#                         'singer3',
#                         'soccer1',
#                         'soccer2',
#                         'soldier',
#                         'tiger',
#                         'traffic',
#                         'wiper',
#                         'zebrafish1'
