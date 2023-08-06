################################################################
# xmldirector.bookalope
# (C) 2016,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################

from zope.component import getUtility
from plone.registry.interfaces import IRegistry

import bookalope
from xmldirector.bookalope.interfaces import IBookalopeSettings


def convert_bookalope(context, source, formats=[], title=u'', author=u'', prefix=None):
    """ Convert ``source`` using bookalope.net """

    registry = getUtility(IRegistry)
    settings = registry.forInterface(IBookalopeSettings)

    b_client = bookalope.BookalopeClient(beta_host=settings.bookalope_beta)
    b_client.token = settings.bookalope_api_key

    book = b_client.create_book()
    bookflow = book.bookflows[0]

    bookflow.title = title
    bookflow.author = author
    bookflow.save()

    handle = context.get_handle()
    with handle.open(source, 'rb') as doc:
        bookflow.set_document('index.docx', doc.read())

    if not handle.exists('result'):
        handle.makedir('result')

    for format in formats:
        # Get the Style instance for the default styling.
        styles = b_client.get_styles(format)
        default_style = next(_ for _ in styles if _.short_name == "default")
        converted_bytes = bookflow.convert(format, default_style, version="test")

        fname = "result/{}.{}".format(prefix or bookflow.id, format)
        with handle.open(fname, "wb") as doc_conv:
            doc_conv.write(converted_bytes)

    book.delete()
