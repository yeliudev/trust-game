# -----------------------------------------------------
# Trust Game
# Licensed under the MIT License
# Written by Ye Liu (ye-liu at whu.edu.cn)
# -----------------------------------------------------

import random

from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtWidgets import QApplication

from config import cfg
from utils import AVATARS, QAvatar, match_agent, set_shadow_effect

global window, sess


def next_page():
    index = window.pages.currentIndex() + 1
    window.pages.setCurrentIndex(index)


def check_age():
    try:
        if (age := int(window.age_input.text())) > 10 and age < 100:
            window.age_error_label.setText('')
            sess['meta']['age'] = age
            return True
        raise Exception
    except Exception:
        window.age_error_label.setText('Please input a valid age.')


def check_gender():
    if window.male_radio.isChecked():
        window.gender_error_label.hide()
        sess['meta']['gender'] = window.male_radio.text()
        return True
    elif window.female_radio.isChecked():
        window.gender_error_label.hide()
        sess['meta']['gender'] = window.female_radio.text()
        return True
    else:
        window.gender_error_label.show()


def check_edu():
    if (edu := window.edu_combo.currentText()) == 'Please indicate':
        window.edu_error_label.show()
    else:
        window.edu_error_label.hide()
        sess['meta']['edu'] = edu
        return True


def check_ethnic():
    if (ethnic := window.ethnic_combo.currentText()) == 'Please indicate':
        window.ethnic_error_label.show()
    elif ethnic == 'Others':
        if (ethnic := window.ethnic_input.text()).isalpha():
            window.ethnic_error_label.hide()
            sess['meta']['ethnic'] = ethnic
            return True
        else:
            window.ethnic_error_label.show()
    else:
        window.ethnic_error_label.hide()
        sess['meta']['ethnic'] = ethnic
        return True


def check_avatar():
    if sess.get('has_avatar', False):
        window.user_avatar_error_label.hide()
        return True
    else:
        window.user_avatar_error_label.show()


def check_name():
    if (name := window.user_name_input.text()).isalpha():
        window.user_name_error_label.hide()
        window.user_name.setText(name)
        sess['meta']['name'] = name
        return True
    else:
        window.user_name_error_label.show()


def check_invest():
    try:
        if (coins := int(
                window.invest_input.text())) > 0 and coins <= sess['coins']:
            window.invest_error_label.hide()
            return coins
        raise Exception
    except Exception:
        if sess.get('raise_error', True):
            window.invest_error_label.show()


def _state_checkbox_changed():
    if window.state_checkbox.isChecked():
        window.continue_button_active.show()
        window.continue_button_inactive.hide()
    else:
        window.continue_button_active.hide()
        window.continue_button_inactive.show()


def _continue_button_clicked():
    has_age = check_age()
    has_gender = check_gender()
    has_edu = check_edu()
    has_ethnic = check_ethnic()
    if has_age and has_gender and has_edu and has_ethnic:
        next_page()


def _user_avatar_clicked():
    window.avatar_panel.show()


def _avatar_clicked():
    window.user_avatar_1.setPixmap(window.sender().pixmap())
    window.user_avatar_2.setPixmap(window.sender().pixmap())
    window.user_avatar_error_label.hide()
    window.avatar_panel.hide()
    sess['has_avatar'] = True


def _match_button_clicked():

    def _show_agent():
        # Match agent
        agent = match_agent(sess['meta'], cfg['agent'])
        loading_timer.stop()

        # Display agent
        window.loading_icon.hide()
        window.agent_avatar_1.show()
        window.agent_name_label.show()
        window.agent_age_label.show()
        window.agent_gender_label.show()
        window.agent_edu_label.show()
        window.agent_ethnic_label.show()
        window.okay_button.show()
        window.agent_avatar_1.setPixmap(QPixmap(agent['avatar']))
        window.agent_avatar_2.setPixmap(QPixmap(agent['avatar']))
        window.agent_name.setText(agent['name'])
        window.agent_name_value.setText(agent['name'])
        window.agent_age_value.setText(str(agent['age']))
        window.agent_gender_value.setText(agent['gender'])
        window.agent_edu_value.setText(agent['edu'])
        window.agent_ethnic_value.setText(agent['ethnic'])

    has_avatar = check_avatar()
    has_name = check_name()
    if has_avatar and has_name:
        # Disable useless widgets
        window.user_avatar_1.setEnabled(False)
        window.user_name_label.setEnabled(False)
        window.user_name_input.setEnabled(False)
        window.match_button.hide()

        # Display loading icon
        loading_timer = QTimer()
        loading_timer.timeout.connect(_show_agent)
        loading_timer.start(3000)
        window.loading_icon.show()


