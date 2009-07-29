from openid.extension import Extension
from oauthlib import oauth

__all__ = [
    'OauthAuthorizeTokenRequest',
    'OauthAuthorizeTokenResponse',
    'ns_uri',
    ]

ns_uri = 'http://specs.openid.net/extensions/oauth/1.0'

class OauthAuthorizeTokenRequest(Extension):
    
    ns_alias = 'oauth'
    
    def __init__(self, consumer, scope):
        Extension.__init__(self)
        self.consumer = consumer
        self.scope = scope
        
    def getExtensionArgs(self):
        args = {}
        
        args['consumer'] = self.consumer
        #args['scope'] = self.scope
        
        return args

OauthAuthorizeTokenRequest.ns_uri = ns_uri

class OauthAuthorizeTokenResponse(Extension):

    ns_alias = 'oauth'
    
    def __init__(self):
        Extension.__init__(self)
        self.authorized_request_token = None
        
    def fromSuccessResponse(cls, success_response):
        self = cls()

        #args = success_response.getSignedNS(self.ns_uri)
        
        args = success_response.extensionResponse(self.ns_uri, False)
        
        if (len(args) > 0):
            #Note that we're passing an empty string for the secret part since the oauth token secret
            #should be an empty string per section 10 of the extension spec
            self.authorized_request_token = oauth.OAuthToken(args['request_token'], '')
            
        return self

    fromSuccessResponse = classmethod(fromSuccessResponse)

OauthAuthorizeTokenResponse.ns_uri = ns_uri
