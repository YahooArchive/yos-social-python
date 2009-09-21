#!/usr/bin/python

__author__   = 'Dustin Whittle <dustin@yahoo-inc.com>'
__version__  = '0.1'

import os, sys, unittest

# update sys path to include bundled modules with priority
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../src'))

import oauthlib, simplejson, yahoo.oauth, yahoo.application


CONSUMER_KEY      = 'dj0yJmk9WUxPUkhFUWxISWpvJmQ9WVdrOWFYWmhTVzVDTXpBbWNHbzlNVGt4TmpJNU1EazROdy0tJnM9Y29uc3VtZXJzZWNyZXQmeD01Ng--'
CONSUMER_SECRET   = 'f893cf549be5cb37f83b1414e2ff212df2ea4c18'
APPLICATION_ID    = 'ivaInB30'
CALLBACK_URL      = 'http://imaginingtheweb.com/'
ACCESS_TOKEN      =  yahoo.oauth.AccessToken.from_string('xoauth_yahoo_guid=ECPZF7D765KTAXPDKWS7GE7CUU&oauth_token_secret=49c5d87ec90630bfbd75e05e8aba0b8a2dfbff9e&oauth_expires_in=3600&oauth_session_handle=ACThYEp256HbrfHBPMCoe00lD1fVW_bfPBLX_mCMqqLnruo43Bj.6HU-&oauth_authorization_expires_in=898629027&oauth_token=A%3DnGqKU27OoB6Eahwpjkn1uo7HMYSSl6UXfT_3HgzoRjcf75ozXZe4CW3lzmhp0APtMyU4s3xEdGbNMMCIacBcvQWq_6ekrf2vPuw7Z5rUqphW7Jn4UIZnj63W827xeyxIw0H13D8x3e54LlQqNW.fbDtAOzI.hg37NhoS07V9LKz7Z1.kvGAKgxNOyR4iIBT6TzqpbZsmowlogN5di3YLLCX3YkzfuC.rIKWvcv4aiEtvNZ7Il2N27n4mN.eApGW6fhWECjZ1bSIquoOeL3TAvX66tDqATnDu.MdjVyGeeX336Aa1FSeopKZTM8NVbR02NtTGOG5vb8258LGWpZ5148yuJBND5Q4.ShVOsy8u59y3P5vVk5iACpuGg0OgQp3fCC7KHgbqEM65zS0t._gqh82NG6WrNuBUpmjpHLBbkllFYiY.9LaJj2cCz8or9yLzoY5ch98Sui1SXjpKejfnKQr.ccIqqJW4uZdQXPVGQU0Pk9ZdSkFm98vkeyJ4AGpdj3zSPnVQ04JVAne2hJ41q3M5tRw4XDhc.5.6nwe2e5UbcI4.8FGf0z3tWLskcpgvmfmasTJUZaK0FH_2kjY1SduD.4zTLkObGdORylNsDZBSadepcHeDQfJIZ.KlIPCpfGu2YmSfexnOzwvPp19IqnpmzwwuF897KpSWlZijd4D8F5w3okQAVXdKd219F.jZk1cE6X6wVKKM9vUdavnAaZPBrJHTqngCwXUSE9APJyyPOf3w.0tJRqaozJxEmoEvBiVXx7HoOIB0CXtWVdDvDeM2dahoQrD0scQ-')

class OAuthApplicationTest(unittest.TestCase):

  def setUp(self):
    self.oauthapp = yahoo.application.OAuthApplication(CONSUMER_KEY, CONSUMER_SECRET, APPLICATION_ID, CALLBACK_URL, ACCESS_TOKEN)
    self.oauthapp.token = self.oauthapp.refresh_access_token(self.oauthapp.token)

  def test_get_request_token(self):
    request_token = self.oauthapp.get_request_token()
    self.assertEquals('3600', request_token.expires_in)
    self.assertEquals('https://api.login.yahoo.com/oauth/v2/request_auth?oauth_token=%s' % request_token.key, request_token.request_auth_url)

  def test_refresh_access_token(self):
    self.oauthapp.token = self.oauthapp.refresh_access_token(self.oauthapp.token)
    self.assertEquals('3600', self.oauthapp.token.expires_in)
    self.assertEquals('ECPZF7D765KTAXPDKWS7GE7CUU', self.oauthapp.token.yahoo_guid)

  def test_get_authorization_url(self):
    request_token = self.oauthapp.get_request_token()
    self.assertEquals('https://api.login.yahoo.com/oauth/v2/request_auth?oauth_token=%s' % request_token.key, self.oauthapp.get_authorization_url(request_token, None))

  def test_get_profile(self):
    profile = self.oauthapp.getProfile()
    self.assertEquals('Dustin Whittle', profile['nickname'])
    self.assertEquals('http://profiles.yahoo.com/u/ECPZF7D765KTAXPDKWS7GE7CUU', profile['profileUrl'])

  def test_get_presence(self):
    presence = self.oauthapp.getPresence()
    self.assertEquals('...', presence['value']['status'])
    self.assertEquals('yahoo', presence['src'])

  def test_get_connections(self):
    connections = self.oauthapp.getConnections()['connections']
    self.assertEquals(81, connections['count'])

  def test_get_contacts(self):
    contacts = self.oauthapp.getContacts()['connections']
    self.assertEquals(81, contacts['count'])

  def test_get_updates(self):
    updates = self.oauthapp.getUpdates()['updates']
    self.assertEquals('Dustin Whittle', updates[0]['profile_nickname'])

  def test_insert_update(self):
    update = self.oauthapp.insertUpdate('my test description', 'my test title', 'http://apps.yahoo.com/test')
    self.assertEquals('Operation was successfull', update['error']['detail'])

  def test_get_social_graph(self):
    social_graph = self.oauthapp.getSocialGraph(0, 10)
    self.assertEquals('ChrisHeilmann', social_graph[0]['nickname'])

  def test_get_geo_places(self):
    geocode = self.oauthapp.getGeoPlaces('SOMA, San Francisco, California')
    self.assertEquals('23512042', geocode['place']['woeid'])

  def test_yql(self):
    data = self.oauthapp.yql('select * from social.profile where guid=me')
    self.assertEquals('Dustin Whittle', data['query']['results']['profile']['nickname'])


if __name__ == '__main__':
  unittest.main()
