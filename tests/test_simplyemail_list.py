from Helpers import helpers
from Helpers import Download
from Helpers import Parser
from Helpers import EmailFormat
from Helpers import HtmlBootStrapTheme
from Helpers import Connect6
from Helpers import Parser
from Common import TaskController
from Helpers import VersionCheck
import SimplyEmail

assert helpers.color('test')
assert helpers.color('test', firewall=True)
assert helpers.color('test', warning=True)


# perfrom list funcs
Task = TaskController.Conducter()
Task.load_modules()
Task.ListModules()
V = VersionCheck.VersionCheck("1.3")
V.VersionRequest()

# perfrom Download testing
ua = helpers.getua()
dl = Download.Download(True)
html = dl.requesturl('http://google.com', ua, timeout=2, retrytime=3, statuscode=False)
dl.GoogleCaptchaDetection(html)
f, download = dl.download_file('http://www.sample-videos.com/doc/Sample-doc-file-100kb.doc', '.pdf')
dl.delete_file(f)