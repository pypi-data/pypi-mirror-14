'''
Created on 6 déc. 2014

@author: inso
'''

import unittest
from ucoinpy.documents.certification import SelfCertification, Certification

selfcert_inlines = ["HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:\
h/H8tDIEbfA4yxMQcvfOXVDQhi1sUa9qYtPKrM59Bulv97ouwbAvAsEkC1Uyit1IOpeAV+CQQs4IaAyjE8F1Cw==:\
1416335620:cgeek\n", "RdrHvL179Rw62UuyBrqy2M1crx7RPajaViBatS59EGS:\
Ah55O8cvdkGS4at6AGOKUjy+wrFwAq8iKRJ5xLIb6Xdi3M8WfGOUdMjwZA6GlSkdtlMgEhQPm+r2PMebxKrCBg==:\
1416428323:vit\n" ]

cert_inlines = [
"8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:\
0:TgmDuMxZdyutroj9jiLJA8tQp/389JIzDKuxW5+h7GIfjDu1ZbwI7HNm5rlUDhR2KreaV/QJjEaItT4Cf75rCQ==\n",
"9fx25FmeBDJcikZLWxK5HuzKNbY6MaWYXoK1ajteE42Y:8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:0:\
qn/XNJjaGIwfnR+wGrDME6YviCQbG+ywsQWnETlAsL6q7o3k1UhpR5ZTVY9dvejLKuC+1mUEXVTmH+8Ib55DBA==\n"
]

class Test_SelfCertification(unittest.TestCase):
    '''
    classdocs
    '''

    def test_selfcertification(self):
        version = 1
        currency = "zeta_brousouf"
        selfcert = SelfCertification.from_inline(version, currency, selfcert_inlines[0])
        self.assertEqual(selfcert.pubkey, "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk")
        self.assertEqual(selfcert.signatures[0], "h/H8tDIEbfA4yxMQcvfOXVDQhi1sUa9qYtPKrM59Bulv97ouwbAvAsEkC1Uyit1IOpeAV+CQQs4IaAyjE8F1Cw==")
        self.assertEqual(selfcert.timestamp, 1416335620)
        self.assertEqual(selfcert.uid, "cgeek")

        selfcert = SelfCertification.from_inline(version, currency, selfcert_inlines[1])
        self.assertEqual(selfcert.pubkey, "RdrHvL179Rw62UuyBrqy2M1crx7RPajaViBatS59EGS")
        self.assertEqual(selfcert.signatures[0], "Ah55O8cvdkGS4at6AGOKUjy+wrFwAq8iKRJ5xLIb6Xdi3M8WfGOUdMjwZA6GlSkdtlMgEhQPm+r2PMebxKrCBg==")
        self.assertEqual(selfcert.timestamp, 1416428323)
        self.assertEqual(selfcert.uid, "vit")

    def test_certifications(self):
        version = 1
        currency = "zeta_brousouf"
        blockhash = "DA39A3EE5E6B4B0D3255BFEF95601890AFD80709"
        cert = Certification.from_inline(version, currency, blockhash, cert_inlines[0])
        self.assertEqual(cert.pubkey_from, "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU")
        self.assertEqual(cert.pubkey_to, "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk")
        self.assertEqual(cert.blockid.number, 0)
        self.assertEqual(cert.blockid.sha_hash, blockhash)
        self.assertEqual(cert.signatures[0], "TgmDuMxZdyutroj9jiLJA8tQp/389JIzDKuxW5+h7GIfjDu1ZbwI7HNm5rlUDhR2KreaV/QJjEaItT4Cf75rCQ==")

        cert = Certification.from_inline(version, currency, blockhash, cert_inlines[1])
        self.assertEqual(cert.pubkey_from, "9fx25FmeBDJcikZLWxK5HuzKNbY6MaWYXoK1ajteE42Y")
        self.assertEqual(cert.pubkey_to, "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU")
        self.assertEqual(cert.blockid.number, 0)
        self.assertEqual(cert.blockid.sha_hash, blockhash)
        self.assertEqual(cert.signatures[0], "qn/XNJjaGIwfnR+wGrDME6YviCQbG+ywsQWnETlAsL6q7o3k1UhpR5ZTVY9dvejLKuC+1mUEXVTmH+8Ib55DBA==")
