from django.test import SimpleTestCase

from .stats import EntradaInvalida, calcular, parsear


class StatsTests(SimpleTestCase):
    def test_parsear_separadores_mixtos(self):
        self.assertEqual(parsear("1, 2 3;4\n5.5"), [1, 2, 3, 4, 5.5])

    def test_parsear_invalido(self):
        with self.assertRaises(EntradaInvalida):
            parsear("1, a, 3")
        with self.assertRaises(EntradaInvalida):
            parsear("   ")

    def test_calculos(self):
        r = calcular([2, 4, 4, 4, 5, 5, 7, 9])
        self.assertEqual(r["promedio"], 5)
        self.assertEqual(r["mediana"], 4.5)
        self.assertEqual(r["moda"], [4])
        self.assertEqual(r["desvio_poblacional"], 2)

    def test_un_solo_valor(self):
        r = calcular([7])
        self.assertEqual(r["promedio"], 7)
        self.assertIsNone(r["desvio_muestral"])

    def test_sin_moda(self):
        self.assertIsNone(calcular([1, 2, 3])["moda"])


class ViewTests(SimpleTestCase):
    def test_index_get(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_index_post(self):
        r = self.client.post("/", {"numeros": "10 20 30"})
        self.assertContains(r, "Promedio")
        self.assertContains(r, ">20<")

    def test_index_error(self):
        self.assertContains(self.client.post("/", {"numeros": "x"}), "Valor no válido")

    def test_api(self):
        r = self.client.post("/api/calcular/", {"numeros": [1, 2, 3]}, content_type="application/json")
        self.assertEqual(r.json()["promedio"], 2)
        r = self.client.post("/api/calcular/", {"numeros": "a"}, content_type="application/json")
        self.assertEqual(r.status_code, 400)
        self.assertEqual(self.client.get("/api/calcular/").status_code, 405)
