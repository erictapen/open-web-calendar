# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

import translate
import pytest


@pytest.mark.parametrize(
    "language,file,id,expected_value",
    [
        ("en", "calendar", "language", "English"), 
        ("en", "_test", "id1", "test"), 
        ("en", "_test", "id2", "test2"), 
        ("de", "_test", "id1", "Test"), 
        ("de", "_test", "id2", "test2"), 
        ("en", "_test", "calendar.language", "English"), 
    ]
)
def test_translate(language, file, id, expected_value):
    """Translate the id."""
    assert translate.string(language, file, id) == expected_value



@pytest.mark.parametrize(
    "language,id,value,fill",
    [
        ("en", "id2", '<span id="translate-id2" class="translation">test2</span>', {}), 
        ("en", "test-html", '<span id="translate-test-html" class="translation"><b>Hi!</b></span>', {}), 
        ("en", "check-escape", '<span id="translate-check-escape" class="translation">&lt;nanana&gt;</span>', {}),
        ("en", "format-argument", '<span id="translate-format-argument" class="translation">This is a nice day!</span>', {"sunny": "nice"}), 
        ("en", "format-argument", '<span id="translate-format-argument" class="translation">This is a rainy day!</span>', {"sunny": "rainy"}), 
    ]
)
def test_convert_html(language, id, value, fill):
    """Check that html conversion works."""
    assert translate.html(language, "_test", id, **fill) == value


@pytest.mark.parametrize("language", ["en", "de"])
def test_load_from_common(language):
    assert translate.string(language, "common", "project-description") ==  translate.string(language, "index", "project-description")
    
def test_invalid_id():
    with pytest.raises(KeyError):
        translate.string("en", "common", "invalid-id-for-test")
        

def test_ua_calendar():
    """Check that we get a valid dhtmlx scheduler translation."""
    expected = {'date': {'month_full': ['Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень', 'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень'], 'month_short': ['Січ', 'Лют', 'Бер', 'Кві', 'Тра', 'Чер', 'Лип', 'Сер', 'Вер', 'Жов', 'Лис', 'Гру'], 'day_full': ['Неділя', 'Понеділок', 'Вівторок', 'Середа', 'Четвер', "П'ятниця", 'Субота'], 'day_short': ['Нед', 'Пон', 'Вів', 'Сер', 'Чет', 'Птн', 'Суб']}, 'labels': {'dhx_cal_today_button': 'Сьогодні', 'day_tab': 'День', 'week_tab': 'Тиждень', 'month_tab': 'Місяць', 'new_event': 'Нова подія', 'icon_save': 'Зберегти', 'icon_cancel': 'Відміна', 'icon_details': 'Деталі', 'icon_edit': 'Редагувати', 'icon_delete': 'Вилучити', 'confirm_closing': '', 'confirm_deleting': 'Подія вилучиться назавжди. Ви впевнені?', 'section_description': 'Опис', 'section_time': 'Часовий проміжок', 'full_day': 'Весь день', 'confirm_recurring': 'Хочете редагувати весь перелік повторюваних подій?', 'section_recurring': 'Повторювана подія', 'button_recurring': 'Відключено', 'button_recurring_open': 'Включено', 'button_edit_series': 'Редагувати серію', 'button_edit_occurrence': 'Редагувати примірник', 'agenda_tab': 'Перелік', 'date': 'Дата', 'description': 'Опис', 'year_tab': 'Рік', 'week_agenda_tab': 'Перелік', 'grid_tab': 'Таблиця', 'drag_to_create': 'Drag to create', 'drag_to_move': 'Drag to move', 'message_ok': 'OK', 'message_cancel': 'Cancel', 'next': 'Next', 'prev': 'Previous', 'year': 'Year', 'month': 'Month', 'day': 'Day', 'hour': 'Hour', 'minute': 'Minute', 'repeat_radio_day': 'День', 'repeat_radio_week': 'Тиждень', 'repeat_radio_month': 'Місяць', 'repeat_radio_year': 'Рік', 'repeat_radio_day_type': 'Кожний', 'repeat_text_day_count': 'день', 'repeat_radio_day_type2': 'Кожний робочий день', 'repeat_week': ' Повторювати кожен', 'repeat_text_week_count': 'тиждень , по:', 'repeat_radio_month_type': 'Повторювати', 'repeat_radio_month_start': '', 'repeat_text_month_day': ' числа кожний ', 'repeat_text_month_count': 'місяць', 'repeat_text_month_count2_before': 'кожен ', 'repeat_text_month_count2_after': 'місяць', 'repeat_year_label': '', 'select_year_day2': '', 'repeat_text_year_day': 'день', 'select_year_month': '', 'repeat_radio_end': 'Без дати закінчення', 'repeat_text_occurences_count': 'повторень', 'repeat_radio_end3': 'До ', 'repeat_radio_end2': '', 'month_for_recurring': ['січня', 'лютого', 'березня', 'квітня', 'травня', 'червня', 'липня', 'серпня', 'вересня', 'жовтня', 'листопада', 'грудня'], 'day_for_recurring': ['Неділям', 'Понеділкам', 'Вівторкам', 'Середам', 'Четвергам', "П'ятницям", 'Суботам']}}
    cal = translate.dhtmlx("ua")
    def compare(expected, b, gone=[]):
        for k in expected:
            assert k in b
            if isinstance(expected[k], str):
                assert expected[k] == b[k], ".".join(gone+[k])
            elif isinstance(expected[k], list):
                assert expected[k] == b[k], ".".join(gone+[k])
            elif isinstance(expected[k], dict):
                compare(expected[k], b[k], gone + [k])
            else:
                assert False
    compare(expected, cal)
    
@pytest.mark.parametrize(
    "entry", [
    ("Deutsch", "de"),
    ("English", "en"),
    ('Portuguese', 'pt'),
])
def test_languages_are_listed(entry):
    languages = translate.dhtmlx_languages()
    assert entry in languages


def test_language_alias_is_not_a_translation_language():
    """If this fails, please edit the file to rename language codes properly."""
    for code in translate.LANGUAGE_ALIAS:
        assert code not in translate.TRANSLATIONS


def test_compute_recommendation():
    assert translate.languages_for_the_index_file() != []