from typing import List

import xlrd
from pprint import pprint
from datetime import date

NUMBER_OF_CERTIFICATE_COLS = 8
NUMBER_OF_CERTIFICATE_FIELDS = 5


class ParsedCertificate:
    contract_n = None
    certificate_n = None
    inn = None
    full_name = None
    date_received = None

    @property
    def has_contract_n(self):
        return self.contract_n is not None

    @property
    def has_certificate_n(self):
        return self.certificate_n is not None

    @property
    def has_inn(self):
        return self.inn is not None

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
        self.certificate_n = str(certificate_n)
        if self.certificate_n == "":
            self.certificate_n = None

    def set_inn(self, inn):
        try:
            self.inn = int(inn)
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
        if self.contract_n is not None:
            count += 1
        if self.certificate_n is not None:
            count += 1
        if self.inn is not None:
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
        if certificate.has_inn:
            wrong_fields = "<u>Имя</u>, " if not certificate.has_full_name else ""
            wrong_fields += "<u>Дата получения</u>, " if not certificate.has_date_received else ""
            wrong_fields += "<u>Номер договора</u>, " if not certificate.has_contract_n else ""
            wrong_fields += "<u>Номер сертификата</u>, " if not certificate.has_certificate_n else ""

            wrong_fields = wrong_fields[:-2]

            cert_string = f"""<p style="margin-bottom: 6px"><b>{certificate.full_name if certificate.has_full_name else certificate.inn}</b> - <i>Ошибки в полях:</i> {wrong_fields}</p>"""
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
                new_certificate.set_inn(row[3].value)
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
