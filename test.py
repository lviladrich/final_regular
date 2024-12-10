


import unittest
from unittest.mock import patch


# Importar la función a testear (ajusta el import a tu estructura de archivos)
from main import solicitar_dni


class TestSolicitarDni(unittest.TestCase):

    @patch("builtins.input", side_effect=["45622304"])
    def test_dni_valido(self, mock_input):
        """Test para DNI válido"""
        dni = solicitar_dni()
        self.assertEqual(
            dni, 45622304
        )  # Se espera que la función retorne el DNI correcto

    @patch("builtins.input", side_effect=["abc", "123", "45622304"])
    def test_dni_no_valido_reintento(self, mock_input):
        """Test para DNI no válidos que requieren reintento"""
        dni = solicitar_dni()
        self.assertEqual(
            dni, 45622304
        )  # Se espera que la función finalmente acepte 45622304


if __name__ == "_main_":
    unittest.main()