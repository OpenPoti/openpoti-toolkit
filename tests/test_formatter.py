import json
from pathlib import Path

import pytest

from openpecha.formatters import TsadraFormatter
from openpecha.formatters import HFMLFormatter
from openpecha.formatters import GoogleOCRFormatter



class TestHFMLFormatter:

    def test_get_base_text(self):
        m_text = Path('tests/data/formatter/hfml/kangyur_01.txt').read_text()
        formatter = HFMLFormatter()

        text = formatter.text_preprocess(m_text)
        formatter.build_layers(text, len([text]))
        result = formatter.get_base_text()

        expected = Path('tests/data/formatter/hfml/kangyur_base.txt').read_text()

        assert result == expected


    def test_build_layers(self):
        m_text1 = Path('tests/data/formatter/hfml/kangyur_01.txt').read_text()
        m_text2 = Path('tests/data/formatter/hfml/kangyur_02.txt').read_text()
        formatter = HFMLFormatter()

        text1 = formatter.text_preprocess(m_text1)
        text2 = formatter.text_preprocess(m_text2)
        texts = [text1, text2, text2]
        for text in texts:
            result = formatter.build_layers(text, len(texts))

        result = formatter.get_result()
        
        expected_result = {
            'page': [[(0, 24, 'kk', '1a'), (27, 676, 'kl', '1b'), (679, 2173, 'lm', '2a')], [(0, 266, 'kk', '1a')], [(0, 266, 'kk', '1a')]],
            'topic': [[(27, 2173, 'v0'),(0, 26, 'v1')],[(26, 266, 'v1'), (0, 26, 'v2')], [(26, 266, 'v2')]],
            'sub_topic': [[(27, 1351, 'v0'), (1352, 1494, 'v0'), (1495, 2173, 'v0'), (0, 25, 'v1')], [(26, 266, 'v1'),(0,25, 'v2')],[(26, 266, 'v2')]],
            'error': [[(1838, 1843, 'མཆིའོ་')]],
            'absolute_error': [[(2040, 2042), (2044, 2045)]],
            'note':[[1518, 1624, 1938]]
        }

        for layer in result:
            assert result[layer] == expected_result[layer]


class TestGoogleOCRFormatter:

    @pytest.fixture(scope='class')
    def get_resources(self):
        data_path = Path('tests/data/formatter/google_ocr/W0001/v001')
        responses = [json.load(fn.open()) for fn in sorted(list((data_path/'resources').iterdir()))]
        formatter = GoogleOCRFormatter()
        return formatter, data_path, responses

    
    def test_get_base_text(self, get_resources):
        formatter, data_path, responses = get_resources
        formatter.build_layers(responses)
        
        result = formatter.get_base_text()

        expected = (data_path/'v001.txt').read_text()
        assert result == expected

    
    def test_build_layers(self, get_resources):
        formatter, data_path, responses = get_resources

        result = formatter.build_layers(responses)

        expected = {
            'page': [(0, 19), (24, 888), (893, 1607), (1612, 1809)],
        }

        for result_page, expected_page in zip(result['page'], expected['page']):
            assert result_page[:2] == expected_page