from .crdt import CRDTDocument


class CRDTManager:

    def __init__(self):

        self.documents = {}


    def get_document(self, document_id):

        if document_id not in self.documents:

            self.documents[document_id] = CRDTDocument()

        return self.documents[document_id]


crdt_manager = CRDTManager()
