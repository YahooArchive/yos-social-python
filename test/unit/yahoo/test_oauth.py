#!/usr/bin/python

__author__   = 'Dustin Whittle <dustin@yahoo-inc.com>'
__version__  = '0.1'

import os, sys, unittest

# update sys path to include bundled modules with priority
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../src'))

import oauthlib, simplejson, yahoo.oauth

# Yahoo! Social API
OAUTH_TEST_API_URL = 'http://json-service.appspot.com/echo'

class RequestTokenTest(unittest.TestCase):

  def setUp(self):
    key              = 'j5nyp6'
    secret           = 'A%3DKO6ZjIGGmw3.Ba7UQ64vLHcGEK5IZoB.32NLJqLDyJzGRBXxWs1YoX_u842QTClj5Do9CbM7tMO5yS_B4fH.zyCbVOpXQoY1NZXQEH.UmWFEmjpKZTX0pv2lEbVtwK2Xwf9FqylF2zlU5f5fIoLaOrfr2eDEVUbwtVJjh465Ry5ig7JAcWu.tb2HxV5Ucw7UrlDAub93hdTU.9w9ggtCMz3zF16cG1NfBROZIVXniyaKxYb0yzGV6E4uq_iwFde65pUyc8SfUXvW5U2Vr4V3dvN3HNb2tquPBcrcthb59VGZ2Yf75oBK2lI.NgcdqPl2t3JbaHwDp4xbnw9dzEHkWGZgiBcPpt2EjnBUznYq7JH.b3uX1rxTWZcJkcsOXATekisHPwGQORUTmkH9G3zhvn0vDnwPO1KucrIa8Kx1yhUt2Vd9bjQWnnX.f8H1C3AFPMsCGsNe9A1jv39AhfIW8JBTOWKqSgvvlcBv24MRlH1PdLbti1mqyEhv7CTYGctUhd1hLtjv4Ox8U7V.ma9QdHJ92F4leeS3eKWDWNL2y1Gt4OLYTqg7IKlUBqHouJE5SC802myr6F.AceLMoL8SvCisvWIFw50bSqKozveV3uAOWgwC51oM5h3GwOttBbZJzsoj7eXqoND5Dy4XUOYoQG.B46lZ3CJAlO8rpkpXlQvMLUh7D1kVKHfdeTw_qwBpKkaulkWk.OYRZ0rua0blkLX.zjRZbiI.s538Z0afVsdh2mc3gDJg9HZ213OjS9On7ffYzkEsCU.jRdED5Ag3y.5omZ0_Y2cOeEw-'
    expires_in       = '3600'
    request_auth_url = 'https://api.login.yahoo.com/oauth/v2/request_auth?oauth_token=j5nyp6'

    self.token = yahoo.oauth.RequestToken(key, secret, expires_in, request_auth_url)

  def test_to_string(self):
    """
    Tests creating a request token string
    """
    self.assertEquals('oauth_token_secret=A%253DKO6ZjIGGmw3.Ba7UQ64vLHcGEK5IZoB.32NLJqLDyJzGRBXxWs1YoX_u842QTClj5Do9CbM7tMO5yS_B4fH.zyCbVOpXQoY1NZXQEH.UmWFEmjpKZTX0pv2lEbVtwK2Xwf9FqylF2zlU5f5fIoLaOrfr2eDEVUbwtVJjh465Ry5ig7JAcWu.tb2HxV5Ucw7UrlDAub93hdTU.9w9ggtCMz3zF16cG1NfBROZIVXniyaKxYb0yzGV6E4uq_iwFde65pUyc8SfUXvW5U2Vr4V3dvN3HNb2tquPBcrcthb59VGZ2Yf75oBK2lI.NgcdqPl2t3JbaHwDp4xbnw9dzEHkWGZgiBcPpt2EjnBUznYq7JH.b3uX1rxTWZcJkcsOXATekisHPwGQORUTmkH9G3zhvn0vDnwPO1KucrIa8Kx1yhUt2Vd9bjQWnnX.f8H1C3AFPMsCGsNe9A1jv39AhfIW8JBTOWKqSgvvlcBv24MRlH1PdLbti1mqyEhv7CTYGctUhd1hLtjv4Ox8U7V.ma9QdHJ92F4leeS3eKWDWNL2y1Gt4OLYTqg7IKlUBqHouJE5SC802myr6F.AceLMoL8SvCisvWIFw50bSqKozveV3uAOWgwC51oM5h3GwOttBbZJzsoj7eXqoND5Dy4XUOYoQG.B46lZ3CJAlO8rpkpXlQvMLUh7D1kVKHfdeTw_qwBpKkaulkWk.OYRZ0rua0blkLX.zjRZbiI.s538Z0afVsdh2mc3gDJg9HZ213OjS9On7ffYzkEsCU.jRdED5Ag3y.5omZ0_Y2cOeEw-&oauth_token=j5nyp6&xoauth_request_auth_url=https%3A%2F%2Fapi.login.yahoo.com%2Foauth%2Fv2%2Frequest_auth%3Foauth_token%3Dj5nyp6&oauth_expires_in=3600', self.token.to_string())

  def test_from_string(self):
    """
    Tests creating a request token from string
    """
    token = yahoo.oauth.RequestToken.from_string('oauth_token_secret=A%253DKO6ZjIGGmw3.Ba7UQ64vLHcGEK5IZoB.32NLJqLDyJzGRBXxWs1YoX_u842QTClj5Do9CbM7tMO5yS_B4fH.zyCbVOpXQoY1NZXQEH.UmWFEmjpKZTX0pv2lEbVtwK2Xwf9FqylF2zlU5f5fIoLaOrfr2eDEVUbwtVJjh465Ry5ig7JAcWu.tb2HxV5Ucw7UrlDAub93hdTU.9w9ggtCMz3zF16cG1NfBROZIVXniyaKxYb0yzGV6E4uq_iwFde65pUyc8SfUXvW5U2Vr4V3dvN3HNb2tquPBcrcthb59VGZ2Yf75oBK2lI.NgcdqPl2t3JbaHwDp4xbnw9dzEHkWGZgiBcPpt2EjnBUznYq7JH.b3uX1rxTWZcJkcsOXATekisHPwGQORUTmkH9G3zhvn0vDnwPO1KucrIa8Kx1yhUt2Vd9bjQWnnX.f8H1C3AFPMsCGsNe9A1jv39AhfIW8JBTOWKqSgvvlcBv24MRlH1PdLbti1mqyEhv7CTYGctUhd1hLtjv4Ox8U7V.ma9QdHJ92F4leeS3eKWDWNL2y1Gt4OLYTqg7IKlUBqHouJE5SC802myr6F.AceLMoL8SvCisvWIFw50bSqKozveV3uAOWgwC51oM5h3GwOttBbZJzsoj7eXqoND5Dy4XUOYoQG.B46lZ3CJAlO8rpkpXlQvMLUh7D1kVKHfdeTw_qwBpKkaulkWk.OYRZ0rua0blkLX.zjRZbiI.s538Z0afVsdh2mc3gDJg9HZ213OjS9On7ffYzkEsCU.jRdED5Ag3y.5omZ0_Y2cOeEw-&oauth_token=j5nyp6&xoauth_request_auth_url=https%3A%2F%2Fapi.login.yahoo.com%2Foauth%2Fv2%2Frequest_auth%3Foauth_token%3Dj5nyp6&oauth_expires_in=3600')
    self.assertEquals(self.token.key, token.key)
    self.assertEquals(self.token.secret, token.secret)
    self.assertEquals(self.token.expires_in, token.expires_in)
    self.assertEquals(self.token.request_auth_url, token.request_auth_url)

  def tearDown(self):
    self.token = None


