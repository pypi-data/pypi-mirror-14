#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# test_borme.py -
# Copyright (C) 2015 Pablo Castellano <pablo@anche.no>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import json
import os
import tempfile
import unittest

import bormeparser
from bormeparser.borme import Borme, BormeActoCargo, BormeActoTexto, BormeAnuncio, BormeXML
from bormeparser.download import download_pdf, download_xml
from bormeparser.exceptions import BormeDoesntExistException
from bormeparser.seccion import SECCION
from bormeparser.provincia import PROVINCIA

try:
    FileNotFoundError
except NameError:
    # Python 2
    FileNotFoundError = IOError

EXAMPLES_PATH = os.path.join(os.path.dirname(bormeparser.__file__), '..', 'examples')

DATA1 = {214: {'Actos': {'Ceses/Dimisiones': {'Adm. Unico': {'JUAN GARCIA GARCIA'}},
                         'Datos registrales': 'T 5188, L 4095, F 146, S 8, H MA120039, I/A 4 (25.05.15).',
                         'Constitución': 'Comienzo de operaciones: 1.04.15. Objeto social: blabla. Domicilio: C/ RANDOM 1 2 (MALAGA). Capital: 3.000,00 Euros.',
                         'Nombramientos': {'Adm. Unico': {'PEDRO GOMEZ GOMEZ'}}},
               'Empresa': 'EMPRESA RANDOM SL.'},
         'borme_cve': 'BORME-A-2015-102-29',
         'borme_fecha': 'Martes 2 de junio de 2015',
         'borme_num': 102,
         'borme_provincia': 'MÁLAGA',
         'borme_seccion': 'SECCIÓN PRIMERA'
         }


class BormeATestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.borme = bormeparser.parse(os.path.join(EXAMPLES_PATH, 'BORME-A-2015-27-10.pdf'), SECCION.A)

    def test_instance(self):
        self.assertEqual(self.borme.date, datetime.date(year=2015, month=2, day=10))
        self.assertEqual(self.borme.seccion, SECCION.A)
        self.assertEqual(self.borme.provincia, PROVINCIA.CACERES)
        self.assertEqual(self.borme.num, 27)
        self.assertEqual(self.borme.cve, 'BORME-A-2015-27-10')
        self.assertEqual(self.borme.url, 'https://boe.es/borme/dias/2015/02/10/pdfs/BORME-A-2015-27-10.pdf')
        self.assertEqual(self.borme.filename, os.path.join(EXAMPLES_PATH, 'BORME-A-2015-27-10.pdf'))

    def test_json(self):
        fp = tempfile.NamedTemporaryFile()
        filename = fp.name
        fp.close()
        converted = self.borme.to_json(filename)
        self.assertTrue(converted)

        fp = open(filename)
        data = json.load(fp)
        fp.close()

        self.assertEqual(data['cve'], 'BORME-A-2015-27-10')
        self.assertEqual(data['date'], '2015-02-10')
        self.assertEqual(data['seccion'], 'A')
        self.assertEqual(data['provincia'], u'Cáceres')  # "C\u00e1ceres"
        self.assertEqual(data['num'], 27)
        self.assertEqual(data['url'], 'https://boe.es/borme/dias/2015/02/10/pdfs/BORME-A-2015-27-10.pdf')
        self.assertEqual(data['from_anuncio'], 57315)
        self.assertEqual(data['to_anuncio'], 57344)
        self.assertEqual(data['num_anuncios'], 30)

        b = Borme.from_json(filename)
        self.assertEqual(b.date, datetime.date(year=2015, month=2, day=10))
        self.assertEqual(b.seccion, SECCION.A)
        self.assertEqual(b.provincia, PROVINCIA.CACERES)
        self.assertEqual(b.num, 27)
        self.assertEqual(b.cve, 'BORME-A-2015-27-10')
        self.assertEqual(b.url, 'https://boe.es/borme/dias/2015/02/10/pdfs/BORME-A-2015-27-10.pdf')
        self.assertEqual(b.filename, filename)

        os.unlink(filename)


class FakeBormeTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        bormeanuncios = [BormeAnuncio(1, DATA1[214]['Empresa'], DATA1[214]['Actos'])]
        cls.borme = Borme((2015, 2, 10), 'A', PROVINCIA.CACERES, 27, 'BORME-A-2015-27-10', bormeanuncios)

    def test_instance(self):
        self.assertEqual(self.borme.date, datetime.date(year=2015, month=2, day=10))
        self.assertEqual(self.borme.seccion, SECCION.A)
        self.assertEqual(self.borme.provincia, PROVINCIA.CACERES)
        self.assertEqual(self.borme.num, 27)
        self.assertEqual(self.borme.cve, 'BORME-A-2015-27-10')
        self.assertEqual(self.borme.url, 'https://boe.es/borme/dias/2015/02/10/pdfs/BORME-A-2015-27-10.pdf')
        self.assertEqual(self.borme.filename, None)

    def test_to_json(self):
        fp = tempfile.NamedTemporaryFile()
        filename = fp.name
        fp.close()
        converted = self.borme.to_json(filename)
        self.assertTrue(converted)

        fp = open(filename)
        data = json.load(fp)
        fp.close()

        self.assertEqual(data['cve'], 'BORME-A-2015-27-10')
        self.assertEqual(data['date'], '2015-02-10')
        self.assertEqual(data['seccion'], 'A')
        self.assertEqual(data['provincia'], u'Cáceres')  # "C\u00e1ceres"
        self.assertEqual(data['num'], 27)
        self.assertEqual(data['url'], 'https://boe.es/borme/dias/2015/02/10/pdfs/BORME-A-2015-27-10.pdf')
        self.assertEqual(data['from_anuncio'], 1)
        self.assertEqual(data['to_anuncio'], 1)
        self.assertEqual(data['num_anuncios'], 1)


class BormeAnuncioTestCase(unittest.TestCase):
    def setUp(self):
        self.anuncio = BormeAnuncio(1, DATA1[214]['Empresa'], DATA1[214]['Actos'])

    def test_instance(self):
        self.assertEqual(self.anuncio.id, 1)
        self.assertEqual(self.anuncio.empresa, DATA1[214]['Empresa'])
        self.assertEqual(self.anuncio.datos_registrales, DATA1[214]['Actos']['Datos registrales'])

    def test_get_actos(self):
        actos = list(self.anuncio.get_actos())
        actos.sort()  # Sort dictionary
        self.assertEqual(len(actos), 3)
        self.assertEqual(actos[0], ('Ceses/Dimisiones', DATA1[214]['Actos']['Ceses/Dimisiones']))
        self.assertEqual(actos[1], ('Constitución', DATA1[214]['Actos']['Constitución']))
        self.assertEqual(actos[2], ('Nombramientos', DATA1[214]['Actos']['Nombramientos']))

    def test_get_borme_actos(self):
        actos = self.anuncio.get_borme_actos()
        actos.sort()  # Sort dictionary
        self.assertEqual(len(actos), 3)
        self.assertIsInstance(actos[0], BormeActoCargo)
        self.assertEqual(actos[0].name, 'Ceses/Dimisiones')
        self.assertEqual(actos[0].cargos, DATA1[214]['Actos']['Ceses/Dimisiones'])
        self.assertIsInstance(actos[1], BormeActoTexto)
        self.assertEqual(actos[1].name, 'Constitución')
        self.assertEqual(actos[1].value, DATA1[214]['Actos']['Constitución'])
        self.assertIsInstance(actos[2], BormeActoCargo)
        self.assertEqual(actos[2].name, 'Nombramientos')
        self.assertEqual(actos[2].cargos, DATA1[214]['Actos']['Nombramientos'])


