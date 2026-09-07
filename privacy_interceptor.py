from PySide6.QtWebEngineCore import QWebEngineUrlRequestInterceptor

class CarlinhoPrivacyInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, blocklist):
        super().__init__()
        self.blocklist = blocklist 

    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        resource_type = info.resourceType()
        first_party_url = info.firstPartyUrl().host()
        request_host = info.requestUrl().host()

        if first_party_url and request_host != first_party_url:
            if any(tracker in request_host for tracker in self.blocklist['trackers']):
                info.block(True)
                return
            
        if any(ad_domain in url for ad_domain in self.blocklist['ads']):
            info.block(True)
            return