class AccessTokenTest(unittest.TestCase):

  def setUp(self):
    key                       = 'A%3DKO6ZjIGGmw3.Ba7UQ64vLHcGEK5IZoB.32NLJqLDyJzGRBXxWs1YoX_u842QTClj5Do9CbM7tMO5yS_B4fH.zyCbVOpXQoY1NZXQEH.UmWFEmjpKZTX0pv2lEbVtwK2Xwf9FqylF2zlU5f5fIoLaOrfr2eDEVUbwtVJjh465Ry5ig7JAcWu.tb2HxV5Ucw7UrlDAub93hdTU.9w9ggtCMz3zF16cG1NfBROZIVXniyaKxYb0yzGV6E4uq_iwFde65pUyc8SfUXvW5U2Vr4V3dvN3HNb2tquPBcrcthb59VGZ2Yf75oBK2lI.NgcdqPl2t3JbaHwDp4xbnw9dzEHkWGZgiBcPpt2EjnBUznYq7JH.b3uX1rxTWZcJkcsOXATekisHPwGQORUTmkH9G3zhvn0vDnwPO1KucrIa8Kx1yhUt2Vd9bjQWnnX.f8H1C3AFPMsCGsNe9A1jv39AhfIW8JBTOWKqSgvvlcBv24MRlH1PdLbti1mqyEhv7CTYGctUhd1hLtjv4Ox8U7V.ma9QdHJ92F4leeS3eKWDWNL2y1Gt4OLYTqg7IKlUBqHouJE5SC802myr6F.AceLMoL8SvCisvWIFw50bSqKozveV3uAOWgwC51oM5h3GwOttBbZJzsoj7eXqoND5Dy4XUOYoQG.B46lZ3CJAlO8rpkpXlQvMLUh7D1kVKHfdeTw_qwBpKkaulkWk.OYRZ0rua0blkLX.zjRZbiI.s538Z0afVsdh2mc3gDJg9HZ213OjS9On7ffYzkEsCU.jRdED5Ag3y.5omZ0_Y2cOeEw-'
    secret                    = '048d18e1dfebb968f0d0ee54b7377af1b3997b11'
    expires_in                = '3600'
    authorization_expires_in  = '898640492'
    session_handle            = 'ACThYEp256HbrfHBPMCoe00lD1fVW_bfPBLX_mCMqqLnruo43Bj.6HU-'
    yahoo_guid                = 'ECPZF7D765KTAXPDKWS7GE7CUU'

    self.token = yahoo.oauth.AccessToken(key, secret, expires_in, session_handle, authorization_expires_in, yahoo_guid)

  def test_to_string(self):
    """
    Tests creating a access token string
    """
    self.assertEquals('xoauth_yahoo_guid=ECPZF7D765KTAXPDKWS7GE7CUU&oauth_token_secret=048d18e1dfebb968f0d0ee54b7377af1b3997b11&oauth_expires_in=3600&oauth_session_handle=ACThYEp256HbrfHBPMCoe00lD1fVW_bfPBLX_mCMqqLnruo43Bj.6HU-&oauth_authorization_expires_in=898640492&oauth_token=A%253DKO6ZjIGGmw3.Ba7UQ64vLHcGEK5IZoB.32NLJqLDyJzGRBXxWs1YoX_u842QTClj5Do9CbM7tMO5yS_B4fH.zyCbVOpXQoY1NZXQEH.UmWFEmjpKZTX0pv2lEbVtwK2Xwf9FqylF2zlU5f5fIoLaOrfr2eDEVUbwtVJjh465Ry5ig7JAcWu.tb2HxV5Ucw7UrlDAub93hdTU.9w9ggtCMz3zF16cG1NfBROZIVXniyaKxYb0yzGV6E4uq_iwFde65pUyc8SfUXvW5U2Vr4V3dvN3HNb2tquPBcrcthb59VGZ2Yf75oBK2lI.NgcdqPl2t3JbaHwDp4xbnw9dzEHkWGZgiBcPpt2EjnBUznYq7JH.b3uX1rxTWZcJkcsOXATekisHPwGQORUTmkH9G3zhvn0vDnwPO1KucrIa8Kx1yhUt2Vd9bjQWnnX.f8H1C3AFPMsCGsNe9A1jv39AhfIW8JBTOWKqSgvvlcBv24MRlH1PdLbti1mqyEhv7CTYGctUhd1hLtjv4Ox8U7V.ma9QdHJ92F4leeS3eKWDWNL2y1Gt4OLYTqg7IKlUBqHouJE5SC802myr6F.AceLMoL8SvCisvWIFw50bSqKozveV3uAOWgwC51oM5h3GwOttBbZJzsoj7eXqoND5Dy4XUOYoQG.B46lZ3CJAlO8rpkpXlQvMLUh7D1kVKHfdeTw_qwBpKkaulkWk.OYRZ0rua0blkLX.zjRZbiI.s538Z0afVsdh2mc3gDJg9HZ213OjS9On7ffYzkEsCU.jRdED5Ag3y.5omZ0_Y2cOeEw-', self.token.to_string())

  def test_from_string(self):
    """
    Tests creating a access token from string
    """
    token = yahoo.oauth.AccessToken.from_string('xoauth_yahoo_guid=ECPZF7D765KTAXPDKWS7GE7CUU&oauth_token_secret=048d18e1dfebb968f0d0ee54b7377af1b3997b11&oauth_expires_in=3600&oauth_session_handle=ACThYEp256HbrfHBPMCoe00lD1fVW_bfPBLX_mCMqqLnruo43Bj.6HU-&oauth_authorization_expires_in=898640492&oauth_token=A%253DKO6ZjIGGmw3.Ba7UQ64vLHcGEK5IZoB.32NLJqLDyJzGRBXxWs1YoX_u842QTClj5Do9CbM7tMO5yS_B4fH.zyCbVOpXQoY1NZXQEH.UmWFEmjpKZTX0pv2lEbVtwK2Xwf9FqylF2zlU5f5fIoLaOrfr2eDEVUbwtVJjh465Ry5ig7JAcWu.tb2HxV5Ucw7UrlDAub93hdTU.9w9ggtCMz3zF16cG1NfBROZIVXniyaKxYb0yzGV6E4uq_iwFde65pUyc8SfUXvW5U2Vr4V3dvN3HNb2tquPBcrcthb59VGZ2Yf75oBK2lI.NgcdqPl2t3JbaHwDp4xbnw9dzEHkWGZgiBcPpt2EjnBUznYq7JH.b3uX1rxTWZcJkcsOXATekisHPwGQORUTmkH9G3zhvn0vDnwPO1KucrIa8Kx1yhUt2Vd9bjQWnnX.f8H1C3AFPMsCGsNe9A1jv39AhfIW8JBTOWKqSgvvlcBv24MRlH1PdLbti1mqyEhv7CTYGctUhd1hLtjv4Ox8U7V.ma9QdHJ92F4leeS3eKWDWNL2y1Gt4OLYTqg7IKlUBqHouJE5SC802myr6F.AceLMoL8SvCisvWIFw50bSqKozveV3uAOWgwC51oM5h3GwOttBbZJzsoj7eXqoND5Dy4XUOYoQG.B46lZ3CJAlO8rpkpXlQvMLUh7D1kVKHfdeTw_qwBpKkaulkWk.OYRZ0rua0blkLX.zjRZbiI.s538Z0afVsdh2mc3gDJg9HZ213OjS9On7ffYzkEsCU.jRdED5Ag3y.5omZ0_Y2cOeEw-')
    self.assertEquals(self.token.key, token.key)
    self.assertEquals(self.token.secret, token.secret)
    self.assertEquals(self.token.expires_in, token.expires_in)
    self.assertEquals(self.token.authorization_expires_in, token.authorization_expires_in)
    self.assertEquals(self.token.session_handle, token.session_handle)
    self.assertEquals(self.token.yahoo_guid, token.yahoo_guid)

  def tearDown(self):
    self.token = None


