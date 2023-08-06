################################################################
# xmldirector.plonecore
# (C) 2014,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################

import os
import uuid
import tempfile
from zipfile import ZipFile

import plone.api
from Products.Five.browser import BrowserView

from xmldirector.plonecore.browser.restapi import store_zip
from xmldirector.crex.browser.restapi import convert_crex


class CREX(BrowserView):

    @property
    def handle(self):
        try:
            return self.context.get_handle(create_if_not_existing=True)
        except:
            return None

    def new_connector(self):
        connector = plone.api.content.create(type='xmldirector.plonecore.connector', container=self.context, title=u'CREX DOCX to XML conversion')
        connector.setLayout('crex-upload-form')
        connector.connector_subpath = str(uuid.uuid1())
        connector.plone_utils.addPortalMessage(u'Connector created')
        return self.request.response.redirect(connector.absolute_url())

    def have_docx(self):
        handle = self.handle
        if handle:
            return handle.exists('src/index.docx')

    def have_xml(self):
        handle = self.handle
        if handle:
            return handle.exists('result/xml/index.xml')

    def have_html(self):
        handle = self.handle
        if handle:
            return handle.exists('result/html/index.html')

    def have_dita(self):
        handle = self.handle
        if handle:
            return handle.exists('result/dita')

    def upload_docx(self):
        handle = self.handle
        docx = self.request.form['docx'].read()
        if len(docx) == 0:
            raise ValueError('No file uploaded')
        if not handle.exists('src'):
            handle.makedir('src')
        with handle.open('src/index.docx', 'wb') as fp:
            fp.write(docx)

        self.context.plone_utils.addPortalMessage(u'DOCX file uploaded and stored')
        return self.request.response.redirect(self.context.absolute_url())

    def cleanup(self):
        handle = self.handle
        if handle.exists('result'):
            handle.removedir('result', recursive=True, force=True)
        if handle.exists('src'):
            handle.removedir('src', recursive=True, force=True)
        self.context.plone_utils.addPortalMessage(u'Cleanup done')
        return self.request.response.redirect(self.context.absolute_url())

    def convert_dghodoc(self):
        return self.convert_crex(
                'https://www.c-rex.net/api/XBot/Convert//Demo.XmlDirector/XmlDirector',
                'demo@c-rex.net',
                'demo$crex'
                )

    def convert_single_topic(self):
        return self.convert_crex(
            'https://www.c-rex.net/api/XBot/Convert/Demo/docx2DITATopic',
                'demo@c-rex.net',
                'demo$crex'
            )

    def convert_split_topic(self):
        return self.convert_crex(
            'https://www.c-rex.net/api/XBot/Convert/Demo/docx2DITAMap',
                'demo@c-rex.net',
                'demo$crex'
            )

    def convert_crex(self, crex_url, crex_username, crex_password):

        zip_tmp = tempfile.mktemp(suffix='.zip')
        handle = self.handle
        with handle.open('src/index.docx', 'rb') as fp_in:
            with ZipFile(zip_tmp, 'w') as fp_out:
                fp_out.writestr('index.docx', fp_in.read())

        result_zip_fn = convert_crex(zip_tmp, crex_url, crex_username, crex_password)
        store_zip(self.context, result_zip_fn, 'result')

        self.context.plone_utils.addPortalMessage(u'Conversion results stored')
        return self.request.response.redirect(self.context.absolute_url())

    def convert_bookalope(self):
        import pdb; pdb.set_trace() 

        import bookalope


        b_client = bookalope.BookalopeClient(beta_host=True)
        b_client.token = '051d17836932453f8bc962a442a35543'


        book = b_client.create_book()
        bookflow = book.bookflows[0]

        bookflow.title = 'XML Director Bookalope demo'
        bookflow.author = 'xml-director.info (Andreas Jung/ZOPYX)'
        bookflow.save()

        handle = self.handle
        with handle.open('src/index.docx', 'rb') as doc:
            bookflow.set_document('index.docx', doc.read())

        formats = [fext for format_ in b_client.get_export_formats() for fext in format_.file_exts]

        if not handle.exists('result'):
            handle.makedir('result')

        for format_ in formats:
            print("Converting and downloading " + format_ + "...")

            # Get the Style instance for the default styling.
            styles = b_client.get_styles(format_)
            default_style = next(_ for _ in styles if _.short_name == "default")
            converted_bytes = bookflow.convert(format_, default_style, version="test")

            # Save the converted document.
            fname = "result/{}.{}".format(bookflow.id, format_)
            with handle.open(fname, "wb") as doc_conv:
                doc_conv.write(converted_bytes)

        print("Deleting book and all bookflows...")
        book.delete()

        self.context.plone_utils.addPortalMessage(u'EBook formats generated and stored')
        return self.request.response.redirect(self.context.absolute_url())
