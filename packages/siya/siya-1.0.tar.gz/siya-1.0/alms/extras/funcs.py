# -*- coding: utf-8 -*-
import Image, ImageDraw, ImageFont

from head.models import Book

from django.utils.encoding import smart_str

BUFF = 87
PADDING = 15
TWIDTH = 325
END_XPOS =  340
MAIN_WIDTH = 300
CALL_NO_CORD = (15,15)

FONT_PATH = ""
FONT_NAME = "LiberationMono-Regular.ttf"
FONT_SIZE = 11

CURSOR = (15,15)


def font():
    return ImageFont.truetype(FONT_PATH+FONT_NAME,FONT_SIZE)

FONT=font()

IMG = Image.open("base.png")
DRAW = ImageDraw.Draw(IMG)

def next_line(line, diff=15):
    if line.__class__ == int:
        return line + diff
    elif line.__class__ == tuple or line.__class__ == list:
        return (line[0],line[1]+diff)
    else:
        return None

def trans_line(line,diff=12):
    return next_line(line,diff)




def write(text,cord,draw=DRAW,font=FONT,overlap=TWIDTH):
    global CURSOR
    size = draw.textsize(text)[0]
    width = overlap - cord[0] - 11
    if size > width:
        text_piece = ""
        line = ""
        size = (0,0)
        for _ in text:
            if size[0] > width - 22 and _ not in [' ','\t',':',';',',','.','']:
                text_piece += "-\n"
                line = ""
            text_piece += _
            line += _
            size = draw.textsize(line)
        CURSOR = (cord[0] + draw.textsize(text_piece)[0],cord[1]+draw.textsize(text_piece)[1])
        draw.text(cord,smart_str(text_piece),font=font,fill="#000000")
    else:
        draw.text(cord,smart_str(text),font=font,fill="#000000")
        CURSOR = (cord[0] + draw.textsize(text)[0], cord[1]+draw.textsize(text)[1])


def writelines(text_list, cord,draw=DRAW,overlap=TWIDTH):
    '''
    direction = vertical(v) or horizontal(h)
    '''
    for text in text_list:
        write(text=smart_str(text),cord=cord,overlap=overlap,draw=draw)
        cord = next_line(cord)


def makeCard(accNo):
    book = Book.objects.get(accession_number=accNo)
    
    '''
    write call number
    '''
    call_number_list = book.get_call_number().split(" ")
    writelines(call_number_list,CALL_NO_CORD,overlap=BUFF)

    '''
    write the authors's name, title, other authors' names, place of
    publication,publisher's name and year of publication.
    '''
    main_text = []
    authors_list = book.author.all()
    if len(authors_list) == 0:
        ## no authors
        mauthor , other_authors = None, None
    elif len(authors_list) == 1:
        mauthor = authors_list[0].get_catalog_name()
        other_authors = []
    elif len(authors_list) > 1:
        mauthor = authors_list[0].get_catalog_name()
        other_authors = authors_list[1:]

    if mauthor == None or  mauthor == "None": ## authors are not specified
        titpub_text = book.get_title() + ";"
    else:
        main_text.append(mauthor)
        titpub_text = "  "+book.get_title() + ";"
        if other_authors is not None:
            titpub_text += "%".join(other_authors)
    titpub_text += book.get_catalog_publishers()
    
    main_text.append(titpub_text)
    
    
    writelines(text_list=main_text, cord=(BUFF, PADDING),overlap=END_XPOS)


    '''
    Page No.                Edition
    ISBN                    Series
    Volume                  Price
    '''

    edition = smart_str(book.edition)
    series = smart_str(book.series)
    price = smart_str(book.price)

    if edition == None or edition == "None":
        edition = ""

    if series == None or series == "None":
        series = ""

    if price == None or price == "None":
        price = ""

    len_edition = DRAW.textsize('Edition: '+edition)[0]
    len_series = DRAW.textsize('Series: '+series)[0]
    len_price = DRAW.textsize('Price: '+price)[0]
    dict_edition = {
            'len': len_edition,
            'val': edition,
            'name': 'edition'
            }
    dict_series = {
            'len': len_series,
            'val': series,
            'name': 'series'
            }
    dict_price = {
            'len': len_price,
            'val': price,
            'name': 'price'
            }

    dict_list = (dict_price,dict_edition,dict_series)

    largest_one = max(dict_list,key=lambda a:a['len'])

    writelines(text_list=[_['name'].title()+": "+_['val'] for _ in dict_list if _['val'] != ""],cord=(END_XPOS-largest_one['len'],CURSOR[1]),overlap=END_XPOS)

    IMG.save("image__1.png", "PNG")
