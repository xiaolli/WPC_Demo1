from watson_developer_cloud import DocumentConversionV1


class WatsonDocumentConversion:

    def document_convert(self,document_url):
        with open(document_url,'r') as document:
            config = {'conversion_target': DocumentConversionV1.NORMALIZED_TEXT}
            response = DocumentConversionV1.convert_document(document=document,
                                                             config=config,
                                                             media_type='text/html')

        return response