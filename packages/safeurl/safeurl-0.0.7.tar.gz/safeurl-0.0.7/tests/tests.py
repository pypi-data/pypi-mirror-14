from unittest import TestCase
from safeurl.core import getRealURL


class MainTestCase(TestCase):
    def test_decodeUrl(self):
        self.assertEqual(getRealURL('http://bit.ly/1gaiW96'),
                         'https://www.yandex.ru/')

    def test_decodeUrlArray(self):
        self.assertEqual(
            getRealURL(['http://bit.ly/1gaiW96', 'http://bit.ly/1gaiW96']),
            ['https://www.yandex.ru/', 'https://www.yandex.ru/'])

    def test_errorDecodeUrl(self):
        self.assertEqual(getRealURL('http://bit.ly.wrong/wrong'),
                         'Failed')

    def test_errorDecodeUrlArray(self):
        self.assertEqual(
            getRealURL(
                ['http://bit.ly.wrong/wrong', 'http://bit.ly.wrong/wrong']),
            ['Failed', 'Failed'])

    def test_errorWithOkDecodeUrlArray(self):
        self.assertEqual(
            getRealURL(['http://bit.ly.wrong/wrong', 'http://bit.ly/1gaiW96',
                        'http://bit.ly.wrong/wrong']),
            ['Failed', 'https://www.yandex.ru/', 'Failed'])