class BormeActoTestCase(unittest.TestCase):
    def test_cargo_instance(self):
        acto = BormeActoCargo('Nombramientos', DATA1[214]['Actos']['Nombramientos'])
        self.assertEqual(len(acto.cargos), 1)
        self.assertEqual(acto.cargos['Adm. Unico'], DATA1[214]['Actos']['Nombramientos']['Adm. Unico'])

        # Exceptions
        self.assertRaises(ValueError, BormeActoCargo, 'Acto invalido', 'mal')
        self.assertRaises(ValueError, BormeActoCargo, 'Constitución', 'mal')
        self.assertRaises(ValueError, BormeActoCargo, 'Nombramientos', 'mal')

    def test_texto_instance(self):
        acto = BormeActoTexto('Constitución', DATA1[214]['Actos']['Constitución'])
        self.assertEqual(acto.value, DATA1[214]['Actos']['Constitución'])

        # Exceptions
        self.assertRaises(ValueError, BormeActoTexto, 'Acto invalido', ['mal'])
        self.assertRaises(ValueError, BormeActoTexto, 'Nombramientos', ['mal'])


class BormeXMLTestCase(unittest.TestCase):
    date = (2015, 9, 24)
    url = 'https://www.boe.es/diario_borme/xml.php?id=BORME-S-20150924'
    url_insecure = 'http://www.boe.es/diario_borme/xml.php?id=BORME-S-20150924'
    nbo = 183

    def test_from_file(self):
        path = os.path.join(tempfile.gettempdir(), 'BORME-S-20150924.xml')
        downloaded = download_xml(self.date, path)
        self.assertTrue(downloaded)
        self.assertEqual(os.path.getsize(path), 20534)

        # from local file
        bxml = BormeXML.from_file(path)
        self.assertEqual(bxml.url, self.url)
        self.assertEqual(bxml.date, datetime.date(year=self.date[0], month=self.date[1], day=self.date[2]))
        self.assertEqual(bxml.filename, path)
        self.assertEqual(bxml.nbo, self.nbo)
        self.assertEqual(bxml.prev_borme, datetime.date(year=self.date[0], month=self.date[1], day=self.date[2] - 1))
        self.assertEqual(bxml.next_borme, datetime.date(year=self.date[0], month=self.date[1], day=self.date[2] + 1))
        os.unlink(path)

        # from remote file (https)
        bxml = BormeXML.from_file(self.url)
        self.assertEqual(bxml.url, self.url)
        self.assertEqual(bxml.date, datetime.date(year=self.date[0], month=self.date[1], day=self.date[2]))
        self.assertEqual(bxml.filename, None)
        self.assertEqual(bxml.nbo, self.nbo)
        self.assertEqual(bxml.prev_borme, datetime.date(year=self.date[0], month=self.date[1], day=self.date[2] - 1))
        self.assertEqual(bxml.next_borme, datetime.date(year=self.date[0], month=self.date[1], day=self.date[2] + 1))

        # from remote file (insecure https)
        bxml = BormeXML.from_file(self.url, secure=False)
        self.assertEqual(bxml.url, self.url_insecure)
        self.assertEqual(bxml.date, datetime.date(year=self.date[0], month=self.date[1], day=self.date[2]))
        self.assertEqual(bxml.filename, None)
        self.assertEqual(bxml.nbo, self.nbo)
        self.assertEqual(bxml.prev_borme, datetime.date(year=self.date[0], month=self.date[1], day=self.date[2] - 1))
        self.assertEqual(bxml.next_borme, datetime.date(year=self.date[0], month=self.date[1], day=self.date[2] + 1))

        # Exceptions
        self.assertRaises(FileNotFoundError, BormeXML.from_file, 'invalidfile.xml')

    def test_from_date(self):
        bxml = BormeXML.from_date(self.date)
        self.assertEqual(bxml.url, self.url)
        self.assertEqual(bxml.date, datetime.date(year=self.date[0], month=self.date[1], day=self.date[2]))
        self.assertEqual(bxml.filename, None)
        self.assertEqual(bxml.nbo, self.nbo)
        self.assertEqual(bxml.prev_borme, datetime.date(year=self.date[0], month=self.date[1], day=self.date[2] - 1))
        self.assertEqual(bxml.next_borme, datetime.date(year=self.date[0], month=self.date[1], day=self.date[2] + 1))

        date = datetime.date(*self.date)
        bxml = BormeXML.from_date(date)
        self.assertEqual(bxml.url, self.url)
        self.assertEqual(bxml.date, datetime.date(year=self.date[0], month=self.date[1], day=self.date[2]))
        self.assertEqual(bxml.filename, None)
        self.assertEqual(bxml.nbo, self.nbo)
        self.assertEqual(bxml.prev_borme, datetime.date(year=self.date[0], month=self.date[1], day=self.date[2] - 1))
        self.assertEqual(bxml.next_borme, datetime.date(year=self.date[0], month=self.date[1], day=self.date[2] + 1))

        # Exceptions
        self.assertRaises(BormeDoesntExistException, BormeXML.from_date, (2015, 9, 26))

        l = ['BORME-A-2015-183-%s' % x
             for x in ['01', '03', '04', '06', '07', '08', '09', '10', '11', '12', '14', '15', '16', '22', '25', '26',
             '28', '29', '30', '31', '32', '33', '34', '35', '36', '38', '39', '40', '41', '43', '46', '47', '49', '50', '51']
             ]
        self.assertEqual(bxml.get_cves(SECCION.A), l)

        # TODO: get_sizes


