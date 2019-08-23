import webbrowser
from .catalog import MetadataCatalog     

class GeoNetworkCatalog(MetadataCatalog):

    def api_url(self):
        return self.service_url + "/srv/api/0.1"

    def xml_services_url(self):
        return self.service_url + "/srv/eng"

    def metadata_exists(self, uuid):
        try:
            self.get_metadata(uuid)
            return True
        except:
            return False

    def get_metadata(self, uuid):
        url = self.api_url() + "/records/" + uuid
        return self.http_request(url)

    def publish_metadata(self, metadata):
        headers = {"accept": "application/json"}
        self.nam.setTokenInHeader()
        url = self.xml_services_url() + "/mef.import=?_csrf=" + self.nam.token
        with open(metadata,'rb') as f:
            files = {'mefFile': (metadata, f, 'application/zip', {'Expires': '0'})}        
            r = self.nam.session.post(url, files=files, headers = headers)
        print (r.text)
        r.raise_for_status()
        '''
        if "errors" in r and r['errors']:
            raise Exception(r['errors'])       
        '''

    def delete_metadata(self, uuid):
        #TODO: bucket??
        url = self.api_url() + "/records?uuids=%s" % uuid
        self.http_request(url, method="delete")

    def me(self):
        url = self.api_url() + "/me"
        ret =  self.http_request(url, headers = {"Accept": "application/json"})
        return ret

    def metadata_url(self, uuid):
        return self.service_url + "/srv/spa/catalog.search#/metadata/" + uuid

    def open_metadata(self, uuid):        
        webbrowser.open_new_tab(self.metadata_url(uuid))

    def set_layer_url(self, uuid, url):
        pass









