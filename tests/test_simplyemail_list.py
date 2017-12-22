from Helpers import helpers
from Helpers import Download
from Helpers import Parser
from Helpers import CanarioAPI
from Helpers import EmailFormat
from Helpers import HtmlBootStrapTheme
from Helpers import Connect6
from Helpers import Converter
from Helpers import VerifyEmails
from Helpers import LinkedinNames
from Helpers import VersionCheck
from Common import TaskController
from Modules import SearchPGP
from Modules import AskSearch
from Modules import YahooSearch
from Modules import WhoisAPISearch
from Modules import RedditPostSearch
from Modules import FlickrSearch
import os
import SimplyEmail

assert helpers.color('test')
assert helpers.color('test', firewall=True)
assert helpers.color('test', warning=True)
assert helpers.formatLong(
    "test", "TESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
assert helpers.DirectoryListing('/')


# perfrom list funcs

def test_taskcontrollers():
    Task = TaskController.Conducter()
    Task.load_modules()
    # check inits
    for x in Task.modules:
        l = Task.modules[x]
        mod = l.ClassName('test.com', verbose=True)
    Task.ListModules()
    Task.title()
    Task.title_screen()
    #V = VersionCheck.VersionCheck("1.3")
    #V.VersionRequest()
    # test the cleaning function of the TC
    # create fake email items
    Task.ConsumerList = ['alex@test.com', 'alex@test.com', 'alex2@gmail.com', 'alex2@test.com']
    Task.HtmlList = ['alex@test.com', 'alex@test.com', 'alex2@gmail.com', 'alex2@test.com']
    finallist, htmllist = Task.CleanResults('test.com')
    # now make sure we have correct data
    i = finallist.count("alex@test.com")
    b = htmllist.count("alex@test.com")
    assert 'alex@test.com' in finallist
    assert 'alex2@test.com' in finallist
    assert 'alex2@gmail.com' not in finallist
    assert i < 2
    assert 'alex@test.com' in htmllist
    assert 'alex2@test.com' in htmllist
    assert 'alex2@gmail.com' not in htmllist
    assert b < 2

def test_searchpgp():
    s = SearchPGP.ClassName('verisgroup.com', verbose=True)
    FinalOutput, HtmlResults, JsonResults = s.execute()
    assert 'jmacovei@verisgroup.com' in FinalOutput

def test_asksearch():
    s = AskSearch.ClassName('gmail.com', verbose=True)
    FinalOutput, HtmlResults, JsonResults = s.execute()
    assert len(FinalOutput) > 0

def test_yahoosearch():
    s = YahooSearch.ClassName('gmail.com', verbose=True)
    FinalOutput, HtmlResults, JsonResults = s.execute()
    assert len(FinalOutput) > 0

def test_whoisapi():
    s = WhoisAPISearch.ClassName('verisgroup.com', verbose=True)
    FinalOutput, HtmlResults, JsonResults = s.execute()
    assert 'abuse@web.com' in FinalOutput

def test_redditsearch():
    s = RedditPostSearch.ClassName('gmail.com', verbose=True)
    FinalOutput, HtmlResults, JsonResults = s.execute()
    #assert '@gmail.com' in FinalOutput 
    #Look into this issue

def test_flickrsearch():
    s = FlickrSearch.ClassName('microsoft.com', verbose=True)
    FinalOutput, HtmlResults, JsonResults = s.execute()

def test_downloads():
    # perfrom Download testing
    ua = helpers.getua()
    dl = Download.Download(True)
    html = dl.requesturl(
        'http://google.com', ua, timeout=2, retrytime=3, statuscode=False)
    dl.GoogleCaptchaDetection(html)
    f, download = dl.download_file(
        'http://www.sample-videos.com/doc/Sample-doc-file-100kb.doc', '.pdf')
    dl.delete_file(f)

def test_canario():
    c = CanarioAPI.canary('thisshouldnotworkapikey')

def test_verifyemails():
    em1 = ['test@gmail.com']
    em2 = ['alex@gmail.com']
    v = VerifyEmails.VerifyEmail(em1, em2, 'gmail.com')
    v.GetMX()
    assert 'gmail' in v.mxhost['Host']
    b = v.VerifySMTPServer()

'''
def test_linkedin():
    # test Linkedin Name gen
    l = LinkedinNames.LinkedinScraper('verisgroup.com')
    names = l.LinkedInNames()
    assert ['Beth', 'Rodriguez'] in names
    CleanNames = []
    for x in names:
        name = l.LinkedInClean(x)
        if name:
            CleanNames.append(name)
    assert ['Beth', 'Rodriguez'] in names
'''

def test_converter():
    # test the convert for all formats
    p = os.path.dirname(os.path.realpath('.')) + '/SimplyEmail/tests/'
    c = Converter.Converter(verbose=True)
    print p
    text = c.convert_docx_to_txt(p + 'Test-DOCX.docx')
    assert text
    assert 'How to Design and Test' in text
    text = c.convert_doc_to_txt(p + 'Test-DOC.doc')
    assert text
    assert 'How to Design and Test' in text
    text = c.convert_pdf_to_txt(p + 'Test-PDF.pdf')
    assert text
    assert 'How to Design and Test' in text
    text = c.convert_zip_to_text(p + 'Test-PPTX.pptx')
    assert text
    assert 'Test SLIDE' in text
    assert 'Test SLIDE 2' in text
    assert 'Test SLIDE 3' in text

def test_htmlbootstrap():
    em = ['{\'Email\': "alex@test.com", \'Source\': "gmail"}', '{\'Email\': "alex2@test.com", \'Source\': "Canary Paste Bin"}', '{\'Email\': "alex3@test.com", \'Source\': "testing"}']
    h = HtmlBootStrapTheme.HtmlBuilder(em, "test.com")
    h.BuildHtml()
    assert '<td>alex@test.com</td>' in h.HTML
    assert '<td>alex2@test.com</td>' in h.HTML
    assert '<td>alex3@test.com</td>' in h.HTML
    assert '<td>gmail</td>' in h.HTML
    assert '<td>Canary Paste Bin</td>' in h.HTML
    assert '<td>testing</td>' in h.HTML
    assert 'Canary (PasteBin) search detected Email(s)' in h.HTML
    p = os.path.dirname(os.path.realpath('.')) 
    h.OutPutHTML(p)


def test_paser():
    # test parser functions with test data
    raw = """
    alex //
    test //...dfdfsf
    data !@#$%^%&^&*()
    <em>alex@verisgroup.com</em>
    <em> alex@verisgroup.com </em>
    <tr>alex@verisgroup.com</tr>
    <></><><><><><>
    """
    p = Parser.Parser(raw)
    p.RemoveUnicode()
    finaloutput, htmlresults = p.extendedclean('test')


def test_emailformat():
    em = EmailFormat.EmailFormat('verisgroup.com', Verbose=True)
    name = em.BuildName(['alex', 'test'], "{first}.{last}")
    assert name == 'alex.test'
    cleannames = [['alex', 'test'], ['alex', 'man'],
                  ['alex', 'dude'], ['mad', 'max']]
    domain = 'verisgroup.com'
    finalemails = ['mmax@verisgroup.com']
    result = em.EmailDetect(cleannames, domain, finalemails)
    assert result[0] == '{f}{last}'
    finalemails = ['m.max@verisgroup.com']
    result = em.EmailDetect(cleannames, domain, finalemails)
    assert result[0] == '{f}.{last}'
    finalemails = ['madmax@verisgroup.com']
    result = em.EmailDetect(cleannames, domain, finalemails)
    assert result[0] == '{first}{last}'
    finalemails = ['mad.max@verisgroup.com']
    result = em.EmailDetect(cleannames, domain, finalemails)
    assert result[0] == '{first}.{last}'
    finalemails = ['mad.m@verisgroup.com']
    result = em.EmailDetect(cleannames, domain, finalemails)
    assert result[0] == '{first}.{l}'
    finalemails = ['madm@verisgroup.com']
    result = em.EmailDetect(cleannames, domain, finalemails)
    assert result[0] == '{first}{l}'
    finalemails = ['mad_max@verisgroup.com']
    result = em.EmailDetect(cleannames, domain, finalemails)
    assert result[0] == '{first}_{last}'
    finalemails = ['mad@verisgroup.com']
    result = em.EmailDetect(cleannames, domain, finalemails)
    assert result[0] == '{first}'
    # now test building emails
    fm = '{f}{last}'
    emails = em.EmailBuilder(cleannames, domain, fm)
    assert 'mmax@verisgroup.com' in emails
    fm = '{f}.{last}'
    emails = em.EmailBuilder(cleannames, domain, fm)
    assert 'm.max@verisgroup.com' in emails
    fm = '{first}{last}'
    emails = em.EmailBuilder(cleannames, domain, fm)
    assert 'madmax@verisgroup.com' in emails
    fm = '{first}.{last}'
    emails = em.EmailBuilder(cleannames, domain, fm)
    assert 'mad.max@verisgroup.com' in emails
    fm = '{first}.{l}'
    emails = em.EmailBuilder(cleannames, domain, fm)
    assert 'mad.m@verisgroup.com' in emails
    fm = '{first}{l}'
    emails = em.EmailBuilder(cleannames, domain, fm)
    assert 'madm@verisgroup.com' in emails
    fm = '{first}_{last}'
    emails = em.EmailBuilder(cleannames, domain, fm)
    print emails
    assert 'mad_max@verisgroup.com' in emails
    fm = '{first}'
    emails = em.EmailBuilder(cleannames, domain, fm)
    assert 'mad@verisgroup.com' in emails
