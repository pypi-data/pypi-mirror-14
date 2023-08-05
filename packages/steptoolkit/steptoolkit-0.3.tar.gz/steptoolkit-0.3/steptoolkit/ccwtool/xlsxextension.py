# -*- coding: utf-8 -*-

import re
import string
import os

import xlsxwriter

from exchangerate import ExchangeRate


# noinspection PyPep8
class XLSXExtension(object):
    IMAGE_DIR = "{}/images".format(os.path.dirname(__file__))
    data_row_num = None
    data_row_count = 0

    def __init__(self, spec_file):
        self.xlsx_name = xlsxwriter.Workbook(spec_file)
        self.worksheet = self.xlsx_name.add_worksheet()
        self.data_row_num = 14
        self.data_row_count = 0
        self.add_styles()

    # TODO: Нужно переопределить все стили при инициализации
    def add_styles(self):
        self.main_caption = self.xlsx_name.add_format({'valign': 'vcenter'})
        self.main_caption.set_font_name('Arial')
        self.main_caption.set_font_size(16)
        self.main_caption.set_bold()
        self.main_caption.set_indent(1)

        self.address_caption = self.xlsx_name.add_format({'valign': 'vcenter'})
        self.address_caption.set_font_name('Arial')
        self.address_caption.set_font_size(10)
        self.address_caption.set_bold()

        self.version_caption = self.xlsx_name.add_format({'valign': 'vcenter'})
        self.version_caption.set_font_name('Arial')
        self.version_caption.set_font_size(10)
        self.version_caption.set_indent(7)

        self.currency_caption = self.xlsx_name.add_format(
            {'align': 'center', 'valign': 'vcenter', 'bg_color': '#F2DCDB'})
        self.currency_caption.set_font_name('Arial')
        self.currency_caption.set_font_size(10)
        self.currency_caption.set_bold()
        self.currency_caption.set_border(2)
        self.currency_caption.set_color('#000000')

        self.currency_text = self.xlsx_name.add_format({'align': 'center', 'valign': 'vcenter', 'bg_color': '#F2DCDB'})
        self.currency_text.set_font_name('Arial')
        self.currency_text.set_font_size(10)
        self.currency_text.set_border(2)
        self.currency_text.set_color('#000000')

        self.caution_format = self.xlsx_name.add_format({'valign': 'vcenter', 'bg_color': '#F2DCDB'})
        self.caution_format.set_font_name('Arial')
        self.caution_format.set_font_size(16)
        self.caution_format.set_bold()
        self.caution_format.set_color('#FF0000')
        self.caution_format.set_indent(1)
        self.caution_format.set_left(2)
        self.caution_format.set_left_color('#FF0000')

        self.caution_text_format = self.xlsx_name.add_format({'valign': 'vcenter', 'bg_color': '#FFFFFF'})
        self.caution_text_format.set_font_name('Arial')
        self.caution_text_format.set_font_size(10)
        self.caution_text_format.set_bold()
        self.caution_text_format.set_color('#FF0000')
        self.caution_text_format.set_left(2)
        self.caution_text_format.set_left_color('#FF0000')

        self.red_bg_format = self.xlsx_name.add_format({'bg_color': '#F2DCDB'})

        self.red_border_format = self.xlsx_name.add_format()
        self.red_border_format.set_left(2)
        self.red_border_format.set_left_color('#FF0000')
        self.red_border_format.set_bg_color('#F2DCDB')

        self.white_bg_format = self.xlsx_name.add_format({'bg_color': '#FFFFFF'})
        self.white_bg_format.set_border(0)

        self.left_table_header_format = self.xlsx_name.add_format(
            {'align': 'center', 'valign': 'vcenter', 'bg_color': '#FFFFFF'})
        self.left_table_header_format.set_font_name('Arial')
        self.left_table_header_format.set_font_size(11)
        self.left_table_header_format.set_bold()
        self.left_table_header_format.set_color('#000000')
        self.left_table_header_format.set_left(1)
        self.left_table_header_format.set_right(1)
        self.left_table_header_format.set_bottom(1)
        self.left_table_header_format.set_top(2)
        self.left_table_header_format.set_text_wrap()

        self.right_table_header_format = self.xlsx_name.add_format(
            {'align': 'center', 'valign': 'vcenter', 'bg_color': '#FDE9D9'})
        self.right_table_header_format.set_font_name('Arial')
        self.right_table_header_format.set_font_size(11)
        self.right_table_header_format.set_bold()
        self.right_table_header_format.set_color('#000000')
        self.right_table_header_format.set_left(1)
        self.right_table_header_format.set_right(1)
        self.right_table_header_format.set_bottom(1)
        self.right_table_header_format.set_top(2)
        self.right_table_header_format.set_text_wrap()

        self.right_red_table_header_format = self.xlsx_name.add_format(
            {'align': 'center', 'valign': 'vcenter', 'bg_color': '#FDE9D9'})
        self.right_red_table_header_format.set_font_name('Arial')
        self.right_red_table_header_format.set_font_size(11)
        self.right_red_table_header_format.set_bold()
        self.right_red_table_header_format.set_left_color('#FF0000')
        self.right_red_table_header_format.set_left(2)
        self.right_red_table_header_format.set_right(1)
        self.right_red_table_header_format.set_right_color('#000000')
        self.right_red_table_header_format.set_bottom(1)
        self.right_red_table_header_format.set_bottom_color('#000000')
        self.right_red_table_header_format.set_top(2)
        self.right_red_table_header_format.set_top_color('#000000')
        self.right_red_table_header_format.set_text_wrap()

        self.cell_table_header_format = self.xlsx_name.add_format(
            {'align': 'center', 'valign': 'vcenter', 'bg_color': '#FDE9D9'})
        self.cell_table_header_format.set_font_name('Arial')
        self.cell_table_header_format.set_font_size(11)
        self.cell_table_header_format.set_bold()
        self.cell_table_header_format.set_color('#000000')
        self.cell_table_header_format.set_border(1)
        self.cell_table_header_format.set_text_wrap()

        self.cell_red_table_header_format = self.xlsx_name.add_format(
            {'align': 'center', 'valign': 'vcenter', 'bg_color': '#FDE9D9'})
        self.cell_red_table_header_format.set_font_name('Arial')
        self.cell_red_table_header_format.set_font_size(11)
        self.cell_red_table_header_format.set_bold()
        self.cell_red_table_header_format.set_right(1)
        self.cell_red_table_header_format.set_right_color('#000000')
        self.cell_red_table_header_format.set_left(2)
        self.cell_red_table_header_format.set_left_color('#FF0000')
        self.cell_red_table_header_format.set_top(1)
        self.cell_red_table_header_format.set_top_color('#000000')
        self.cell_red_table_header_format.set_bottom(1)
        self.cell_red_table_header_format.set_bottom_color('#000000')
        self.cell_red_table_header_format.set_text_wrap()

        self.title_cell_table_header_format = self.xlsx_name.add_format(
            {'align': 'left', 'valign': 'vcenter', 'bg_color': '#008080'})
        self.title_cell_table_header_format.set_font_name('Arial')
        self.title_cell_table_header_format.set_font_size(14)
        self.title_cell_table_header_format.set_bold()
        self.title_cell_table_header_format.set_top_color('#000000')
        self.title_cell_table_header_format.set_top(1)
        self.title_cell_table_header_format.set_bottom_color('#000000')
        self.title_cell_table_header_format.set_bottom(1)
        self.title_cell_table_header_format.set_font_color('#FFFFFF')

        self.title_cell_red_table_header_format = self.xlsx_name.add_format(
            {'align': 'left', 'valign': 'vcenter', 'bg_color': '#008080'})
        self.title_cell_red_table_header_format.set_font_name('Arial')
        self.title_cell_red_table_header_format.set_font_size(14)
        self.title_cell_red_table_header_format.set_bold()
        self.title_cell_red_table_header_format.set_top_color('#000000')
        self.title_cell_red_table_header_format.set_top(1)
        self.title_cell_red_table_header_format.set_bottom_color('#000000')
        self.title_cell_red_table_header_format.set_bottom(1)
        self.title_cell_red_table_header_format.set_right_color('#000000')
        self.title_cell_red_table_header_format.set_right(0)
        self.title_cell_red_table_header_format.set_left_color('#FF0000')
        self.title_cell_red_table_header_format.set_left(2)
        self.title_cell_red_table_header_format.set_font_color('#FFFFFF')

        self.summ_cell_table_header_format = self.xlsx_name.add_format(
            {'align': 'left', 'valign': 'vcenter', 'bg_color': '#FFFFFF'})
        self.summ_cell_table_header_format.set_font_name('Arial')
        self.summ_cell_table_header_format.set_font_size(11)
        self.summ_cell_table_header_format.set_bold()
        self.summ_cell_table_header_format.set_color('#000000')
        self.summ_cell_table_header_format.set_border(1)
        self.summ_cell_table_header_format.set_font_color('#008080')

        self.summ_dollars_cell_table_header_format = self.xlsx_name.add_format(
            {'align': 'right', 'valign': 'vcenter', 'bg_color': '#FFFFFF'})
        self.summ_dollars_cell_table_header_format.set_font_name('Arial')
        self.summ_dollars_cell_table_header_format.set_font_size(11)
        self.summ_dollars_cell_table_header_format.set_bold()
        self.summ_dollars_cell_table_header_format.set_color('#000000')
        self.summ_dollars_cell_table_header_format.set_border(1)
        self.summ_dollars_cell_table_header_format.set_font_color('#008080')
        self.summ_dollars_cell_table_header_format.set_num_format('$#,##0.00')

        self.summ_dollars_red_cell_table_header_format = self.xlsx_name.add_format(
            {'align': 'right', 'valign': 'vcenter', 'bg_color': '#FFFFFF'})
        self.summ_dollars_red_cell_table_header_format.set_font_name('Arial')
        self.summ_dollars_red_cell_table_header_format.set_font_size(11)
        self.summ_dollars_red_cell_table_header_format.set_bold()
        self.summ_dollars_red_cell_table_header_format.set_top_color('#000000')
        self.summ_dollars_red_cell_table_header_format.set_top(1)
        self.summ_dollars_red_cell_table_header_format.set_bottom_color('#000000')
        self.summ_dollars_red_cell_table_header_format.set_bottom(1)
        self.summ_dollars_red_cell_table_header_format.set_right_color('#000000')
        self.summ_dollars_red_cell_table_header_format.set_right(1)
        self.summ_dollars_red_cell_table_header_format.set_left_color('#FF0000')
        self.summ_dollars_red_cell_table_header_format.set_left(2)
        self.summ_dollars_red_cell_table_header_format.set_font_color('#008080')
        self.summ_dollars_red_cell_table_header_format.set_num_format('$#,##0.00')

        self.summ_euros_cell_table_header_format = self.xlsx_name.add_format(
            {'align': 'right', 'valign': 'vcenter', 'bg_color': '#FFFFFF'})
        self.summ_euros_cell_table_header_format.set_font_name('Arial')
        self.summ_euros_cell_table_header_format.set_font_size(11)
        self.summ_euros_cell_table_header_format.set_bold()
        self.summ_euros_cell_table_header_format.set_color('#000000')
        self.summ_euros_cell_table_header_format.set_border(1)
        self.summ_euros_cell_table_header_format.set_font_color('#008080')
        self.summ_euros_cell_table_header_format.set_num_format(u'€#,##0.00')

        self.summ_rubles_cell_table_header_format = self.xlsx_name.add_format(
            {'align': 'right', 'valign': 'vcenter', 'bg_color': '#FFFFFF'})
        self.summ_rubles_cell_table_header_format.set_font_name('Arial')
        self.summ_rubles_cell_table_header_format.set_font_size(11)
        self.summ_rubles_cell_table_header_format.set_bold()
        self.summ_rubles_cell_table_header_format.set_color('#000000')
        self.summ_rubles_cell_table_header_format.set_border(1)
        self.summ_rubles_cell_table_header_format.set_font_color('#008080')
        self.summ_rubles_cell_table_header_format.set_num_format(u'#,##0.00р\.')

        self.summ_percents_cell_table_header_format = self.xlsx_name.add_format(
            {'align': 'right', 'valign': 'vcenter', 'bg_color': '#FFFFFF'})
        self.summ_percents_cell_table_header_format.set_font_name('Arial')
        self.summ_percents_cell_table_header_format.set_font_size(11)
        self.summ_percents_cell_table_header_format.set_bold()
        self.summ_percents_cell_table_header_format.set_color('#000000')
        self.summ_percents_cell_table_header_format.set_border(1)
        self.summ_percents_cell_table_header_format.set_font_color('#008080')
        self.summ_percents_cell_table_header_format.set_num_format(0x0a)

        self.footer_normal_cell_table_header_format = self.xlsx_name.add_format({'valign': 'vcenter'})
        self.footer_normal_cell_table_header_format.set_font_name('Arial')
        self.footer_normal_cell_table_header_format.set_font_size(11)
        self.footer_normal_cell_table_header_format.set_bold()
        self.footer_normal_cell_table_header_format.set_indent(1)

        self.footer_italic_cell_table_header_format = self.xlsx_name.add_format({'valign': 'vcenter'})
        self.footer_italic_cell_table_header_format.set_font_name('Arial')
        self.footer_italic_cell_table_header_format.set_italic()
        self.footer_italic_cell_table_header_format.set_font_size(12)
        self.footer_italic_cell_table_header_format.set_indent(1)

        self.footer_bold_cell_table_header_format = self.xlsx_name.add_format({'valign': 'vcenter'})
        self.footer_bold_cell_table_header_format.set_font_name('Arial')
        self.footer_bold_cell_table_header_format.set_font_size(12)
        self.footer_bold_cell_table_header_format.set_bold()
        self.footer_bold_cell_table_header_format.set_italic()

        self.footer_common_cell_table_header_format = self.xlsx_name.add_format({'valign': 'vcenter'})
        self.footer_common_cell_table_header_format.set_indent(1)

        self.red_border_white_bg_format = self.xlsx_name.add_format()
        self.red_border_white_bg_format.set_left(2)
        self.red_border_white_bg_format.set_left_color('#FF0000')
        self.red_border_white_bg_format.set_bg_color('#FFFFFF')

        self.product_center_format = self.xlsx_name.add_format(
            {'align': 'center', 'valign': 'vcenter', 'bg_color': '#FFFFFF'})
        self.product_center_format.set_font_name('Arial')
        self.product_center_format.set_font_size(10)
        self.product_center_format.set_color('#000000')
        self.product_center_format.set_border(1)
        self.product_center_format.set_font_color('#000000')

        self.product_center_red_format = self.xlsx_name.add_format(
            {'align': 'center', 'valign': 'vcenter', 'bg_color': '#FFFFFF'})
        self.product_center_red_format.set_font_name('Arial')
        self.product_center_red_format.set_font_size(10)
        self.product_center_red_format.set_top_color('#000000')
        self.product_center_red_format.set_top(1)
        self.product_center_red_format.set_bottom_color('#000000')
        self.product_center_red_format.set_bottom(1)
        self.product_center_red_format.set_right_color('#000000')
        self.product_center_red_format.set_right(1)
        self.product_center_red_format.set_left_color('#FF0000')
        self.product_center_red_format.set_left(2)
        self.product_center_red_format.set_font_color('#000000')

        self.product_left_format = self.xlsx_name.add_format(
            {'align': 'left', 'valign': 'vcenter', 'bg_color': '#FFFFFF'})
        self.product_left_format.set_font_name('Arial')
        self.product_left_format.set_font_size(10)
        self.product_left_format.set_color('#000000')
        self.product_left_format.set_border(1)
        self.product_left_format.set_font_color('#000000')

        self.product_left_indent_format = self.xlsx_name.add_format(
            {'align': 'left', 'valign': 'vcenter', 'bg_color': '#FFFFFF'})
        self.product_left_indent_format.set_font_name('Arial')
        self.product_left_indent_format.set_font_size(10)
        self.product_left_indent_format.set_color('#000000')
        self.product_left_indent_format.set_border(1)
        self.product_left_indent_format.set_font_color('#000000')
        self.product_left_indent_format.set_indent(1)

        self.product_dollars_format = self.xlsx_name.add_format(
            {'align': 'right', 'valign': 'vcenter', 'bg_color': '#FFFFFF'})
        self.product_dollars_format.set_font_name('Arial')
        self.product_dollars_format.set_font_size(10)
        self.product_dollars_format.set_color('#000000')
        self.product_dollars_format.set_border(1)
        self.product_dollars_format.set_font_color('#000000')
        self.product_dollars_format.set_num_format('$#,##0.00')

        self.product_dollars_red_format = self.xlsx_name.add_format(
            {'align': 'right', 'valign': 'vcenter', 'bg_color': '#FFFFFF'})
        self.product_dollars_red_format.set_font_name('Arial')
        self.product_dollars_red_format.set_font_size(10)
        self.product_dollars_red_format.set_top_color('#000000')
        self.product_dollars_red_format.set_top(1)
        self.product_dollars_red_format.set_bottom_color('#000000')
        self.product_dollars_red_format.set_bottom(1)
        self.product_dollars_red_format.set_right_color('#000000')
        self.product_dollars_red_format.set_right(1)
        self.product_dollars_red_format.set_left_color('#FF0000')
        self.product_dollars_red_format.set_left(2)
        self.product_dollars_red_format.set_font_color('#000000')
        self.product_dollars_red_format.set_num_format('$#,##0.00')

        self.product_euros_format = self.xlsx_name.add_format(
            {'align': 'right', 'valign': 'vcenter', 'bg_color': '#FFFFFF'})
        self.product_euros_format.set_font_name('Arial')
        self.product_euros_format.set_font_size(10)
        self.product_euros_format.set_color('#000000')
        self.product_euros_format.set_border(1)
        self.product_euros_format.set_font_color('#000000')
        self.product_euros_format.set_num_format(u'€#,##0.00')

        self.product_rubles_format = self.xlsx_name.add_format(
            {'align': 'right', 'valign': 'vcenter', 'bg_color': '#FFFFFF'})
        self.product_rubles_format.set_font_name('Arial')
        self.product_rubles_format.set_font_size(10)
        self.product_rubles_format.set_color('#000000')
        self.product_rubles_format.set_border(1)
        self.product_rubles_format.set_font_color('#000000')
        self.product_rubles_format.set_num_format(u'#,##0.00р\.')

        self.product_percents_format = self.xlsx_name.add_format(
            {'align': 'right', 'valign': 'vcenter', 'bg_color': '#FFFFFF'})
        self.product_percents_format.set_font_name('Arial')
        self.product_percents_format.set_font_size(10)
        self.product_percents_format.set_color('#000000')
        self.product_percents_format.set_border(1)
        self.product_percents_format.set_font_color('#000000')
        self.product_percents_format.set_num_format(0x0a)

        self.product_right_format = self.xlsx_name.add_format(
            {'align': 'right', 'valign': 'vcenter', 'bg_color': '#FFFFFF'})
        self.product_right_format.set_font_name('Arial')
        self.product_right_format.set_font_size(10)
        self.product_right_format.set_color('#000000')
        self.product_right_format.set_border(1)
        self.product_right_format.set_font_color('#000000')

    def add_header(self, **meta):
        column_with_fixed_width = {'A': 4.14, 'B': 19.86, 'C': 21.57, 'D': 65.71, 'E': 5.43, 'F': 5.14, 'G': 11.43,
                                   'H': 10.29, 'I': 19.71, 'J': 22.14, 'K': 15.29, 'L': 10.57, 'M': 10.57, 'N': 14.57,
                                   'O': 14.57, 'P': 14.14, 'Q': 17.14, 'R': 13.14, 'S': 12, 'T': 12, 'U': 15.71,
                                   'V': 15.71, 'W': 18.71}

        exchange_rates = ExchangeRate()

        for column in column_with_fixed_width:
            column_str = column + ":" + column
            column_format = None
            if re.search('[I-W]', column):
                column_format = self.white_bg_format
            self.worksheet.set_column(column_str, column_with_fixed_width[column], column_format)

        for column in column_with_fixed_width:
            for row in range(11):
                row_format = None
                if column == "I":
                    row_format = self.red_border_format
                elif column == "W":
                    tmp_format = self.xlsx_name.add_format()
                    tmp_format.set_left(2)
                    tmp_format.set_left_color('#FF0000')
                    tmp_format.set_bg_color('#FFFFFF')
                    row_format = tmp_format
                elif re.search('[J-V]', column):
                    row_format = self.red_bg_format
                row_str = column + str(row + 1)
                self.worksheet.write(row_str, None, row_format)

        self.worksheet.insert_image('B1', "{}/logo.jpg".format(XLSXExtension.IMAGE_DIR),
                                    {'x_scale': 0.15, 'y_scale': 0.15, 'x_offset': 2, 'y_offset': 4})

        self.worksheet.write('A5', u'СПЕЦИФИКАЦИЯ НА ОБОРУДОВАНИЕ, МАТЕРИАЛЫ И ВЕДОМОСТЬ ОБЪЕМА РАБОТ',
                             self.main_caption)
        self.worksheet.write('A7', (u'Наименование объекта, адрес: %s' % meta['customer_name'].decode('utf-8')),
                             self.main_caption)

        self.worksheet.write('D1', u'127018, Россия, Москва, ул. Полковая, д.3, стр.3', self.address_caption)
        self.worksheet.write('D2', u'Тел.: +7 (495) 775-3120, 363-0133     Факс: +7 (495) 363-01-34',
                             self.address_caption)
        self.worksheet.write('D3', u'E-mail: info@step.ru     http://www.step.ru', self.address_caption)

        self.worksheet.write('D9', (u'Версия: %s' % meta['version']), self.version_caption)
        self.worksheet.write('D10', (u'Дата составления: %s' % meta['date']),
                             self.version_caption)

        self.worksheet.write('L4', u'Валюта', self.currency_caption)
        self.worksheet.write('M4', u'Курс', self.currency_caption)
        self.worksheet.write('L5', u'$', self.currency_caption)
        self.worksheet.write('M5', exchange_rates.get_value('USD'), self.currency_text)
        self.worksheet.write('L6', u'€', self.currency_caption)
        self.worksheet.write('M6', exchange_rates.get_value('EUR'), self.currency_text)

        self.worksheet.write('I10', u'УДАЛИТЬ ЭТИ столбцы перед ОТПРАВКОЙ ЗАКАЗЧИКУ', self.caution_format)
        self.worksheet.write('W11', u'Столбец скрыть', self.caution_text_format)

        # noinspection PyPep8
        table_header_data = [u"№ п.п.", u"Производитель, страна", u"Артикул", u"Номенклатура", u"Ед. изм.", u"К-во",
                             u"Цена", u"Сумма", {u"GPL (Cisco) / Рекомендованные вендором": [u"Цена, $", u"Сумма, $"]},
                             {u"Входные цены (ЦБ РФ)": [u"Трудозатраты, чел/день", u"Цена, р", u"Цена, €", u"Цена, $",
                                                        u"Сумма, $"]},
                             {u"Рекомендованные к продаже": [u"Цена, $", u"Сумма, $"]},
                             {u"Маржа": [u"абсолютная", u"в %"]},
                             u"Срок поставки на склад СТЭПа", u"Автор данных (ФИО)", u"Дата заполнения",
                             u"Код товара/услуги (1С)"]

        table_header_columms = string.uppercase[:23]
        column_index = 0
        for item in table_header_data:
            if type(item) == unicode:
                merge_str = table_header_columms[column_index] + "12:" + table_header_columms[column_index] + "13"
                if re.search('[A-H]', merge_str):
                    merge_format = self.left_table_header_format
                else:
                    if re.search('[W]', merge_str):
                        merge_format = self.right_red_table_header_format
                    else:
                        merge_format = self.right_table_header_format
                self.worksheet.merge_range(merge_str, item, merge_format)
                column_index += 1
            elif type(item) == dict:
                last_column_index = column_index + len(item.values()[0]) - 1
                merge_str = table_header_columms[column_index] + "12:" + table_header_columms[last_column_index] + "12"
                if re.search('[A-H]', merge_str):
                    merge_format = self.left_table_header_format
                else:
                    if re.search('[I]', merge_str):
                        merge_format = self.right_red_table_header_format
                    else:
                        merge_format = self.right_table_header_format
                self.worksheet.merge_range(merge_str, item.keys()[0], merge_format)

                for itemA in item.values()[0]:
                    cell_str = table_header_columms[column_index] + "13"
                    cell_format = self.cell_table_header_format
                    if re.search('I', cell_str):
                        cell_format = self.cell_red_table_header_format
                    self.worksheet.write(cell_str, itemA, cell_format)
                    column_index += 1

        for col in range(23):
            cell_str = table_header_columms[col] + "14"
            if cell_str == "D14":
                self.worksheet.write(cell_str, u'Оборудование', self.title_cell_table_header_format)
            elif re.search('[IW]', cell_str):
                self.worksheet.write(cell_str, None, self.title_cell_red_table_header_format)
            else:
                self.worksheet.write(cell_str, None, self.title_cell_table_header_format)

    def add_products(self, products):
        count = 1
        for product in products:
            self.worksheet.set_row(self.data_row_num, 15.75)
            self.worksheet.write_string(('A' + str(self.data_row_num + 1)), str(count), self.product_center_format)
            self.worksheet.write(('B' + str(self.data_row_num + 1)), u'Cisco Systems, США', self.product_left_format)
            self.worksheet.write(('C' + str(self.data_row_num + 1)), product['name'], self.product_left_format)
            self.worksheet.write(('D' + str(self.data_row_num + 1)), product['description'],
                                 self.product_left_indent_format)
            self.worksheet.write(('E' + str(self.data_row_num + 1)), u'шт.', self.product_center_format)
            self.worksheet.write(('F' + str(self.data_row_num + 1)), int(product['count']),
                                 self.product_center_format)
            self.worksheet.write(('G' + str(self.data_row_num + 1)), None, self.product_dollars_format)
            self.worksheet.write(('H' + str(self.data_row_num + 1)),
                                 ('=F' + str(self.data_row_num + 1) + "*" + 'G' + str(self.data_row_num + 1)),
                                 self.product_dollars_format)
            self.worksheet.write(('I' + str(self.data_row_num + 1)), float(product['price']),
                                 self.product_dollars_red_format)
            self.worksheet.write(('J' + str(self.data_row_num + 1)),
                                 ('=F' + str(self.data_row_num + 1) + "*" + 'I' + str(self.data_row_num + 1)),
                                 self.product_dollars_format)
            self.worksheet.write(('K' + str(self.data_row_num + 1)), None, self.product_right_format)
            self.worksheet.write(('L' + str(self.data_row_num + 1)), None, self.product_rubles_format)
            self.worksheet.write(('M' + str(self.data_row_num + 1)), None, self.product_euros_format)
            # noinspection PyPep8
            self.worksheet.write(('N' + str(self.data_row_num + 1)), (
                '=(IF($M$5=0,0,(IF(M' + str(self.data_row_num + 1) + '=0,L' + str(
                    self.data_row_num + 1) + '/$M$5,M' + str(
                    self.data_row_num + 1) + '*$M$6/$M$5))))'), self.product_dollars_format)
            self.worksheet.write(('O' + str(self.data_row_num + 1)),
                                 ('=N' + str(self.data_row_num + 1) + '*F' + str(self.data_row_num + 1)),
                                 self.product_dollars_format)
            self.worksheet.write(('P' + str(self.data_row_num + 1)), None, self.product_dollars_format)
            self.worksheet.write(('Q' + str(self.data_row_num + 1)),
                                 ('=P' + str(self.data_row_num + 1) + '*F' + str(self.data_row_num + 1)),
                                 self.product_dollars_format)
            self.worksheet.write(('R' + str(self.data_row_num + 1)),
                                 ('=H' + str(self.data_row_num + 1) + '-O' + str(self.data_row_num + 1)),
                                 self.product_dollars_format)
            # noinspection PyPep8
            self.worksheet.write(('S' + str(self.data_row_num + 1)), (
                '=(H' + str(self.data_row_num + 1) + '-O' + str(self.data_row_num + 1) + ')/H' + str(
                    self.data_row_num + 1)), self.product_percents_format)
            self.worksheet.write(('T' + str(self.data_row_num + 1)), None, self.product_center_format)
            self.worksheet.write(('U' + str(self.data_row_num + 1)), None, self.product_center_format)
            self.worksheet.write(('V' + str(self.data_row_num + 1)), None, self.product_center_format)
            self.worksheet.write(('W' + str(self.data_row_num + 1)), None, self.product_center_red_format)
            self.data_row_num += 1
            self.data_row_count += 1
            i = 1
            for component in product['components']:
                self.worksheet.set_row(self.data_row_num, 15.75)
                self.worksheet.write_string(('A' + str(self.data_row_num + 1)), (str(count) + "." + str(i)),
                                            self.product_center_format)
                self.worksheet.write(('B' + str(self.data_row_num + 1)), u'Cisco Systems, США',
                                     self.product_left_format)
                self.worksheet.write(('C' + str(self.data_row_num + 1)), component['name'], self.product_left_format)
                self.worksheet.write(('D' + str(self.data_row_num + 1)), component['description'],
                                     self.product_left_indent_format)
                self.worksheet.write(('E' + str(self.data_row_num + 1)), u'шт.', self.product_center_format)
                self.worksheet.write(('F' + str(self.data_row_num + 1)), int(component['count']),
                                     self.product_center_format)
                self.worksheet.write(('G' + str(self.data_row_num + 1)), None, self.product_dollars_format)
                self.worksheet.write(('H' + str(self.data_row_num + 1)),
                                     ('=F' + str(self.data_row_num + 1) + "*" + 'G' + str(self.data_row_num + 1)),
                                     self.product_dollars_format)
                self.worksheet.write(('I' + str(self.data_row_num + 1)), float(component['price']),
                                     self.product_dollars_red_format)
                self.worksheet.write(('J' + str(self.data_row_num + 1)),
                                     ('=F' + str(self.data_row_num + 1) + "*" + 'I' + str(self.data_row_num + 1)),
                                     self.product_dollars_format)
                self.worksheet.write(('K' + str(self.data_row_num + 1)), None, self.product_right_format)
                self.worksheet.write(('L' + str(self.data_row_num + 1)), None, self.product_rubles_format)
                self.worksheet.write(('M' + str(self.data_row_num + 1)), None, self.product_euros_format)
                # noinspection PyPep8,PyPep8
                self.worksheet.write(('N' + str(self.data_row_num + 1)), (
                    '=(IF($M$5=0,0,(IF(M' + str(self.data_row_num + 1) + '=0,L' + str(
                        self.data_row_num + 1) + '/$M$5,M' + str(self.data_row_num + 1) + '*$M$6/$M$5))))'),
                                     self.product_dollars_format)
                self.worksheet.write(('O' + str(self.data_row_num + 1)),
                                     ('=N' + str(self.data_row_num + 1) + '*F' + str(self.data_row_num + 1)),
                                     self.product_dollars_format)
                self.worksheet.write(('P' + str(self.data_row_num + 1)), None, self.product_dollars_format)
                self.worksheet.write(('Q' + str(self.data_row_num + 1)),
                                     ('=P' + str(self.data_row_num + 1) + '*F' + str(self.data_row_num + 1)),
                                     self.product_dollars_format)
                self.worksheet.write(('R' + str(self.data_row_num + 1)),
                                     ('=H' + str(self.data_row_num + 1) + '-O' + str(self.data_row_num + 1)),
                                     self.product_dollars_format)
                # noinspection PyPep8
                self.worksheet.write(('S' + str(self.data_row_num + 1)), (
                    '=(H' + str(self.data_row_num + 1) + '-O' + str(self.data_row_num + 1) + ')/H' + str(
                        self.data_row_num + 1)), self.product_percents_format)
                self.worksheet.write(('T' + str(self.data_row_num + 1)), None, self.product_center_format)
                self.worksheet.write(('U' + str(self.data_row_num + 1)), None, self.product_center_format)
                self.worksheet.write(('V' + str(self.data_row_num + 1)), None, self.product_center_format)
                self.worksheet.write(('W' + str(self.data_row_num + 1)), None, self.product_center_red_format)
                self.data_row_num += 1
                self.data_row_count += 1
                i += 1
            for service in product['services']:
                self.worksheet.set_row(self.data_row_num, 15.75)
                self.worksheet.write_string(('A' + str(self.data_row_num + 1)), (str(count) + "." + str(i)),
                                            self.product_center_format)
                self.worksheet.write(('B' + str(self.data_row_num + 1)), u'Cisco Systems, США',
                                     self.product_left_format)
                self.worksheet.write(('C' + str(self.data_row_num + 1)), service['name'], self.product_left_format)
                self.worksheet.write(('D' + str(self.data_row_num + 1)), service['description'],
                                     self.product_left_indent_format)
                self.worksheet.write(('E' + str(self.data_row_num + 1)), u'шт.', self.product_center_format)
                self.worksheet.write(('F' + str(self.data_row_num + 1)), int(service['count']),
                                     self.product_center_format)
                self.worksheet.write(('G' + str(self.data_row_num + 1)), None, self.product_dollars_format)
                self.worksheet.write(('H' + str(self.data_row_num + 1)),
                                     ('=F' + str(self.data_row_num + 1) + "*" + 'G' + str(self.data_row_num + 1)),
                                     self.product_dollars_format)
                self.worksheet.write(('I' + str(self.data_row_num + 1)), float(service['price']),
                                     self.product_dollars_red_format)
                self.worksheet.write(('J' + str(self.data_row_num + 1)),
                                     ('=F' + str(self.data_row_num + 1) + "*" + 'I' + str(self.data_row_num + 1)),
                                     self.product_dollars_format)
                self.worksheet.write(('K' + str(self.data_row_num + 1)), None, self.product_right_format)
                self.worksheet.write(('L' + str(self.data_row_num + 1)), None, self.product_rubles_format)
                self.worksheet.write(('M' + str(self.data_row_num + 1)), None, self.product_euros_format)
                # noinspection PyPep8,PyPep8
                self.worksheet.write(('N' + str(self.data_row_num + 1)), (
                    '=(IF($M$5=0,0,(IF(M' + str(self.data_row_num + 1) + '=0,L' + str(
                        self.data_row_num + 1) + '/$M$5,M' + str(self.data_row_num + 1) + '*$M$6/$M$5))))'),
                                     self.product_dollars_format)
                self.worksheet.write(('O' + str(self.data_row_num + 1)),
                                     ('=N' + str(self.data_row_num + 1) + '*F' + str(self.data_row_num + 1)),
                                     self.product_dollars_format)
                self.worksheet.write(('P' + str(self.data_row_num + 1)), None, self.product_dollars_format)
                self.worksheet.write(('Q' + str(self.data_row_num + 1)),
                                     ('=P' + str(self.data_row_num + 1) + '*F' + str(self.data_row_num + 1)),
                                     self.product_dollars_format)
                self.worksheet.write(('R' + str(self.data_row_num + 1)),
                                     ('=H' + str(self.data_row_num + 1) + '-O' + str(self.data_row_num + 1)),
                                     self.product_dollars_format)
                # noinspection PyPep8
                self.worksheet.write(('S' + str(self.data_row_num + 1)), (
                    '=(H' + str(self.data_row_num + 1) + '-O' + str(self.data_row_num + 1) + ')/H' + str(
                        self.data_row_num + 1)), self.product_percents_format)
                self.worksheet.write(('T' + str(self.data_row_num + 1)), None, self.product_center_format)
                self.worksheet.write(('U' + str(self.data_row_num + 1)), None, self.product_center_format)
                self.worksheet.write(('V' + str(self.data_row_num + 1)), None, self.product_center_format)
                self.worksheet.write(('W' + str(self.data_row_num + 1)), None, self.product_center_red_format)
                self.data_row_num += 1
                self.data_row_count += 1
            count += 1

    def add_summary(self):
        self.worksheet.set_row(self.data_row_num, 15.75)
        self.worksheet.set_row(self.data_row_num, 15.75)
        self.worksheet.set_row((self.data_row_num + 3), 15.75)
        self.worksheet.set_row((self.data_row_num + 4), 15.75)
        self.worksheet.set_row((self.data_row_num + 5), 15.75)
        self.worksheet.set_row((self.data_row_num + 6), 15.75)
        self.worksheet.set_row((self.data_row_num + 7), 15.75)

        self.worksheet.write(('D' + str(self.data_row_num + 1)), u"Итого за оборудование",
                             self.summ_cell_table_header_format)

        summ_data_cells = ['G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S']

        for cell in summ_data_cells:
            cell_str = cell + str(self.data_row_num + 1)
            cell_data = 0.00

            if re.search('L', cell_str):
                cell_format = self.summ_rubles_cell_table_header_format
            elif re.search('M', cell_str):
                cell_format = self.summ_euros_cell_table_header_format
            elif re.search('S', cell_str):
                cell_format = self.summ_percents_cell_table_header_format
            else:
                if re.search('I', cell_str):
                    cell_format = self.summ_dollars_red_cell_table_header_format
                else:
                    cell_format = self.summ_dollars_cell_table_header_format

            if self.data_row_count > 0:
                cell_data = "=SUM(" + cell + str(self.data_row_num - self.data_row_count + 1) + ":" + cell + str(
                    self.data_row_num) + ")"
                self.worksheet.write_formula(cell_str, cell_data, cell_format)
            else:
                self.worksheet.write(cell_str, int(cell_data), cell_format)

    def add_body(self, products):
        self.add_products(products)
        self.add_summary()

    def add_footer(self):
        self.worksheet.write_rich_string(("A" + str((self.data_row_num + 3))), u'Цены  - ',
                                         self.footer_bold_cell_table_header_format, u'DDP Москва',
                                         self.footer_italic_cell_table_header_format,
                                         u'. Включая НДС. Курс оплаты по безналичному расчету ЦБРФ.',
                                         self.footer_italic_cell_table_header_format)
        self.worksheet.write(("A" + str((self.data_row_num + 5))), u'Срок исполнения:',
                             self.footer_italic_cell_table_header_format)

        self.worksheet.write(("A" + str((self.data_row_num + 7))), u'Надеемся, что наше предложение Вас заинтересует',
                             self.footer_normal_cell_table_header_format)

        self.worksheet.set_column('I:I', 19.71, self.red_border_white_bg_format)
        self.worksheet.set_column('W:W', 18.71, self.red_border_white_bg_format)

    def close(self):
        self.xlsx_name.close()
