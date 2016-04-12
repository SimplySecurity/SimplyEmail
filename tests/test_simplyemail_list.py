from Helpers import helpers
from Helpers import Download
from Helpers import Parser
from Helpers import CanarioAPI
from Helpers import EmailFormat
from Helpers import HtmlBootStrapTheme
from Helpers import Connect6
from Helpers import Parser
from Helpers import LinkedinNames
from Helpers import VersionCheck
from Common import TaskController
import SimplyEmail

assert helpers.color('test')
assert helpers.color('test', firewall=True)
assert helpers.color('test', warning=True)
assert helpers.formatLong(
    "test", "TESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
assert helpers.DirectoryListing('/')


# perfrom list funcs
Task = TaskController.Conducter()
Task.load_modules()
Task.ListModules()
V = VersionCheck.VersionCheck("1.3")
V.VersionRequest()

# perfrom Download testing
ua = helpers.getua()
dl = Download.Download(True)
html = dl.requesturl(
    'http://google.com', ua, timeout=2, retrytime=3, statuscode=False)
dl.GoogleCaptchaDetection(html)
f, download = dl.download_file(
    'http://www.sample-videos.com/doc/Sample-doc-file-100kb.doc', '.pdf')
dl.delete_file(f)


def test_emailformat():
    em = EmailFormat.EmailFormat('verisgroup.com', Verbose=True)
    name = em.BuildName(['alex', 'test'], "{first}.{last}")
    assert name == 'alex.test'
    cleannames = [['alex', 'test'], ['alex', 'man'], ['alex', 'dude'], ['mad', 'max']]
    domain = 'verisgroup.com'
    finalemails = ['mmax@verisgroup.com']
    result = em.EmailDetect(cleannames, domain, finalemails)
    assert result[0] == '{f}{last}'
    finalemails = ['m.max@verisgroup.com'
    result = em.EmailDetect(cleannames, domain, finalemails)
    assert result[0] == '{f}.{last}'
    finalemails = ['madmax@verisgroup.com'
    result = em.EmailDetect(cleannames, domain, finalemails)
    assert result[0] == '{first}{last}'
    finalemails = ['mad.max@verisgroup.com'
    result = em.EmailDetect(cleannames, domain, finalemails)
    assert result[0] == '{first}.{last}'
    finalemails = ['mad.m@verisgroup.com'
    result = em.EmailDetect(cleannames, domain, finalemails)
    assert result[0] == '{first}.{l}'
    finalemails = ['madm@verisgroup.com'
    result = em.EmailDetect(cleannames, domain, finalemails)
    assert result[0] == '{first}{l}'
    finalemails = ['mad_max@verisgroup.com'
    result = em.EmailDetect(cleannames, domain, finalemails)
    assert result[0] == '{first}_{last}'
    finalemails = ['mad@verisgroup.com'
    result = em.EmailDetect(cleannames, domain, finalemails)
    assert result[0] == '{first}'