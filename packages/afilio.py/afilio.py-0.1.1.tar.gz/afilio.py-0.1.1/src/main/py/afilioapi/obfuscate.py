import math
import random
import sys
import uuid


class Obfuscator():
    def obf_float(self, f):
        f = 1. if float(f) == 0. else f
        return random.random()*f

    def obf_int(self, n):
        return random.randint(n+1, sys.maxsize)

    def obf_status(self, status):
        return "accepted" if status == "refused" else "accepted"

    def obf(self, sale):
        sale_obj = sale[key]
        key = "%d" % self.obf_int(list(sale.keys())[0])

        s = self.obf_status
        i = self.obf_int
        f = self.obf_float
        d = lambda d: d
        st = lambda s: uuid.uuid4().hex

        return {key: key,
                {"saleid": key,
                "status": s(sale_obj["status"]),
                "progid": i(sale_obj["progid"]),
                "order_id": i(sale_obj["order_id"]),
                "order_price": f(sale_obj["order_price"]),
                "comission": f(sale_obj["comission"]),
                "date": d(sale_obj["date"]),
                "payment": sale_obj["payment"],
                "xtra": "NULL",
                "aff_xtra": uuid.uuid4().hex}
        }


class ObfuscateCLI():
    def run(self, input_data):
        pass


if __name__ == "__main__":
    import sys
    ObfuscateCLI().run(sys.argv[1:])


import unittest


class ObfuscateTestCase(unittest.TestCase):
    def test_obf_float(self):
        self.assertNotEqual(0, Obfuscator().obf_float(0))
        self.assertNotEqual(0., Obfuscator().obf_float(0.))
        self.assertNotEqual(0.1, Obfuscator().obf_float(0.1))
        self.assertNotEqual(1., Obfuscator().obf_float(1.))
        self.assertNotEqual(1000., Obfuscator().obf_float(1000.))

    def test_obf_int(self):
        self.assertNotEqual(0, Obfuscator().obf_int(0))
        self.assertNotEqual(1, Obfuscator().obf_int(1))
        self.assertNotEqual(1000, Obfuscator().obf_int(1000))

    def test_obfuscate_sale(self):
        sale = {"sale":
                {"12401863":
                    {"saleid":"12401863",
                     "status":"refused",
                      "progid":"1719",
                      "order_id":"336662676",
                      "order_price":"108.2300",
                      "comission":"3.7900",
                      "date":"2016-01-11 21:14:01",
                      "payment":"Unpaid",
                      "xtra":"NULL",
                      "aff_xtra":"1791e9da288c424289a4d6464adb6ffb"}
                    }
                }

        obfd = Obfuscator().obf(sale)
        #self.assertCountNotEqual(sale["sale"].keys(), obfd.keys())