def _confirm_button_clicked():

    def _show_result():
        # Compute gain
        yield_rate = random.normalvariate(sess['meta']['mean'],
                                          sess['meta']['var'])
        if yield_rate < -1:
            yield_rate = -1
        elif yield_rate > cfg['multiplier'] - 1:
            yield_rate = cfg['multiplier'] - 1
        gain = int(sess['log'][-1][0] * yield_rate + sess['log'][-1][0])
        sess['coins'] += gain
        sess['log'][-1].append(gain)
        dealing_timer.stop()

        # Hide useless widgets
        window.user_name.hide()
        window.agent_name.hide()
        window.user_avatar_2.hide()
        window.agent_avatar_2.hide()
        window.dealing_icon.hide()

        # Display results
        window.result_label.setText(f'Trustee gave ￡{gain} back to you.')
        window.total_coins_label.setText(str(sess['coins']))
        window.result_label.show()
        window.result_button.show()

    if invest := check_invest():
        # Clear input box
        sess['raise_error'] = False
        window.invest_input.clear()
        sess['raise_error'] = True

        # Hide useless widgets
        window.invest_title.hide()
        window.invest_subtitle.hide()
        window.invest_icon.hide()
        window.invest_input.hide()
        window.confirm_button.hide()

        # Compute remaining coins
        sess['coins'] -= invest
        sess['log'].append([invest])
        window.total_coins_label.setText(str(sess['coins']))

        # Display dealing animation
        window.user_name.show()
        window.agent_name.show()
        window.user_avatar_2.show()
        window.agent_avatar_2.show()
        window.dealing_icon.show()
        dealing_timer = QTimer()
        dealing_timer.timeout.connect(_show_result)
        dealing_timer.start(5000)
        window.dealing_icon.show()


def _result_button_clicked():
    # Hide useless widgets
    window.result_label.hide()
    window.result_button.hide()

    if sess['coins'] > 0 and sess['round'] < cfg['num_rounds']:
        # Start next round
        sess['round'] += 1
        window.invest_title.setText(f'Round {sess["round"]}')
        window.invest_title.show()
        window.invest_subtitle.show()
        window.invest_icon.show()
        window.invest_input.show()
        window.confirm_button.show()
    else:
        # Output logs
        next_page()


def _finish_button_clicked():
    exit()


def init_pages():
    # Page 1
    set_shadow_effect(window.page_1_dialog)
    window.continue_button_active.hide()
    window.state_checkbox.stateChanged.connect(_state_checkbox_changed)
    window.continue_button_active.clicked.connect(next_page)

    # Page 2
    set_shadow_effect(window.page_2_dialog)
    window.gender_error_label.hide()
    window.edu_error_label.hide()
    window.ethnic_error_label.hide()
    window.age_input.setAttribute(Qt.WA_MacShowFocusRect, 0)
    window.ethnic_input.setAttribute(Qt.WA_MacShowFocusRect, 0)
    window.age_input.textChanged.connect(check_age)
    window.male_radio.toggled.connect(check_gender)
    window.female_radio.toggled.connect(check_gender)
    window.edu_combo.currentIndexChanged.connect(check_edu)
    window.ethnic_combo.currentIndexChanged.connect(check_ethnic)
    window.ethnic_input.textChanged.connect(check_ethnic)
    window.continue_button.clicked.connect(_continue_button_clicked)

    # Page 3
    set_shadow_effect(window.page_3_dialog)
    window.intro_text.setPlainText(window.intro_text.toPlainText().format(
        cfg['num_rounds'], cfg['multiplier']))
    window.start_button.clicked.connect(next_page)

    # Page 4
    set_shadow_effect(window.page_4_dialog)
    window.avatar_panel.hide()
    window.agent_avatar_1.hide()
    window.agent_name_label.hide()
    window.agent_age_label.hide()
    window.agent_gender_label.hide()
    window.agent_edu_label.hide()
    window.agent_ethnic_label.hide()
    window.loading_icon.hide()
    window.okay_button.hide()
    window.user_avatar_error_label.hide()
    window.user_name_error_label.hide()
    window.user_name_input.setAttribute(Qt.WA_MacShowFocusRect, 0)
    window.user_name_input.textChanged.connect(check_name)
    window.match_button.clicked.connect(_match_button_clicked)
    window.okay_button.clicked.connect(next_page)
    window.user_avatar_1 = QAvatar('default-avatar', _user_avatar_clicked,
                                   window.user_avatar_1)
    for i, avatar in enumerate(AVATARS):
        QAvatar(avatar, _avatar_clicked, getattr(window, f'avatar_{i}'))
    loading = QMovie('assets/loading.gif')
    loading.start()
    window.loading_icon.setMovie(loading)

    # Page 5
    set_shadow_effect(window.page_5_dialog)
    window.user_name.hide()
    window.agent_name.hide()
    window.user_avatar_2.hide()
    window.agent_avatar_2.hide()
    window.dealing_icon.hide()
    window.result_button.hide()
    window.invest_error_label.hide()
    window.invest_input.setAttribute(Qt.WA_MacShowFocusRect, 0)
    window.total_coins_label.setText(str(sess['coins']))
    window.invest_input.textChanged.connect(check_invest)
    window.confirm_button.clicked.connect(_confirm_button_clicked)
    window.result_button.clicked.connect(_result_button_clicked)
    dealing = QMovie('assets/dealing.gif')
    dealing.start()
    window.dealing_icon.setMovie(dealing)

    # Page 6
    set_shadow_effect(window.page_6_dialog)
    window.finish_button.clicked.connect(_finish_button_clicked)


if __name__ == '__main__':
    # Setup Qt Application
    app = QApplication([])
    window = uic.loadUi('mainwindow.ui')

    # Initialize session and pages
    sess = dict(
        round=1,
        coins=cfg['initial_coins'],
        log=[],
        meta=dict(
            mean=random.choice(cfg['agent']['means']),
            var=random.choice(cfg['agent']['variances'])))
    init_pages()

    # Display main window
    window.show()
    app.exec()
