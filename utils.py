# -----------------------------------------------------
# Trust Game
# Licensed under the MIT License
# Written by Ye Liu (ye-liu at whu.edu.cn)
# -----------------------------------------------------

import random

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QLabel

NAMES = ['Alex', 'Alfie', 'Chris', 'Ellis', 'Blair']
GENDERS = ['Male', 'Female']
ETHNICS = ['White', 'Asian', 'Mixed', 'Black']
AVATARS = [f'{gen}-{eth}'.lower() for gen in GENDERS for eth in ETHNICS]


class QAvatar(QLabel):

    clicked = pyqtSignal()

    def __init__(self, name, fallback, *args, **kwargs):
        super(QAvatar, self).__init__(*args, **kwargs)
        self.setObjectName(name)
        self.setGeometry(0, 0, 80, 80)
        self.setPixmap(QPixmap(f'assets/{name}.jpg'))
        self.setScaledContents(True)
        self.clicked.connect(fallback)

    def mousePressEvent(self, e):
        self.clicked.emit()


def match_agent(meta, cfg):
    name = random.choice(NAMES)
    age = meta['age'] + random.randint(-3, 3)
    edu = meta['edu']

    if cfg['use_same_gender']:
        gender = meta['gender']
    else:
        gender = GENDERS[GENDERS.index(meta['gender']) - 1]

    if cfg['use_same_ethnic'] and meta['ethnic'] in ETHNICS:
        ethnic = meta['ethnic']
    else:
        ethnics = list(range(len(ETHNICS)))
        if meta['ethnic'] in ETHNICS:
            ethnics.remove(meta['ethnic'])
        ethnic = random.choice(ethnics)

    return dict(
        avatar=f'assets/{gender}-{ethnic}.jpg'.lower(),
        name=name,
        age=age,
        gender=gender,
        edu=edu,
        ethnic=ethnic)


def set_shadow_effect(widget):
    effect = QGraphicsDropShadowEffect()
    effect.setOffset(1, 1)
    effect.setBlurRadius(35)
    effect.setColor(Qt.darkGray)
    widget.setGraphicsEffect(effect)
