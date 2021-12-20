from datetime import date
from io import BytesIO
from typing import List

import xlrd
import xlwt
from xlwt import XFStyle, Borders, easyfont

from certificates.models import Certificate

NUMBER_OF_CERTIFICATE_COLS = 8
NUMBER_OF_CERTIFICATE_FIELDS = 4


class ParsedCertificate:
    contract_n = None
    certificate_n = None
    pinfl = None
    full_name = None
    date_received = None

    @property
    def has_contract_n(self):
        return self.contract_n is not None

    @property
    def has_certificate_n(self):
        return self.certificate_n is not None

    @property
    def has_pinfl(self):
        return self.pinfl is not None

    @property
    def has_full_name(self):
        return self.full_name is not None

    @property
    def has_date_received(self):
        return self.date_received is not None

    def set_contract_n(self, contract_n):
        try:
            self.contract_n = int(contract_n)
        except ValueError:
            pass

    def set_certificate_n(self, certificate_n):
        if certificate_n == "":
            self.certificate_n = None
        else:
            try:
                temp_certificate_n = str(int(certificate_n))
                certificate_n = "0" * (3-len(temp_certificate_n)) + temp_certificate_n
            except ValueError:
                pass
            self.certificate_n = certificate_n

    def set_pinfl(self, pinfl):
        try:
            self.pinfl = int(pinfl)
        except ValueError:
            pass

    def set_full_name(self, full_name):
        self.full_name = str(full_name)
        if self.full_name == "":
            self.full_name = None

    def set_date_received(self, day, month, year):
        try:
            day = int(day)
            month = int(month)
            year = int(year)
            self.date_received = date(day=day, month=month, year=pad_year(year))
        except ValueError:
            pass

    def filled_fields(self):
        count = 0
        if self.certificate_n is not None:
            count += 1
        if self.pinfl is not None:
            count += 1
        if self.full_name is not None:
            count += 1
        if self.date_received is not None:
            count += 1
        return count

    def is_correct(self):
        return self.filled_fields() == NUMBER_OF_CERTIFICATE_FIELDS

def populate_certificate(model_certificate, parsed_certificate):
    model_certificate.full_name = parsed_certificate.full_name
    model_certificate.certificate_n = parsed_certificate.certificate_n
    model_certificate.contract_n = parsed_certificate.contract_n
    model_certificate.date_received = parsed_certificate.date_received


def broken_certificates_report(broken_certificates: List[ParsedCertificate]):
    report = ""
    completely_wrong = 0
    for certificate in broken_certificates:
        if certificate.has_pinfl:
            wrong_fields = "<u>Имя</u>, " if not certificate.has_full_name else ""
            wrong_fields += "<u>Дата получения</u>, " if not certificate.has_date_received else ""
            wrong_fields += "<u>Номер сертификата</u>, " if not certificate.has_certificate_n else ""

            wrong_fields = wrong_fields[:-2]

            cert_string = f"""<p style="margin-bottom: 6px"><b>{certificate.full_name if certificate.has_full_name else certificate.pinfl_or_inn}</b> - <i>Ошибки в полях:</i> {wrong_fields}</p>"""
            report += cert_string
        else:
            completely_wrong += 1

    incorrect_certificates_n = len(broken_certificates) - completely_wrong

    report = f"""<h3 style="margin-bottom: 10px">Некорректных сертификатов: {incorrect_certificates_n}</h3>{report}"""
    return incorrect_certificates_n, report


def pad_year(year: int):
    if year < 1000:
        year = 2000 + year
    return year


def parse_excel(file):
    excel = xlrd.open_workbook(file_contents=file.read())
    sheets = excel.sheet_names()

    correct_certificates = []
    broken_certificates = []
    sheets_used = []

    for sheet in sheets:  # Loop through lists
        sheet = excel.sheet_by_name(sheet)
        for row in sheet.get_rows():  # Loop through rows in sheet
            if len(row) == NUMBER_OF_CERTIFICATE_COLS:
                new_certificate = ParsedCertificate()
                new_certificate.set_full_name(row[1].value)
                new_certificate.set_contract_n(row[2].value)
                new_certificate.set_pinfl(row[3].value)
                new_certificate.set_date_received(row[4].value, row[5].value, row[6].value)
                new_certificate.set_certificate_n(row[7].value)

                if new_certificate.is_correct():
                    correct_certificates.append(new_certificate)
                    if sheet not in sheets_used:
                        sheets_used.append(sheet)
                else:
                    broken_certificates.append(new_certificate)

    print(f"Сломаны: {len(broken_certificates)}\t\tНормальные: {len(correct_certificates)}")

    return correct_certificates, broken_certificates

def build_certificate_excel(queryset):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("Сертификаты")

    title_style = XFStyle()
    borders = Borders()
    borders.bottom = Borders.MEDIUM
    borders.right = Borders.MEDIUM
    borders.left = Borders.MEDIUM
    title_style.borders = borders
    title_style.font = easyfont(f"bold on, height {12*20};")

    font_style = XFStyle()
    font_style.font = easyfont(f"height {12*20};")

    sheet.write(0, 1, "ФИО", title_style)
    sheet.write(0, 2, "№ Договора", title_style)
    sheet.write(0, 3, "ИНН или ПИНФЛ", title_style)
    sheet.write(0, 4, "День", title_style)
    sheet.write(0, 5, "Месяц", title_style)
    sheet.write(0, 6, "Год", title_style)
    sheet.write(0, 7, "Сертификат №", title_style)

    for r, obj in enumerate(queryset):
        obj: Certificate
        n = r+1
        sheet.write(n, 0, str(n), font_style)
        sheet.write(n, 1, str(obj.full_name), font_style)
        sheet.write(n, 2, str(obj.contract_n), font_style)
        sheet.write(n, 3, str(obj.pinfl_or_inn()), font_style)
        sheet.write(n, 4, str(obj.date_received.year), font_style)
        sheet.write(n, 5, str(obj.date_received.month), font_style)
        sheet.write(n, 6, str(obj.date_received.day), font_style)
        sheet.write(n, 7, str(obj.certificate_n), font_style)

    sheet.col(0).width = 1400
    sheet.col(1).width = 14000
    sheet.col(2).width = 4500
    sheet.col(3).width = 5500
    sheet.col(7).width = 5500

    file = BytesIO()
    workbook.save(file)
    return file