class BormeCTestCase1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.borme = bormeparser.parse(os.path.join(EXAMPLES_PATH, 'BORME-C-2011-20488.xml'), SECCION.C)

    def test_instance(self):
        self.assertEqual(self.borme['cifs'], {'A31017494', 'A31067218', 'A58348038', 'B31136005'})
        self.assertEqual(self.borme['cve'], 'BORME-C-2011-20488')
        self.assertEqual(self.borme['departamento'], 'CONVOCATORIAS DE JUNTAS')
        self.assertEqual(self.borme['empresa'], 'DESARROLLOS ESPECIALES DE SISTEMAS DE ANCLAJE, S.A.')
        self.assertEqual(self.borme['fecha'], datetime.date(year=2011, month=5, day=27))
        self.assertEqual(self.borme['seccion'], SECCION.C)
        self.assertEqual(self.borme['diario_numero'], 101)
        self.assertEqual(self.borme['filename'], os.path.join(EXAMPLES_PATH, 'BORME-C-2011-20488.xml'))
        self.assertEqual(self.borme['id_anuncio'], 'A110044738')
        self.assertEqual(self.borme['numero_anuncio'], 44738)
        self.assertEqual(self.borme['pagina_inicial'], 22110)
        self.assertEqual(self.borme['pagina_final'], 22116)
        self.assertEqual(self.borme['seccion'], SECCION.C)


class BormeCTestCase2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.borme = bormeparser.parse(os.path.join(EXAMPLES_PATH, 'BORME-C-2011-20488.html'), SECCION.C)

    def test_instance(self):
        self.assertEqual(self.borme['cifs'], {'A31017494', 'A31067218', 'A58348038', 'B31136005'})
        self.assertEqual(self.borme['cve'], 'BORME-C-2011-20488')
        self.assertEqual(self.borme['departamento'], 'CONVOCATORIAS DE JUNTAS')
        self.assertEqual(self.borme['diario_numero'], 101)
        self.assertEqual(self.borme['empresa'], 'DESARROLLOS ESPECIALES DE SISTEMAS DE ANCLAJE, S.A.')
        self.assertEqual(self.borme['fecha'], datetime.date(year=2011, month=5, day=27))
        self.assertEqual(self.borme['filename'], os.path.join(EXAMPLES_PATH, 'BORME-C-2011-20488.html'))
        self.assertEqual(self.borme['seccion'], SECCION.C)


if __name__ == '__main__':
    unittest.main()
