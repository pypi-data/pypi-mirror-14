from twisted.internet.ssl import Certificate
from twisted.python.filepath import FilePath
from twisted.trial.unittest import SynchronousTestCase

from fusion_util.cert import chainCerts



class chainCertTests(SynchronousTestCase):
    """
    Tests for L{chainCerts}.
    """
    def test_chainCerts(self):
        """
        L{chainCerts} loads all but the first cert in a file.
        """
        data = FilePath(__file__).sibling('data').child('certs')
        cert1 = data.child('cert1.pem').getContent()
        cert2 = data.child('cert2.pem').getContent()
        cert3 = data.child('cert3.pem').getContent()
        expected = [
            Certificate.loadPEM(cert) for cert in [cert2, cert3]]
        chain = chainCerts(cert1 + '\n' + cert2 + '\n' + cert3)
        self.assertEqual(len(chain), 2)
        self.assertEqual(
            chain[0].digest('sha256'), expected[0].digest('sha256'))
        self.assertEqual(
            chain[1].digest('sha256'), expected[1].digest('sha256'))
