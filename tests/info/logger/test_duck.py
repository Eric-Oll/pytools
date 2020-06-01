import unittest

from pytools.info.logger.duck import Duck

class TestDuck(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = Duck(level=Duck.DEBUG)

    def test_format_message(self):
        message_list = [
            '1ère ligne',
            '2ème ligne',
            '3ème ligne'
        ]

        # Avec les valeur par défaut
        self.assertEqual(self.logger.format_message(Duck.DEBUG, message_list)\
                         [len(self.logger.format_header(Duck.DEBUG).replace('%MESSAGE%', '')):],
                         "1ère ligne\n\t- 2ème ligne\n\t- 3ème ligne"
                         )

        # Avec un puce spécifique
        self.assertEqual(self.logger.format_message(Duck.DEBUG, message_list, bulletpoint='==>')\
                         [len(self.logger.format_header(Duck.DEBUG).replace('%MESSAGE%', '')):],
                         "1ère ligne\n==>2ème ligne\n==>3ème ligne"
                         )

        # Avec des sauts de ligne à la fin
        self.assertEqual(self.logger.format_message(Duck.DEBUG, message_list, lines_after=2)\
                         [len(self.logger.format_header(Duck.DEBUG).replace('%MESSAGE%', '')):],
                         "1ère ligne\n\t- 2ème ligne\n\t- 3ème ligne\n\n"
                         )

        # Avec des sauts de ligne au début
        result = self.logger.format_message(Duck.DEBUG, message_list, lines_before=2)
        self.assertEqual(result[:2], "\n\n")
        self.assertEqual(result[len(self.logger.format_header(Duck.DEBUG).replace('%MESSAGE%', ''))+2:],
                         "1ère ligne\n\t- 2ème ligne\n\t- 3ème ligne"
                         )


        # Avec puce spécificaue et saut de ligne à la fin
        self.assertEqual(self.logger.format_message(Duck.DEBUG, message_list,
                                                    bulletpoint='\t==>', lines_after=3)\
                         [len(self.logger.format_header(Duck.DEBUG).replace('%MESSAGE%', '')):],
                         "1ère ligne\n\t==>2ème ligne\n\t==>3ème ligne\n\n\n"
                         )

if __name__ == '__main__':
    unittest.main()