class ClientTest(unittest.TestCase):

  def setUp(self):
    self.client           = yahoo.oauth.Client()
    self.consumer_key     = 'dj0yJmk9WUxPUkhFUWxISWpvJmQ9WVdrOWFYWmhTVzVDTXpBbWNHbzlNVGt4TmpJNU1EazROdy0tJnM9Y29uc3VtZXJzZWNyZXQmeD01Ng--'
    self.consumer_secret  = 'f893cf549be5cb37f83b1414e2ff212df2ea4c18'
    self.application_id   = 'ivaInB30'
    self.callback_url     = 'http://imaginingtheweb.com/'

    self.consumer                   = oauthlib.oauth.OAuthConsumer(self.consumer_key, self.consumer_secret)
    self.signature_method_plaintext = oauthlib.oauth.OAuthSignatureMethod_PLAINTEXT()
    self.signature_method_hmac_sha1 = oauthlib.oauth.OAuthSignatureMethod_HMAC_SHA1()

  def test_client(self):
    self.assertEquals('api.login.yahoo.com', self.client.server)
    self.assertEquals(443, self.client.port)
    self.assertEquals('https://api.login.yahoo.com/oauth/v2/get_request_token', self.client.request_token_url)
    self.assertEquals('https://api.login.yahoo.com/oauth/v2/get_token', self.client.access_token_url)
    self.assertEquals('https://api.login.yahoo.com/oauth/v2/request_auth', self.client.authorization_url)

  def test_fetch_request_token(self):
    request = oauthlib.oauth.OAuthRequest.from_consumer_and_token(self.consumer, http_method='GET', http_url=self.client.request_token_url)
    request.sign_request(self.signature_method_plaintext, self.consumer, None)

    request_token = self.client.fetch_request_token(request)

    self.assertTrue(request_token.key != None)
    self.assertTrue(request_token.secret != None)
    self.assertEquals('3600', request_token.expires_in)
    self.assertEquals('https://api.login.yahoo.com/oauth/v2/request_auth?oauth_token=%s' % request_token.key, request_token.request_auth_url)

  def test_fetch_access_token(self):
    pass

  def test_authorize_token(self):
    pass

  def test_get_authorization_url(self):
    request_token = yahoo.oauth.RequestToken.from_string('oauth_token_secret=A%253DKO6ZjIGGmw3.Ba7UQ64vLHcGEK5IZoB.32NLJqLDyJzGRBXxWs1YoX_u842QTClj5Do9CbM7tMO5yS_B4fH.zyCbVOpXQoY1NZXQEH.UmWFEmjpKZTX0pv2lEbVtwK2Xwf9FqylF2zlU5f5fIoLaOrfr2eDEVUbwtVJjh465Ry5ig7JAcWu.tb2HxV5Ucw7UrlDAub93hdTU.9w9ggtCMz3zF16cG1NfBROZIVXniyaKxYb0yzGV6E4uq_iwFde65pUyc8SfUXvW5U2Vr4V3dvN3HNb2tquPBcrcthb59VGZ2Yf75oBK2lI.NgcdqPl2t3JbaHwDp4xbnw9dzEHkWGZgiBcPpt2EjnBUznYq7JH.b3uX1rxTWZcJkcsOXATekisHPwGQORUTmkH9G3zhvn0vDnwPO1KucrIa8Kx1yhUt2Vd9bjQWnnX.f8H1C3AFPMsCGsNe9A1jv39AhfIW8JBTOWKqSgvvlcBv24MRlH1PdLbti1mqyEhv7CTYGctUhd1hLtjv4Ox8U7V.ma9QdHJ92F4leeS3eKWDWNL2y1Gt4OLYTqg7IKlUBqHouJE5SC802myr6F.AceLMoL8SvCisvWIFw50bSqKozveV3uAOWgwC51oM5h3GwOttBbZJzsoj7eXqoND5Dy4XUOYoQG.B46lZ3CJAlO8rpkpXlQvMLUh7D1kVKHfdeTw_qwBpKkaulkWk.OYRZ0rua0blkLX.zjRZbiI.s538Z0afVsdh2mc3gDJg9HZ213OjS9On7ffYzkEsCU.jRdED5Ag3y.5omZ0_Y2cOeEw-&oauth_token=j5nyp6&xoauth_request_auth_url=https%3A%2F%2Fapi.login.yahoo.com%2Foauth%2Fv2%2Frequest_auth%3Foauth_token%3Dj5nyp6&oauth_expires_in=3600')
    self.assertEquals('https://api.login.yahoo.com/oauth/v2/request_auth?oauth_token=j5nyp6&oauth_callback=http%3A%2F%2Fimaginingtheweb.com%2F', oauthlib.oauth.OAuthRequest.from_token_and_callback(token=request_token, callback=self.callback_url, http_method='GET', http_url=self.client.authorization_url).to_url())

  def test_access_resource(self):
    access_token = yahoo.oauth.AccessToken.from_string('xoauth_yahoo_guid=ECPZF7D765KTAXPDKWS7GE7CUU&oauth_token_secret=048d18e1dfebb968f0d0ee54b7377af1b3997b11&oauth_expires_in=3600&oauth_session_handle=ACThYEp256HbrfHBPMCoe00lD1fVW_bfPBLX_mCMqqLnruo43Bj.6HU-&oauth_authorization_expires_in=898640492&oauth_token=A%253DKO6ZjIGGmw3.Ba7UQ64vLHcGEK5IZoB.32NLJqLDyJzGRBXxWs1YoX_u842QTClj5Do9CbM7tMO5yS_B4fH.zyCbVOpXQoY1NZXQEH.UmWFEmjpKZTX0pv2lEbVtwK2Xwf9FqylF2zlU5f5fIoLaOrfr2eDEVUbwtVJjh465Ry5ig7JAcWu.tb2HxV5Ucw7UrlDAub93hdTU.9w9ggtCMz3zF16cG1NfBROZIVXniyaKxYb0yzGV6E4uq_iwFde65pUyc8SfUXvW5U2Vr4V3dvN3HNb2tquPBcrcthb59VGZ2Yf75oBK2lI.NgcdqPl2t3JbaHwDp4xbnw9dzEHkWGZgiBcPpt2EjnBUznYq7JH.b3uX1rxTWZcJkcsOXATekisHPwGQORUTmkH9G3zhvn0vDnwPO1KucrIa8Kx1yhUt2Vd9bjQWnnX.f8H1C3AFPMsCGsNe9A1jv39AhfIW8JBTOWKqSgvvlcBv24MRlH1PdLbti1mqyEhv7CTYGctUhd1hLtjv4Ox8U7V.ma9QdHJ92F4leeS3eKWDWNL2y1Gt4OLYTqg7IKlUBqHouJE5SC802myr6F.AceLMoL8SvCisvWIFw50bSqKozveV3uAOWgwC51oM5h3GwOttBbZJzsoj7eXqoND5Dy4XUOYoQG.B46lZ3CJAlO8rpkpXlQvMLUh7D1kVKHfdeTw_qwBpKkaulkWk.OYRZ0rua0blkLX.zjRZbiI.s538Z0afVsdh2mc3gDJg9HZ213OjS9On7ffYzkEsCU.jRdED5Ag3y.5omZ0_Y2cOeEw-')
    request = oauthlib.oauth.OAuthRequest.from_consumer_and_token(self.consumer, token=access_token, http_method='GET', http_url=OAUTH_TEST_API_URL, parameters={ 'format': 'json' })
    request.sign_request(self.signature_method_hmac_sha1, self.consumer, access_token)

    response = simplejson.loads(self.client.access_resource(request))

    self.assertEquals('json-service.appspot.com', response['headers']['host'])
    self.assertEquals('dj0yJmk9WUxPUkhFUWxISWpvJmQ9WVdrOWFYWmhTVzVDTXpBbWNHbzlNVGt4TmpJNU1EazROdy0tJnM9Y29uc3VtZXJzZWNyZXQmeD01Ng--', response['query_params']['oauth_consumer_key'])
    self.assertEquals('HMAC-SHA1', response['query_params']['oauth_signature_method'])
    self.assertEquals('json', response['query_params']['format'])

  def tearDown(self):
    self.client = None


if __name__ == '__main__':
  unittest.main()
