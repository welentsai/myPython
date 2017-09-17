#!/usr/bin/python
# -*- coding: utf-8 -*-
from . import fitz
import math, sys
'''
The following is a collection of commodity functions to simplify the use of PyMupdf.
'''
#==============================================================================
# A function for searching string occurrences on a page.
#==============================================================================
#def searchFor(page, text, hit_max = 16):
def searchFor(page, text, hit_max = 16):
    '''Search for a string on a page. Parameters:\ntext: string to be searched for\nhit_max: maximum hits.\nReturns a list of rectangles, each of which surrounds a found occurrence.'''
    fitz.CheckParent(page)
    rect = page.rect
    dl = fitz.DisplayList(rect)         # create DisplayList
    page.run(fitz.Device(dl), fitz.Identity) # run page through it
    ts = fitz.TextSheet()                    # create TextSheet
    tp = fitz.TextPage(rect)            # create TextPage
    dl.run(fitz.Device(ts, tp), fitz.Identity, rect)   # run the page
    # return list of hitting reactangles
    return tp.search(text, hit_max = hit_max)

#==============================================================================
# A function for searching string occurrences on a page.
#==============================================================================
def searchPageFor(doc, pno, text, hit_max=16):
    """Search for a string on a page. Parameters:\npno: integer page number\ntext: string to be searched for\nhit_max: maximum hits.\nReturns a list of rectangles, each of which surrounds a found occurrence."""
    return searchFor(doc[pno], text, hit_max = hit_max)
    
#==============================================================================
# A function for extracting a page's text.
#==============================================================================
#def getText(page, output = "text"):
def getText(page, output = "text"):
    '''Extract a PDF page's text. Parameters:\noutput option: text, html, json or xml.\nReturns strings like the TextPage extraction methods extractText, extractHTML, extractJSON, or etractXML respectively. Default and misspelling choice is "text".'''
    fitz.CheckParent(page)

    # return requested text format
    if output.lower() == "json":
        return page._readPageText(output = 2)
    elif output.lower() == "html":
        return page._readPageText(output = 1)
    elif output.lower() == "xml":
        return page._readPageText(output = 3)
    return page._readPageText(output = 0)

#==============================================================================
# A function for extracting a page's text.
#==============================================================================
#def getPageText(pno, output = "text"):
def getPageText(doc, pno, output = "text"):
    '''Extract a PDF page's text by page number. Parameters:\npno: page number\noutput option: text, html, json or xml.\nReturns strings like the TextPage extraction methods extractText, extractHTML, extractJSON, or etractXML respectively. Default and misspelling choice is "text".'''
    return doc[pno].getText(output = output)

#==============================================================================
# A function for rendering a page's image.
# Requires a page object.
#==============================================================================

def getPixmap(page, matrix = fitz.Identity, colorspace = "rgb", clip = None,
              alpha = True):
    '''Create pixmap of page.\nmatrix: fitz.Matrix for transformation (default: fitz.Identity).\ncolorspace: text string / fitz.Colorspace (rgb, rgb, gray - case ignored), default fitz.csRGB.\nclip: a fitz.IRect to restrict rendering to this area.'''
    fitz.CheckParent(page)

    # determine required colorspace
    cs = colorspace
    if type(colorspace) is str:
        if colorspace.upper() == "GRAY":
            cs = fitz.csGRAY
        elif colorspace.upper() == "CMYK":
            cs = fitz.csCMYK
        else:
            cs = fitz.csRGB
    assert cs.n in (1,3,4), "unsupported colorspace"    

    r = page.rect                            # get page boundaries
    dl = fitz.DisplayList(r)                 # create DisplayList
    page.run(fitz.Device(dl), fitz.Identity) # run page through it

    if clip:
        r.intersect(clip.getRect())          # only the part within clip
        r.transform(matrix)                  # transform it
        clip = r.irect                       # make IRect copy of it
        ir = clip
    else:                                    # take full page
        r.transform(matrix)                  # transform it
        ir = r.irect                         # make IRect copy of it

    pix = fitz.Pixmap(cs, ir, alpha)         # create an empty pixmap
    pix.clearWith(255)                       # clear it with color "white"
    dv = fitz.Device(pix, clip)              # create a "draw" device
    dl.run(dv, matrix, r)                    # render the page
    dv = None
    dl = None
    pix.x = 0
    pix.y = 0
    return pix

#==============================================================================
# A function for rendering a page by its number
#==============================================================================
# getPagePixmap(doc, pno, matrix = fitz.Identity, colorspace = "RGB", clip = None, alpha = False):
def getPagePixmap(doc, pno, matrix = fitz.Identity, colorspace = "rgb",
                  clip = None, alpha = True):
    '''Create pixmap of page number.\nmatrix: fitz.Matrix for transformation (default: fitz.Identity).\ncolorspace: text string / fitz.Colorspace (rgb, rgb, gray - case ignored), default fitz.csRGB.\nclip: a fitz.IRect to restrict rendering to this area.'''
    return doc[pno].getPixmap(matrix = matrix, colorspace = colorspace,
                          clip = clip, alpha = alpha)

#==============================================================================
# An internal function to create a link info dictionary for getToC and getLinks
#==============================================================================
def getLinkDict(ln):
    nl = {"kind": ln.dest.kind, "xref": 0, "id": id(ln)}
    try:
        nl["from"] = ln.rect
    except:
        pass
    pnt = fitz.Point(0, 0)
    if ln.dest.flags & fitz.LINK_FLAG_L_VALID:
        pnt.x = ln.dest.lt.x
    if ln.dest.flags & fitz.LINK_FLAG_T_VALID:
        pnt.y = ln.dest.lt.y

    if ln.dest.kind == fitz.LINK_URI:
        nl["uri"] = ln.dest.uri

    elif ln.dest.kind == fitz.LINK_GOTO:
        nl["page"] = ln.dest.page
        nl["to"] = pnt
        if ln.dest.flags & fitz.LINK_FLAG_R_IS_ZOOM:
            nl["zoom"] = ln.dest.rb.x
        else:
            nl["zoom"] = 0.0

    elif ln.dest.kind == fitz.LINK_GOTOR:
        nl["file"] = ln.dest.fileSpec.replace("\\", "/")
        nl["page"] = ln.dest.page
        if ln.dest.page < 0:
            nl["to"] = ln.dest.dest
        else:
            nl["to"] = pnt
            if ln.dest.flags & fitz.LINK_FLAG_R_IS_ZOOM:
                nl["zoom"] = ln.dest.rb.x
            else:
                nl["zoom"] = 0.0

    elif ln.dest.kind == fitz.LINK_LAUNCH:
        nl["file"] = ln.dest.fileSpec.replace("\\", "/")

    elif ln.dest.kind == fitz.LINK_NAMED:
        nl["name"] = ln.dest.named

    else:
        nl["page"] = ln.dest.page

    return nl

#==============================================================================
# A function to collect all links of a PDF page.
# Required is a page object previously created by the
# loadPage() method of a document.
#==============================================================================
def getLinks(page):
    '''Create a list of all links contained in a PDF page as dictionaries - see PyMuPDF ducmentation for details.'''

    fitz.CheckParent(page)
    ln = page.firstLink
    links = []
    while ln:
        nl = getLinkDict(ln)
        links.append(nl)
        ln = ln.next
    if len(links) > 0:
        linkxrefs = page._getLinkXrefs()
        if len(linkxrefs) == len(links):
            for i in range(len(linkxrefs)):
                links[i]["xref"] = linkxrefs[i]
    return links

#==============================================================================
# A function to collect all bookmarks of a PDF document in the form of a table
# of contents.
#==============================================================================
def getToC(doc, simple = True):
    '''Create a table of contents.\nsimple: a bool to control output. Returns a list, where each entry consists of outline level, title, page number and link destination (if simple = False). For details see PyMuPDF's documentation.'''

    def recurse(olItem, liste, lvl):
        '''Recursively follow the outline item chain and record item information in a list.'''
        while olItem:
            if olItem.title:
                title = olItem.title
            else:
                title = " "

            if not olItem.isExternal:
                if olItem.uri:
                    page = olItem.page + 1
                else:
                    page = -1
            else:
                page = -1

            if not simple:
                link = getLinkDict(olItem)
                liste.append([lvl, title, page, link])
            else:
                liste.append([lvl, title, page])

            if olItem.down:
                liste = recurse(olItem.down, liste, lvl+1)
            olItem = olItem.next
        return liste

    # check if document is open and not encrypted
    if doc.isClosed:
        raise RuntimeError("illegal operation on closed document")

    olItem = doc.outline

    if not olItem: return []
    lvl = 1
    liste = []
    return recurse(olItem, liste, lvl)

def getRectArea(*args):
    """Calculate area of rectangle.\nparameter is one of 'px' (default), 'in', 'cm', or 'mm'."""
    rect = args[0]
    if len(args) > 1:
        unit = args[1]
    else:
        unit = "px"    
    if rect.isInfinite or rect.isEmpty:
        return 0.0
    u = {"px": (1,1), "in": (1.,72.), "cm": (2.54, 72.), "mm": (25.4, 72.)}
    f = (u[unit][0] / u[unit][1])**2
    return f * rect.width * rect.height

#def writeImage(filename, output = "png"):
def writeImage(*arg, **kw):
    '''Save pixmap to file.\nfilename: image filename\noutput: requested output format (png, pam, pnm or tga).'''
    pix = arg[0]
    filename = arg[1]
    if "output" in kw:
        output = kw["output"]
    else:
        output = "png"

    c_output = 0
    if output == "png":
        c_output = 1
        if not filename.lower().endswith(".png"):
            raise ValueError("require .png extension")
        if pix.colorspace.n > 3:
            raise ValueError(pix.colorspace.name + " not supported for png")
    elif output == "tga":
        c_output = 4
        if not filename.lower().endswith(".tga"):
            raise ValueError("require .tga extension")
        if pix.colorspace.n > 3:
            raise ValueError(pix.colorspace.name + " not supported for tga")
    elif output == "pam":
        c_output = 3
        if not filename.lower().endswith(".pam"):
            raise ValueError("require .pam extension")
    elif output == "pnm":
        c_output = 2
        if pix.colorspace.n > 3:
            raise ValueError(pix.colorspace.name + " not supported for pnm")
        if pix.n <= 2:
            if not filename.lower().endswith((".pnm", ".pgm")):
                raise ValueError("colorspace requires pnm or pgm extensions")
        elif not filename.lower().endswith((".pnm", "ppm")):
            raise ValueError("colorspace requires pnm or ppm extensions")
    else:
        raise ValueError("invalid output parameter")

    rc = pix._writeIMG(filename, c_output)

    return rc

#==============================================================================
# arithmetic methods for fitz.Matrix
#==============================================================================
def mat_mult(m1, m2):     # __mul__
    if type(m2) in (int, float):
        return fitz.Matrix(m1.a * m2, m1.b * m2, m1.c * m2,
                           m1.d * m2, m1.e * m2, m1.f * m2)
    m = fitz.Matrix()
    try:
        m.concat(m1, m2)
    except:
        raise NotImplementedError("op2 must be 'Matrix' or number")
    return m

def mat_invert(me):       # __invert__
    m = fitz.Matrix()
    m.invert(me)
    return m

def mat_add(m1, m2):      # __add__
    if type(m2) in (int, float):
        return fitz.Matrix(m1.a + m2, m1.b + m2, m1.c + m2,
                           m1.d + m2, m1.e + m2, m1.f + m2)
    try:
        return fitz.Matrix(m1.a + m2.a, m1.b + m2.b, m1.c + m2.c,
                           m1.d + m2.d, m1.e + m2.e, m1.f + m2.f)
    except:
        raise NotImplementedError("op2 must be 'Matrix' or number")

def mat_sub(m1, m2):      # __sub__
    if type(m2) in (int, float):
        return fitz.Matrix(m1.a - m2, m1.b - m2, m1.c - m2,
                           m1.d - m2, m1.e - m2, m1.f - m2)
    try:
        return fitz.Matrix(m1.a - m2.a, m1.b - m2.b, m1.c - m2.c,
                           m1.d - m2.d, m1.e - m2.e, m1.f - m2.f)
    except:
        raise NotImplementedError("op2 must be 'Matrix' or number")

def mat_abs(m):           # __abs__
    a = m.a**2 + m.b**2 + m.c**2 + m.d**2 + m.e**2 + m.f**2
    return math.sqrt(a)

def mat_true(m):          # __nonzero__
    return (abs(m.a) + abs(m.b) + abs(m.c) + abs(m.d) + abs(m.e) + abs(m.f)) > 0

def mat_equ(m, m2):       # __equ__
    return len(m) == len(m2) and mat_true(m - m2) == 0

def mat_contains(m, x):
    if type(x) not in (int, float):
        return False
    else:
        return x in tuple(m)

#==============================================================================
# arithmetic methods for fitz.Rect
#==============================================================================
def rect_or(r1, r2):         # __or__: include point, rect or irect
    if type(r2) not in (fitz.Rect, fitz.IRect, fitz.Point):
        raise NotImplementedError("op2 must be 'Rect', 'IRect' or 'Point'")
    if type(r1) is fitz.Rect:
        r = fitz.Rect(r1)
    else:
        r = r1.rect
    if type(r2) is fitz.Rect:
        r.includeRect(r2)
    elif type(r2) is fitz.IRect:
        r.includeRect(r2.rect)
    else:
        r.includePoint(r2)
    if type(r1) is fitz.Rect:
        return r
    else:
        return r.irect

def rect_and(r1, r2):        # __and__: intersection with rect or irect
    if type(r2) not in (fitz.Rect, fitz.IRect):
        raise NotImplementedError("op2 must be 'Rect' or 'IRect'")
    if type(r1) is fitz.Rect:
        r = fitz.Rect(r1)
    else:
        r = r1.rect
    if type(r2) is fitz.Rect:
        r.intersect(r2)
    else:
        r.intersect(r2.rect)
    if type(r1) is fitz.Rect:
        return r
    else:
        return r.irect

def rect_add(r1, r2):        # __add__: add number, rect or irect to rect
    if type(r1) is fitz.Rect:
        r = fitz.Rect(r1)
    else:
        r = r1.rect
    if type(r2) in (fitz.Rect, fitz.IRect):
        a = r2
    elif type(r2) in (int, float):
        a = fitz.Rect(r2, r2, r2, r2)
    else:
        raise NotImplementedError("op2 must be 'Rect', 'Irect' or number")
    r.x0 += a.x0
    r.y0 += a.y0
    r.x1 += a.x1
    r.y1 += a.y1
    if type(r1) is fitz.Rect:
        return r
    else:
        return r.irect

def rect_sub(r1, r2):        # __sub__: subtract number, rect or irect from rect
    if type(r1) is fitz.Rect:
        r = fitz.Rect(r1)
    else:
        r = r1.rect

    if type(r2) in (fitz.Rect, fitz.IRect):
        a = r2
    elif type(r2) in (int, float):
        a = fitz.Rect(r2, r2, r2, r2)
    else:
        raise NotImplementedError("op2 must be 'Rect', 'Irect' or number")
    r.x0 -= a.x0
    r.y0 -= a.y0
    r.x1 -= a.x1
    r.y1 -= a.y1
    if type(r1) is fitz.Rect:
        return r
    else:
        return r.irect

def rect_mul(r, m):          # __mul__: transform with matrix
    if type(r) is fitz.Rect:
        r1 = fitz.Rect(r)
    else:
        r1 = r.rect
    if type(m) in (int, float):
        r1 = fitz.Rect(r1.x0 * m, r1.y0 * m, r1.x1 * m, r1.y1 * m)
    else:
        try:
            r1.transform(m)
        except:
            raise NotImplementedError("op2 must be number or 'Matrix'")
    if type(r) is fitz.Rect:
        return r1
    else:
        return r1.irect

def rect_equ(r, r2):       # __equ__
    return type(r) == type(r2) and rect_true(r - r2) == 0

def rect_true(r):
    return (abs(r.x0) + abs(r.y0) + abs(r.x1) + abs(r.y1)) > 0
    
#==============================================================================
# arithmetic methods for fitz.Point
#==============================================================================
def point_add(p1, p2):
    if type(p2) is fitz.Point:
        p = p2
    elif type(p2) in (int, float):
        p = fitz.Point(p2, p2)
    else:
        raise NotImplementedError("op2 must be 'Point' or number")
    return fitz.Point(p1.x + p.x, p1.y + p.y)

def point_sub(p1, p2):
    if type(p2) is fitz.Point:
        p = p2
    elif type(p2) in (int, float):
        p = fitz.Point(p2, p2)
    else:
        raise NotImplementedError("op2 must be 'Point' or number")
    return fitz.Point(p1.x - p.x, p1.y - p.y)

def point_mul(p, m):
    if type(m) in (int, float):
        return fitz.Point(p.x*m, p.y*m)
    p1 = fitz.Point(p)
    try:
        return p1.transform(m)
    except:
        raise NotImplementedError("op2 must be 'Matrix' or number")

def point_abs(p):
    return math.sqrt(p.x**2 + p.y**2)

def point_true(p):
    return (abs(p.x) + abs(p.y)) > 0

def point_equ(p, p2):       # __equ__
    return type(p) == type(p2) and point_true(p - p2) == 0

def point_contains(p, x):
    if type(x) not in (int, float):
        return False
    else:
        return x in tuple(p)

#==============================================================================
# Document method Set Metadata
#==============================================================================
def setMetadata(doc, m):
    """Set a PDF's metadata (/Info dictionary)\nm: dictionary like doc.metadata'."""
    if doc.isClosed or doc.isEncrypted:
        raise ValueError("operation on closed or encrypted document")
    if type(m) is not dict:
        raise ValueError("arg2 must be a dictionary")
    for k in m.keys():
        if not k in ("author", "producer", "creator", "title", "format",
                     "encryption", "creationDate", "modDate", "subject",
                     "keywords"):
            raise ValueError("invalid dictionary key: " + k)
    d = "<</Author"
    d += fitz.getPDFstr(m.get("author", "none"))
    d += "/CreationDate"
    d += fitz.getPDFstr(m.get("creationDate", "none"))
    d += "/Creator"
    d += fitz.getPDFstr(m.get("creator", "none"))
    d += "/Keywords"
    d += fitz.getPDFstr(m.get("keywords", "none"))
    d += "/ModDate"
    d += fitz.getPDFstr(m.get("modDate", "none"))
    d += "/Producer"
    d += fitz.getPDFstr(m.get("producer", "none"))
    d += "/Subject"
    d += fitz.getPDFstr(m.get("subject", "none"))
    d += "/Title"
    d += fitz.getPDFstr(m.get("title", "none"))
    d += ">>"
    r = doc._setMetadata(d)
    if r == 0:
        doc.initData()
    return r

def getDestStr(xref, ddict):
    if not ddict:
        return ""
    str_goto = "/Dest[%s %s R/XYZ %s %s %s]"

    if type(ddict) in (int, float):
        dest = str_goto % (xref[0], xref[1], 0, str(ddict), 0)
        return dest
    d_kind = ddict["kind"]

    if d_kind == fitz.LINK_NONE:
        return ""

    if ddict["kind"] == fitz.LINK_GOTO:
        d_zoom = ddict["zoom"]
        d_left = ddict["to"].x
        d_top  = ddict["to"].y
        dest = str_goto % (xref[0], xref[1], str(d_left), str(d_top),
                           str(d_zoom))
        return dest

    str_gotor1 = "/A<</D[%s /XYZ %s %s %s]/F<</F%s/UF%s/Type/Filespec>>" \
                 "/S/GoToR>>"
    str_gotor2 = "/A<</D%s/F<</F%s/UF%s/Type/Filespec>>/S/GoToR>>"
    str_launch = "/A<</F<</F%s/UF%s/Type/Filespec>>/S/Launch>>"
    str_uri    = "/A<</S/URI/URI%s/Type/Action>>"

    if ddict["kind"] == fitz.LINK_URI:
        dest = str_uri % (fitz.getPDFstr(ddict["uri"]),)
        return dest

    if ddict["kind"] == fitz.LINK_LAUNCH:
        fspec = fitz.getPDFstr(ddict["file"])
        dest = str_launch % (fspec, fspec)
        return dest

    if ddict["kind"] == fitz.LINK_GOTOR and ddict["page"] < 0:
        fspec = fitz.getPDFstr(ddict["file"])
        dest = str_gotor2 % (fitz.getPDFstr(ddict["to"]), fspec, fspec)
        return dest

    if ddict["kind"] == fitz.LINK_GOTOR and ddict["page"] >= 0:
        fspec = fitz.getPDFstr(ddict["file"])
        dest = str_gotor1 % (ddict["page"], ddict["to"].x, ddict["to"].y,
                                   ddict["zoom"], fspec, fspec)
        return dest

    return ""

#==============================================================================
# Document method set Table of Contents
#==============================================================================
def setToC(doc, toc):
    '''Create new outline tree (table of contents)\ntoc: a Python list of lists. Each entry must contain level, title, page and optionally top margin on the page.'''
    if doc.isClosed or doc.isEncrypted:
        raise ValueError("operation on closed or encrypted document")

    toclen = len(toc)
    # check toc validity ------------------------------------------------------
    if type(toc) is not list:
        raise ValueError("arg2 must be a list")
    if toclen == 0:
        return len(doc._delToC())
    pageCount = len(doc)
    t0 = toc[0]
    if type(t0) is not list:
        raise ValueError("arg2 must contain lists of 3 or 4 items")
    if t0[0] != 1:
        raise ValueError("hierarchy level of item 0 must be 1")
    for i in list(range(toclen-1)):
        t1 = toc[i]
        t2 = toc[i+1]
        if not -1 <= t1[2] <= pageCount:
            raise ValueError("row %s:page number out of range" % (str(i),))
        if (type(t2) is not list) or len(t2) < 3 or len(t2) > 4:
            raise ValueError("arg2 must contain lists of 3 or 4 items")
        if (type(t2[0]) is not int) or t2[0] < 1:
            raise ValueError("hierarchy levels must be int > 0")
        if t2[0] > t1[0] + 1:
            raise ValueError("row %s: hierarchy steps must not be > 1" + (str(i),))
    # no formal errors in toc --------------------------------------------------

    old_xrefs = doc._delToC()          # del old outlines, get xref numbers
    # prepare table of xrefs for new bookmarks
    xref = [0] + old_xrefs
    xref[0] = doc._getOLRootNumber()        # entry zero is outline root xref#
    if toclen > len(old_xrefs):             # too few old xrefs?
        for i in range((toclen - len(old_xrefs))):
            xref.append(doc._getNewXref())  # acquire new ones

    lvltab = {0:0}                     # to store last entry per hierarchy level

#==============================================================================
# contains new outline objects as strings - first one is outline root
#==============================================================================
    olitems = [{"count":0, "first":-1, "last":-1, "xref":xref[0]}]
#==============================================================================
# build olitems as a list of PDF-like connnected dictionaries
#==============================================================================
    for i in range(toclen):
        o = toc[i]
        lvl = o[0] # level
        title = fitz.getPDFstr(o[1]) # titel
        pno = min(doc.pageCount - 1, max(0, o[2] - 1)) # page number
        top = 0
        if len(o) < 4:
            p = doc.loadPage(pno)
            top = int(round(p.bound().y1) - 36)  # default top location on page
            p = None                             # free page resources
        top1 = top + 0                        # accept provided top parameter
        dest_dict = {}
        if len(o) > 3:
            if type(o[3]) is int or type(o[3]) is float:
                top1 = int(round(o[3]))
                dest_dict = o[3]
            else:
                dest_dict = o[3] if type(o[3]) is dict else {}
                try:
                    top1 = int(round(o[3]["to"].y)) # top
                except: pass
        else:
            dest_dict = top
        if  0 <= top1 <= top + 36:
            top = top1
        d = {}
        d["first"] = -1
        d["count"] = 0
        d["last"]  = -1
        d["prev"]  = -1
        d["next"]  = -1
        d["dest"]  = getDestStr(doc._getPageObjNumber(pno), dest_dict)
        d["top"]   = top
        d["title"] = title
        d["parent"] = lvltab[lvl-1]
        d["xref"] = xref[i+1]
        lvltab[lvl] = i+1
        parent = olitems[lvltab[lvl-1]]
        parent["count"] += 1

        if parent["first"] == -1:
            parent["first"] = i+1
            parent["last"] = i+1
        else:
            d["prev"] = parent["last"]
            prev = olitems[parent["last"]]
            prev["next"]   = i+1
            parent["last"] = i+1
        olitems.append(d)

#==============================================================================
# now create each ol item as a string and insert it in the PDF
#==============================================================================
    for i, ol in enumerate(olitems):
        txt = "<<"
        if ol["count"] > 0:
            txt += "/Count -" + str(ol["count"])
        try:
            txt += ol["dest"]
        except: pass
        try:
            if ol["first"] > -1:
                txt += "/First " + str(xref[ol["first"]]) + " 0 R"
        except: pass
        try:
            if ol["last"] > -1:
                txt += "/Last " + str(xref[ol["last"]]) + " 0 R"
        except: pass
        try:
            if ol["next"] > -1:
                txt += "/Next " + str(xref[ol["next"]]) + " 0 R"
        except: pass
        try:
            if ol["parent"] > -1:
                txt += "/Parent " + str(xref[ol["parent"]]) + " 0 R"
        except: pass
        try:
            if ol["prev"] > -1:
                txt += "/Prev " + str(xref[ol["prev"]]) + " 0 R"
        except: pass
        try:
            txt += "/Title" + ol["title"]
        except: pass
        if i == 0:           # special: this is the outline root
            txt += "/Type/Outlines"
        txt += ">>"
        rc = doc._updateObject(xref[i], txt)     # insert the PDF object
        if rc != 0:
            raise ValueError("outline insert error:\n" + txt)

    doc.initData()
    return toclen

def do_links(doc1, doc2, from_page = -1, to_page = -1, start_at = -1):
    '''Insert links contained in copied page range into destination PDF.
    Parameter values **must** equal those of method insertPDF() - which must have been previously executed.'''
    #--------------------------------------------------------------------------
    # define skeletons for /Annots object texts
    #--------------------------------------------------------------------------
    annot_goto ='''<</Dest[%s 0 R /XYZ %s %s 0]/Rect[%s]/Subtype/Link>>'''

    annot_gotor = '''<</A<</D[%s /XYZ %s %s 0]/F<</F(%s)/UF(%s)/Type/Filespec
    >>/S/GoToR>>/Rect[%s]/Subtype/Link>>'''

    annot_launch = '''<</A<</F<</F(%s)/UF(%s)/Type/Filespec>>/S/Launch
    >>/Rect[%s]/Subtype/Link>>'''

    annot_uri = '''<</A<</S/URI/URI(%s)/Type/Action>>/Rect[%s]/Subtype/Link>>'''

    #--------------------------------------------------------------------------
    # internal function to create the actual "/Annots" object string
    #--------------------------------------------------------------------------
    def cre_annot(lnk, xref_dst, list_src, height):
        '''Create annotation object string for a passed-in link.'''

        # "from" rectangle is always there. Note: y-coords are from bottom!
        r = lnk["from"]
        rect = "%s %s %s %s" % (str(r.x0), str(height - r.y0),   # correct y0
                                str(r.x1), str(height - r.y1))   # correct y1
        if lnk["kind"] == fitz.LINK_GOTO:
            txt = annot_goto
            idx = list_src.index(lnk["page"])
            annot = txt % (str(xref_dst[idx]), str(lnk["to"].x),
                           str(lnk["to"].y), rect)
        elif lnk["kind"] == fitz.LINK_GOTOR:
            txt = annot_gotor
            annot = txt % (str(lnk["page"]), str(lnk["to"].x),
                           str(lnk["to"].y),
                           lnk["file"], lnk["file"],
                           rect)
        elif lnk["kind"] == fitz.LINK_LAUNCH:
            txt = annot_launch
            annot = txt % (lnk["file"], lnk["file"], rect)
        elif lnk["kind"] == fitz.LINK_URI:
            txt = annot_uri
            annot = txt % (lnk["uri"], rect)
        else:
            annot = ""

        return annot
    #--------------------------------------------------------------------------

    # validate & normalize parameters
    if from_page < 0:
        fp = 0
    elif from_page >= doc2.pageCount:
        from_page = doc2.page_count - 1
    else:
        fp = from_page

    if to_page < 0 or to_page >= doc2.pageCount:
        tp = doc2.pageCount - 1
    else:
        tp = to_page

    if start_at < 0:
        raise ValueError("do_links: 'start_at' arg must be >= 0")
    sa = start_at

    incr = 1 if fp <= tp else -1            # page range could be reversed
    # lists of source / destination page numbers
    list_src = list(range(fp, tp + incr, incr))
    list_dst = [sa + i for i in range(len(list_src))]
    # lists of source / destination page xref numbers
    xref_src = []
    xref_dst = []
    for i in range(len(list_src)):
        p_src = list_src[i]
        p_dst = list_dst[i]
        old_xref = doc2._getPageObjNumber(p_src)[0]
        new_xref = doc1._getPageObjNumber(p_dst)[0]
        xref_src.append(old_xref)
        xref_dst.append(new_xref)

    # create /Annots per copied page in destination PDF
    for i in range(len(xref_src)):
        page_src = doc2[list_src[i]]
        links = page_src.getLinks()
        if len(links) == 0:
            page_src = None
            continue
        height = page_src.bound().y1
        p_annots = ""
        page_dst = doc1[list_dst[i]]
        link_tab = []
        for l in links:
            if l["kind"] == fitz.LINK_GOTO and (l["page"] not in list_src):
                continue          # target not in copied pages
            annot_text = cre_annot(l, xref_dst, list_src, height)
            if not annot_text:
                raise ValueError("cannot create /Annot for kind: " + str(l["kind"]))
            link_tab.append(annot_text)
        if len(link_tab) > 0:
            page_dst._addAnnot_FromString(link_tab)
        page_dst = None
        page_src = None
    return

def getLinkText(page, lnk):
    #--------------------------------------------------------------------------
    # define skeletons for /Annots object texts
    #--------------------------------------------------------------------------
    annot_goto = "<</Dest[%s 0 R/XYZ %s %s 0]/Rect[%s]/Subtype/Link>>"

    annot_goto_n = "<</A<</D%s/S/GoTo>>/Rect[%s]/Subtype/Link>>"

    annot_gotor = '''<</A<</D[%s /XYZ %s %s 0]/F<</F(%s)/UF(%s)/Type/Filespec
    >>/S/GoToR>>/Rect[%s]/Subtype/Link>>'''

    annot_gotor_n = "<</A<</D%s/F(%s)/S/GoToR>>/Rect[%s]/Subtype/Link>>"

    annot_launch = '''<</A<</F<</F(%s)/UF(%s)/Type/Filespec>>/S/Launch
    >>/Rect[%s]/Subtype/Link>>'''

    annot_uri = "<</A<</S/URI/URI(%s)>>/Rect[%s]/Subtype/Link>>"

    annot_named = "<</A<</S/Named/N/%s/Type/Action>>/Rect[%s]/Subtype/Link>>"

    r = lnk["from"]
    height = page.rect.height
    rect = "%s %s %s %s" % (str(r.x0), str(height - r.y0),   # correct y0
                            str(r.x1), str(height - r.y1))   # correct y1

    annot = ""
    if lnk["kind"] == fitz.LINK_GOTO:
        if lnk["page"] >= 0:
            txt = annot_goto
            pno = lnk["page"]
            xref = page.parent._getPageXref(pno)[0]
            pnt = lnk.get("to", fitz.Point(0, 0))          # destination point
            annot = txt % (xref, str(pnt.x),
                           str(pnt.y), rect)
        else:
            txt = annot_goto_n
            annot = txt % (fitz.getPDFstr(lnk["to"]), rect)
        
    elif lnk["kind"] == fitz.LINK_GOTOR:
        if lnk["page"] >= 0:
            txt = annot_gotor
            pnt = lnk.get("to", fitz.Point(0, 0))          # destination point
            if type(pnt) is not fitz.Point:
                pnt = fitz.Point(0, 0)
            annot = txt % (str(lnk["page"]), str(pnt.x), str(pnt.y),
                           lnk["file"], lnk["file"], rect)
        else:
            txt = annot_gotor_n
            annot = txt % (fitz.getPDFstr(lnk["to"]), lnk["file"], rect)

    elif lnk["kind"] == fitz.LINK_LAUNCH:
        txt = annot_launch
        annot = txt % (lnk["file"], lnk["file"], rect)

    elif lnk["kind"] == fitz.LINK_URI:
        txt = annot_uri
        annot = txt % (lnk["uri"], rect)

    elif lnk["kind"] == fitz.LINK_NAMED:
        txt = annot_named
        annot = txt % (lnk["name"], rect)

    return annot    
    
def updateLink(page, lnk):
    """ Update a link on the current page. """
    fitz.CheckParent(page)
    annot = getLinkText(page, lnk)
    assert annot != "", "link kind not supported"
    page.parent._updateObject(lnk["xref"], annot, page = page) 
    return

def insertLink(page, lnk, mark = True):
    """ Insert a new link for the current page. """
    fitz.CheckParent(page)
    annot = getLinkText(page, lnk)
    assert annot != "", "link kind not supported"
    page._addAnnot_FromString([annot])
    return

def intersects(me, rect):
    """ Checks whether this rectangle and 'rect' have a rectangle with a positive area in common."""
    if type(rect) not in (fitz.Rect, fitz.IRect):
        return False
    if me.isEmpty or me.isInfinite or rect.isEmpty or rect.isInfinite:
        return False
    r = me & rect
    if r.isEmpty or r.isInfinite:
        return False
    return True

#-------------------------------------------------------------------------------
# Page.insertTextbox
#-------------------------------------------------------------------------------
def insertTextbox(page, rect, buffer, fontname = None, fontfile = None,
                  xref = 0, fontsize = 11, color = (0,0,0), expandtabs = 1,
                  charwidths = None, charlimit = 256, align = 0):
    """Insert text into a given rectangle.
    Parameters:
    buffer - string of text to be inserted
    fontname - name of a Base-14 font, font reference or font reference
    fontfile - file name of a font to be included
    color - RGB color tuple
    expandtabs - handles tab chars with string function
    charwidths - list of glyph widths
    charlimit - limit number of glyphs if width list should be created
    align - align left, center or right
    Returns: float of unused rectangle height
    
    """
    fitz.CheckParent(page)
    if rect not in page.rect:
        raise ValueError("rect not contained in page")
    if rect.isEmpty or rect.isInfinite:
        raise ValueError("rect must be finite and not empty")
    fitz.CheckColor(color)

    widthtab = charwidths
    if not widthtab:                   # need to build our own ...
        fname = fontname
        ffile = fontfile
        xref  = 0
        if ffile:                      # filename given
            fname = None
        elif fname.startswith("/"):    # existing fontname given
            fl = page.getFontList()    # get font list
            for f in fl:
                if f[4] == fname[1:]:  # reference found
                    if f[3] in fitz.Base14_fontnames:   # means: Base-14-Font!
                        xref = -1      # ignore xref
                        fname = f[3]   # use Base-14 name
                        break
                    xref = f[0]        # xref of referenced font
                    break
            if xref == 0:              # /fontname not in list
                raise ValueError("invalid font reference for page")
            elif xref > 0:             # found font reference
                fname = ffile = None
            else:                      # Base-14 name given
                xref = 0
                ffile = None
        widthtab = page.parent._getCharWidths(fontname = fname, xref = xref,
                   fontfile = ffile, limit = charlimit)
    def pixlen(x):
        try:
            return sum([widthtab[ord(c)] for c in x]) * fontsize
        except IndexError:
            m = max([ord(c) for c in x])
            print("max. code point: % - increase charlimit" % m)

    text = ""
    lheight = fontsize * 1.2
    maxpos = rect.y1
    point = fitz.Point(rect.x0, rect.y0 + fontsize)   # text starts here
    pos = point.y                           # y of first line    
    blen = pixlen(" ")                      # pixel size of space
    maxwidth = rect.width                   # pixels of one full line
    t0 = buffer.splitlines()

    #===========================================================================
    # line loop
    #===========================================================================
    just_tab = []                           # stores 'justify' indicators
    for i, line in enumerate(t0):
        line_t = line.expandtabs(expandtabs).split(" ")  # split line into words
        lbuff = ""                          # init line buffer
        rest = maxwidth                     # available line pixels
        #=======================================================================
        # word loop
        #=======================================================================
        for word in line_t:
            pl_w = pixlen(word)             # pixel len of 1 word
            if rest >= pl_w:                # will it fit on the line?
                lbuff += word + " "         # yes, and append word
                rest -= (pl_w + blen)       # update available line space
                continue
            # word won't fit in remaining space - output the line
            lbuff = lbuff.rstrip() + "\n"   # line full, append line break
            text += lbuff                   # append to total page text
            pos += lheight                  # increase line position
            just_tab.append(True)           # line may be justified
            lbuff = ""                      # re-init line buffer
            rest = maxwidth                 # re-init avail. space
            if pl_w <= maxwidth:            # word shorter than 1 line?
                lbuff = word + " "          # start new line with it
                rest = maxwidth - pl_w - blen    # update free space
                continue
            # long word: split across multiple lines - char by char ...
            just_tab[-1] = False            # reset justify indicator
            for c in word:
                if pixlen(lbuff) <= maxwidth - pixlen(c):
                    lbuff += c
                else:                       # line full
                    lbuff += "\n"           # close line
                    text += lbuff           # append to text
                    pos += lheight          # increase line position
                    just_tab.append(False)  # do not justify line
                    lbuff = c               # start new line with this char
            lbuff += " "                    # finish long word
            rest = maxwidth - pixlen(lbuff) # long word stored
                
        if lbuff != "":                     # unprocessed line content?
            text += lbuff.rstrip()          # append to text
            just_tab.append(False)          # do not justify line
        if i < len(t0) - 1:                 # not the last line?
            text += "\n"                    # insert line break
            pos += lheight                  # increase line position
    
    more = pos - maxpos                     # difference to rect bottom
    
    if more > 1e-5:                         # landed too much below
        raise ValueError("rect must be %g pixels higher to store text" % more)

    more = abs(more)
    if more < 1e-5:
        more = 0                            # don't bother with small epsilons
    if align == 0:                          # left alignment: output full chunk
        page.insertText(point, text, fontsize = fontsize,
                        fontname = fontname, fontfile = fontfile, color = color)
        return more
    # center, right, justify: output each line with its own specifics
    spacing = 0
    text_t = text.splitlines()              # split text in lines again
    for i, t in enumerate(text_t):
        pl = maxwidth - pixlen(t)           # pixel amount of empty line space
        pnt = fitz.Point(point.x, point.y + i * lheight)   # text start of line
        if align == 1:                      # center: right shift by half width
            pnt = fitz.Point(pnt.x + pl / 2, pnt.y)
        elif align == 2:                    # right: right shift by full width
            pnt = fitz.Point(pnt.x + pl, pnt.y)
        else:                               # justify
            spaces = t.count(" ")           # number of spaces in line
            if spaces > 0 and just_tab[i]:  # if any, and we may justify
                spacing = pl / spaces       # make every space so  much larger
            else:
                spacing = 0                 # keep normal space length

        page.insertText(pnt, t, fontsize = fontsize, fontname = fontname,
                        fontfile = fontfile, color = color,
                        wordspacing = spacing)
    return more

#-------------------------------------------------------------------------------
# Page.drawLine
#-------------------------------------------------------------------------------
def drawLine(page, p1, p2, color = (0, 0, 0), dashes = None,
               width = 1, roundCap = True, overlay = True):
    """Draw a line between points p1 and p2.
    """
    fitz.CheckParent(page)
    fitz.CheckColor(color)

    doc = page.parent
    xreflist = page._getContents()
    if overlay:
        xref = xreflist[-1]
    else:
        xref = xreflist[0]
        
    cont = doc._getXrefStream(xref)
    
    h = page.rect.y1
    
    d = ""
    if dashes is not None and len(dashes) > 0:
        d = dashes + "d"
    
    templ1 = "\nq %i J %s %g %g %g RG %g w %g %g m %g %g l h S Q "
    
    c  = templ1 % (roundCap, d, color[0], color[1], color[2], width,
                   p1.x, h - p1.y, p2.x, h - p2.y)
    
    if sys.version_info[0] > 2:
        c = bytes(c, "utf-8")
    
    if overlay:
        cont += c        
    else:
        cont = c + cont

    doc._updateStream(xref, cont)
    
    return


#-------------------------------------------------------------------------------
# Page.drawRect
#-------------------------------------------------------------------------------
def drawRect(page, rect, color = (0, 0, 0), fill = None, dashes = None,
               width = 1, roundCap = True, overlay = True):
    """Draw a rectangle on a PDF page.
    """
    page.drawPolyline((rect.top_left, rect.top_right, rect.bottom_right,
                       rect.bottom_left), color = color, fill = fill,
                       dashes = dashes, width = width, roundCap = roundCap,
                       closePath = True, overlay = overlay)
    return


#-------------------------------------------------------------------------------
# Page.drawPolyline
#-------------------------------------------------------------------------------
def drawPolyline(page, points, color = (0, 0, 0), fill = None, dashes = None,
               width = 1, roundCap = True, overlay = True, closePath = False):
    """Draws a circle on a PDF page given its center and radius.
    """
    fitz.CheckParent(page)
    assert len(points) > 1, "need at least two points to draw polyline"
    fitz.CheckColor(color)
    fitz.CheckColor(fill)
    doc = page.parent
    
    xreflist = page._getContents()
    if overlay:
        xref = xreflist[-1]
    else:
        xref = xreflist[0]
        
    cont = doc._getXrefStream(xref)
    
    h = page.rect.y1
    d = ""
    if dashes is not None and len(dashes) > 0:
        d = dashes + "d"
    tempfl = "%g %g %g rg\n"
    templ1 = "\nq %i J %i j %s %g %g %g RG %g w %g %g m\n"
    templ2 = "%g %g l\n"
    
    for i, p in enumerate(points):
        if i == 0:
            c = templ1 % (roundCap, roundCap, d,
                          color[0], color[1], color[2],
                          width, p.x, h - p.y)
            if fill is not None:
                c += tempfl % (fill[0], fill[1], fill[2])
        else:
            c += templ2 % (p.x, h - p.y)
    
    if closePath:
        c += "h "
    if fill is not None:
        c += "B Q "
    else:
        c += "S Q "
    
    if sys.version_info[0] > 2:
        c = bytes(c, "utf-8")
        
    if overlay:
        cont += c
    else:
        cont = c + cont
    
    doc._updateStream(xref, cont)
    
    return


#-------------------------------------------------------------------------------
# Page.drawCircle
#-------------------------------------------------------------------------------
def drawCircle(page, center, radius, color = (0, 0, 0), fill = None,
               dashes = None, width = 1, roundCap = True, overlay = True):
    """Draws a circle on a PDF page given its center and radius.
    """
    fitz.CheckParent(page)
    fitz.CheckColor(color)
    fitz.CheckColor(fill)
    doc = page.parent
    xreflist = page._getContents()
    if overlay:
        xref = xreflist[-1]
    else:
        xref = xreflist[0]
        
    cont = doc._getXrefStream(xref)
    
    h = page.rect.y1
    kappa = 0.552 * radius
    
    l0 = "%g %g %g rg\n"
    l1 = "\nq %g %g %g RG %g w %i J\n"
    l2 = "%s d\n"
    l3 = "%g %g m\n"
    l4 = "%g %g %g %g %g %g c\n"
    
    # the list of points needed for the Bézier curves
    # approximating the circle
    p00  = [center.x - radius, h - (center.y)]                  # p0
    p00 += [center.x - radius, h - (center.y - kappa)]          # p1
    p00 += [center.x - kappa,  h - (center.y - radius)]         # p2
    p00 += [center.x,          h - (center.y - radius)]         # p3
    p00 += [center.x + kappa,  h - (center.y - radius)]         # p4
    p00 += [center.x + radius, h - (center.y - kappa)]          # p5
    p00 += [center.x + radius, h - (center.y)]                  # p6
    p00 += [center.x + radius, h - (center.y + kappa)]          # p7
    p00 += [center.x + kappa,  h - (center.y + radius)]         # p8
    p00 += [center.x,          h - (center.y + radius)]         # p9
    p00 += [center.x - kappa,  h - (center.y + radius)]         # p10
    p00 += [center.x - radius, h - (center.y + kappa)]          # p11
    
    c  = l1 % (color[0], color[1], color[2], width, roundCap)
    if dashes is not None and len(dashes) > 0:
        c += l2 % dashes
    if fill is not None:
        c+= l0 % (fill[0], fill[1], fill[2])
    c += l3 % (p00[0], p00[1])
    c += l4 % (p00[2], p00[3], p00[4], p00[5], p00[6], p00[7])
    c += l4 % (p00[8], p00[9], p00[10], p00[11], p00[12], p00[13])
    c += l4 % (p00[14], p00[15], p00[16], p00[17], p00[18], p00[19])
    c += l4 % (p00[20], p00[21], p00[22], p00[23], p00[0], p00[1])
    if fill is not None:
        c += "h B Q "
    else:
        c += "h S Q "
    
    if sys.version_info[0] > 2:
        c = bytes(c, "utf-8")
        
    if overlay:
        cont += c
    else:
        cont = c + cont
    
    doc._updateStream(xref, cont)
    
    return


#-------------------------------------------------------------------------------
# Page.drawOval
#-------------------------------------------------------------------------------
def drawOval(page, rect, color = (0, 0, 0), fill = None, dashes = None,
               width = 1, roundCap = True, overlay = True):
    """Draws an oval on a PDF page given its containing rectangle.
    """
    fitz.CheckParent(page)
    fitz.CheckColor(color)
    fitz.CheckColor(fill)
    
    doc = page.parent
    xreflist = page._getContents()
    if overlay:
        xref = xreflist[-1]
    else:
        xref = xreflist[0]
        
    cont = doc._getXrefStream(xref)
    
    h = page.rect.y1
    
    kappah = 0.552 * rect.width / 2
    kappav = 0.552 * rect.height / 2
    
    l0 = "%g %g %g rg\n"
    l1 = "\nq %g %g %g RG %g w %i J\n"
    l2 = "%s d\n"
    l3 = "%g %g m\n"
    l4 = "%g %g %g %g %g %g c\n"
    
    # the list of points needed for the Bézier curves
    # approximating the ellipse
    p00  = [rect.x0, h - (rect.y0 + rect.height / 2)]            # p0
    p00 += [rect.x0, h - (rect.y0 + rect.height / 2 - kappav)]   # p1
    p00 += [rect.x0 + rect.width / 2 - kappah, h - (rect.y0)]    # p2
    p00 += [rect.x0 + rect.width / 2, h - (rect.y0)]             # p3
    p00 += [rect.x0 + rect.width / 2 + kappah, h - (rect.y0)]    # p4
    p00 += [rect.x1, h - (rect.y0 + rect.height / 2 - kappav)]   # p5
    p00 += [rect.x1, h - (rect.y0 + rect.height / 2)]            # p6
    p00 += [rect.x1, h - (rect.y0 + rect.height / 2 + kappav)]   # p7
    p00 += [rect.x0 + rect.width / 2 + kappah, h - (rect.y1)]    # p8
    p00 += [rect.x0 + rect.width / 2, h - (rect.y1)]             # p9
    p00 += [rect.x0 + rect.width / 2 - kappah, h - (rect.y1)]    # p10
    p00 += [rect.x0, h - (rect.y0 + rect.height / 2 + kappav)]   # p11
    
    c  = l1 % (color[0], color[1], color[2], width, roundCap)
    if fill is not None:
        c+= l0 % (fill[0], fill[1], fill[2])
    if dashes is not None and len(dashes) > 0:
        c += l2 % dashes
    c += l3 % (p00[0], p00[1])
    c += l4 % (p00[2], p00[3], p00[4], p00[5], p00[6], p00[7])
    c += l4 % (p00[8], p00[9], p00[10], p00[11], p00[12], p00[13])
    c += l4 % (p00[14], p00[15], p00[16], p00[17], p00[18], p00[19])
    c += l4 % (p00[20], p00[21], p00[22], p00[23], p00[0], p00[1])
    if fill is not None:
        c += "h B Q "
    else:
        c += "h S Q "
    
    if sys.version_info[0] > 2:
        c = bytes(c, "utf-8")
        
    if overlay:
        cont += c
    else:
        cont = c + cont
    
    doc._updateStream(xref, cont)
    
    return


#-------------------------------------------------------------------------------
# Page.drawCurve
#-------------------------------------------------------------------------------
def drawCurve(page, p1, p2, p3, color = (0, 0, 0), fill = None, dashes = None,
               width = 1, closePath = False, roundCap = True, overlay = True):
    """Draws a Bézier curve along three arbitray points, using control points on their connecting lines p1 -> p2 and p2 - > p3. Points p1 and p3 are the start and end point of the curve, respectively.
    """
    kappa = 0.552
    k1 = p1 + (p2 - p1) * kappa
    k2 = p3 + (p2 - p3) * kappa
    drawBezier(page, p1, k1, k2, p3, fill = fill, color = color,
               dashes = dashes, width = width, closePath = closePath,
               roundCap = roundCap, overlay = overlay)

    return


#-------------------------------------------------------------------------------
# Page.drawBezier
#-------------------------------------------------------------------------------
def drawBezier(page, p1, p2, p3, p4, color = (0, 0, 0), fill = None, dashes = None,
               width = 1, closePath = False, roundCap = True, overlay = True):
    """Draws a Bézier curve for four points. Start and end are p1 and p4, respectively. p2 and p3 are usedas control points only.
    """
    fitz.CheckParent(page)
    fitz.CheckColor(color)
    fitz.CheckColor(fill)
    
    doc = page.parent
    xreflist = page._getContents()
    if overlay:
        xref = xreflist[-1]
    else:
        xref = xreflist[0]
    h = page.rect.y1
    cont = doc._getXrefStream(xref)
    l0 = "%g %g %g rg\n"
    l1 = "\nq %g %g %g RG %g w %i J %i j\n"
    l2 = "%s d\n"
    l3 = "%g %g m\n"
    l4 = "%g %g %g %g %g %g c\n"
    
    c  = l1 % (color[0], color[1], color[2], width, roundCap, roundCap)
    if fill is not None:
        c+= l0 % (fill[0], fill[1], fill[2])
    if dashes is not None and len(dashes) > 0:
        c += l2 % dashes
    c += l3 % (p1.x, h - p1.y)
    c += l4 % (p2.x, h - p2.y, p3.x, h - p3.y, p4.x, h - p4.y)
    if closePath:
        c += "h "
    if fill is not None:
        c += "B Q "
    else:
        c += "S Q "
    
    if sys.version_info[0] > 2:
        c = bytes(c, "utf-8")
        
    if overlay:
        cont += c
    else:
        cont = c + cont
    
    doc._updateStream(xref, cont)
    
    return


#-------------------------------------------------------------------------------
# Annot.updateImage
#-------------------------------------------------------------------------------
def updateImage(annot):
    '''Update border and color information in the appearance dictionary /AP.'''
    fitz.CheckParent(annot)
    
    def modAP(tab, ctab, ftab, wtab, dtab):
        '''replace all occurrences of colors, width and dashes by provided values.'''
        ntab = []
        in_text_block = False          # if True do nothing
        for i in range(len(tab)):
            if tab[i] == b"Do":        # another XObject invoked
                raise ValueError("nested XObject calls not supported")
            ntab.append(tab[i])        # store in output
            if tab[i] == b"BT":        # begin of text block
                in_text_block = True   # switch on
                continue
            if tab[i] == b"ET":        # end of text block
                in_text_block = False  # switch off
                continue
            if in_text_block:          # skip if in text block
                continue
            if ftab[4] and (tab[i] == b"s"):     # fill color provided
                ntab[-1] = b"b"        # make sure it is used
                continue
            if ctab[4]:                # stroke color provided
                if tab[i] == b"G":     # it is a gray
                    del ntab[-2:]
                    ntab.extend(ctab)
                    continue
                elif tab[i] == b"RG":  # it is RGB
                    del ntab[len(ntab)-4:]
                    ntab.extend(ctab)
                    continue
                elif tab[i] == b"K":   # it is CMYK
                    del ntab[len(ntab)-5:]
                    ntab.extend(ctab)
                    continue
            if ftab[4]:                # fill color provided
                if tab[i] == b"g":     # it is a gray
                    del ntab[-2:]
                    ntab.extend(ftab)
                    continue
                elif tab[i] == b"rg":  # it is RGB
                    del ntab[len(ntab)-4:]
                    ntab.extend(ftab)
                    continue
                elif tab[i] == b"k":   # it is CMYK
                    del ntab[len(ntab)-5:]
                    ntab.extend(ftab)
                    continue
            if wtab[1]:                # width value provided
                if tab[i] == b"w":
                    ntab[-2] = wtab[0]
                    continue
            if dtab[1]:                # dashes provided
                if tab[i] == b"d":
                    j = len(ntab) - 1
                    x = b"d"
                    while not x.startswith(b"["):     # search start of array
                        j -= 1
                        x = ntab[j]
                    del ntab[j:]
                    ntab.extend(dtab)
        return ntab
        
    ap = annot._getAP() # get appearance text
    aptab = ap.split() # decompose into a list
        
    # prepare width, colors and dashes lists
    # fill color
    c = annot.colors.get("fill")
    ftab = [b""]*5
    if c and len(c) > 0:
        l = len(c)
        if l == 4:
            ftab[4] = b"k"
            for i in range(4):
                ftab[i] = str(round(c[i],4)).encode("utf-8")
        elif l == 3:
            ftab[4] = b"rg"
            for i in range(1, 4):
                ftab[i] = str(round(c[i-1],4)).encode("utf-8")
        elif l == 1:
            ftab[4] = b"g"
            ftab[3] = str(round(c[0],4)).encode("utf-8")

    # stroke color
    c = annot.colors.get("common")
    ctab = [b""]*5
    if c and len(c) > 0:
        l = len(c)
        if l == 4:
            ctab[4] = b"K"
            for i in range(4):
                ctab[i] = str(round(c[i], 4)).encode("utf-8")
        elif l == 3:
            ctab[4] = b"RG"
            for i in range(1, 4):
                ctab[i] = str(round(c[i-1], 4)).encode("utf-8")
        elif l == 1:
            ctab[4] = b"G"
            ctab[3] = str(round(c[0], 4)).encode("utf-8")

    # border width
    c = annot.border.get("width")
    wtab = [b"", b""]
    if c:
        wtab[0] = str(round(c, 4)).encode("utf-8")
        wtab[1] = b"w"

    # dash pattern
    c = annot.border.get("dashes")
    dtab = [b""]*2
    if not c is None:
        dtab[1] = b"0 d"
        dtab[0] = b"["
        for n in c:
            if n > 0:
                dtab[0] += str(n).encode("utf-8") + b" "
        dtab[0] += b"]"

    outlist = []
    outlist += ftab if ftab[4] else []
    outlist += ctab if ctab[4] else []
    outlist += wtab if wtab[1] else []
    outlist += dtab if dtab[1] else []
    if not outlist:
        return
    # make sure we insert behind a leading "save graphics state"
    if aptab[0] == b"q":
        outlist = [b"q"] + outlist
        aptab = aptab[1:]
    # now change every color, width and dashes spec
    aptab = modAP(aptab, ctab, ftab, wtab, dtab)
    aptab = outlist + aptab
    ap = b" ".join(aptab)
    annot._setAP(ap)
    return

#----------------------------------------------------------------------
# Name:        wx.lib.colourdb.py
# Purpose:     Adds a bunch of colour names and RGB values to the
#              colour database so they can be found by name
#
# Author:      Robin Dunn
#
# Created:     13-March-2001
# Copyright:   (c) 2001-2017 by Total Control Software
# Licence:     wxWindows license
# Tags:        phoenix-port, unittest, documented
#----------------------------------------------------------------------

def getColorList():
    """
    Returns a list of just the colour names used by this module.

    :rtype: list of strings
    """

    return [ x[0] for x in getColorInfoList() ]


def getColorInfoList():
    """
    Returns the list of colour name/value tuples used by this module.

    :rtype: list of tuples
    """

    return [
        ("ALICEBLUE", 240, 248, 255),
        ("ANTIQUEWHITE", 250, 235, 215),
        ("ANTIQUEWHITE1", 255, 239, 219),
        ("ANTIQUEWHITE2", 238, 223, 204),
        ("ANTIQUEWHITE3", 205, 192, 176),
        ("ANTIQUEWHITE4", 139, 131, 120),
        ("AQUAMARINE", 127, 255, 212),
        ("AQUAMARINE1", 127, 255, 212),
        ("AQUAMARINE2", 118, 238, 198),
        ("AQUAMARINE3", 102, 205, 170),
        ("AQUAMARINE4", 69, 139, 116),
        ("AZURE", 240, 255, 255),
        ("AZURE1", 240, 255, 255),
        ("AZURE2", 224, 238, 238),
        ("AZURE3", 193, 205, 205),
        ("AZURE4", 131, 139, 139),
        ("BEIGE", 245, 245, 220),
        ("BISQUE", 255, 228, 196),
        ("BISQUE1", 255, 228, 196),
        ("BISQUE2", 238, 213, 183),
        ("BISQUE3", 205, 183, 158),
        ("BISQUE4", 139, 125, 107),
        ("BLACK", 0, 0, 0),
        ("BLANCHEDALMOND", 255, 235, 205),
        ("BLUE", 0, 0, 255),
        ("BLUE1", 0, 0, 255),
        ("BLUE2", 0, 0, 238),
        ("BLUE3", 0, 0, 205),
        ("BLUE4", 0, 0, 139),
        ("BLUEVIOLET", 138, 43, 226),
        ("BROWN", 165, 42, 42),
        ("BROWN1", 255, 64, 64),
        ("BROWN2", 238, 59, 59),
        ("BROWN3", 205, 51, 51),
        ("BROWN4", 139, 35, 35),
        ("BURLYWOOD", 222, 184, 135),
        ("BURLYWOOD1", 255, 211, 155),
        ("BURLYWOOD2", 238, 197, 145),
        ("BURLYWOOD3", 205, 170, 125),
        ("BURLYWOOD4", 139, 115, 85),
        ("CADETBLUE", 95, 158, 160),
        ("CADETBLUE1", 152, 245, 255),
        ("CADETBLUE2", 142, 229, 238),
        ("CADETBLUE3", 122, 197, 205),
        ("CADETBLUE4", 83, 134, 139),
        ("CHARTREUSE", 127, 255, 0),
        ("CHARTREUSE1", 127, 255, 0),
        ("CHARTREUSE2", 118, 238, 0),
        ("CHARTREUSE3", 102, 205, 0),
        ("CHARTREUSE4", 69, 139, 0),
        ("CHOCOLATE", 210, 105, 30),
        ("CHOCOLATE1", 255, 127, 36),
        ("CHOCOLATE2", 238, 118, 33),
        ("CHOCOLATE3", 205, 102, 29),
        ("CHOCOLATE4", 139, 69, 19),
        ("COFFEE", 156, 79, 0),
        ("CORAL", 255, 127, 80),
        ("CORAL1", 255, 114, 86),
        ("CORAL2", 238, 106, 80),
        ("CORAL3", 205, 91, 69),
        ("CORAL4", 139, 62, 47),
        ("CORNFLOWERBLUE", 100, 149, 237),
        ("CORNSILK", 255, 248, 220),
        ("CORNSILK1", 255, 248, 220),
        ("CORNSILK2", 238, 232, 205),
        ("CORNSILK3", 205, 200, 177),
        ("CORNSILK4", 139, 136, 120),
        ("CYAN", 0, 255, 255),
        ("CYAN1", 0, 255, 255),
        ("CYAN2", 0, 238, 238),
        ("CYAN3", 0, 205, 205),
        ("CYAN4", 0, 139, 139),
        ("DARKBLUE", 0, 0, 139),
        ("DARKCYAN", 0, 139, 139),
        ("DARKGOLDENROD", 184, 134, 11),
        ("DARKGOLDENROD1", 255, 185, 15),
        ("DARKGOLDENROD2", 238, 173, 14),
        ("DARKGOLDENROD3", 205, 149, 12),
        ("DARKGOLDENROD4", 139, 101, 8),
        ("DARKGREEN", 0, 100, 0),
        ("DARKGRAY", 169, 169, 169),
        ("DARKKHAKI", 189, 183, 107),
        ("DARKMAGENTA", 139, 0, 139),
        ("DARKOLIVEGREEN", 85, 107, 47),
        ("DARKOLIVEGREEN1", 202, 255, 112),
        ("DARKOLIVEGREEN2", 188, 238, 104),
        ("DARKOLIVEGREEN3", 162, 205, 90),
        ("DARKOLIVEGREEN4", 110, 139, 61),
        ("DARKORANGE", 255, 140, 0),
        ("DARKORANGE1", 255, 127, 0),
        ("DARKORANGE2", 238, 118, 0),
        ("DARKORANGE3", 205, 102, 0),
        ("DARKORANGE4", 139, 69, 0),
        ("DARKORCHID", 153, 50, 204),
        ("DARKORCHID1", 191, 62, 255),
        ("DARKORCHID2", 178, 58, 238),
        ("DARKORCHID3", 154, 50, 205),
        ("DARKORCHID4", 104, 34, 139),
        ("DARKRED", 139, 0, 0),
        ("DARKSALMON", 233, 150, 122),
        ("DARKSEAGREEN", 143, 188, 143),
        ("DARKSEAGREEN1", 193, 255, 193),
        ("DARKSEAGREEN2", 180, 238, 180),
        ("DARKSEAGREEN3", 155, 205, 155),
        ("DARKSEAGREEN4", 105, 139, 105),
        ("DARKSLATEBLUE", 72, 61, 139),
        ("DARKSLATEGRAY", 47, 79, 79),
        ("DARKTURQUOISE", 0, 206, 209),
        ("DARKVIOLET", 148, 0, 211),
        ("DEEPPINK", 255, 20, 147),
        ("DEEPPINK1", 255, 20, 147),
        ("DEEPPINK2", 238, 18, 137),
        ("DEEPPINK3", 205, 16, 118),
        ("DEEPPINK4", 139, 10, 80),
        ("DEEPSKYBLUE", 0, 191, 255),
        ("DEEPSKYBLUE1", 0, 191, 255),
        ("DEEPSKYBLUE2", 0, 178, 238),
        ("DEEPSKYBLUE3", 0, 154, 205),
        ("DEEPSKYBLUE4", 0, 104, 139),
        ("DIMGRAY", 105, 105, 105),
        ("DODGERBLUE", 30, 144, 255),
        ("DODGERBLUE1", 30, 144, 255),
        ("DODGERBLUE2", 28, 134, 238),
        ("DODGERBLUE3", 24, 116, 205),
        ("DODGERBLUE4", 16, 78, 139),
        ("FIREBRICK", 178, 34, 34),
        ("FIREBRICK1", 255, 48, 48),
        ("FIREBRICK2", 238, 44, 44),
        ("FIREBRICK3", 205, 38, 38),
        ("FIREBRICK4", 139, 26, 26),
        ("FLORALWHITE", 255, 250, 240),
        ("FORESTGREEN", 34, 139, 34),
        ("GAINSBORO", 220, 220, 220),
        ("GHOSTWHITE", 248, 248, 255),
        ("GOLD", 255, 215, 0),
        ("GOLD1", 255, 215, 0),
        ("GOLD2", 238, 201, 0),
        ("GOLD3", 205, 173, 0),
        ("GOLD4", 139, 117, 0),
        ("GOLDENROD", 218, 165, 32),
        ("GOLDENROD1", 255, 193, 37),
        ("GOLDENROD2", 238, 180, 34),
        ("GOLDENROD3", 205, 155, 29),
        ("GOLDENROD4", 139, 105, 20),
        ("GREEN YELLOW", 173, 255, 47),
        ("GREEN", 0, 255, 0),
        ("GREEN1", 0, 255, 0),
        ("GREEN2", 0, 238, 0),
        ("GREEN3", 0, 205, 0),
        ("GREEN4", 0, 139, 0),
        ("GREENYELLOW", 173, 255, 47),
        ("GRAY", 190, 190, 190),
        ("GRAY0", 0, 0, 0),
        ("GRAY1", 3, 3, 3),
        ("GRAY10", 26, 26, 26),
        ("GRAY100", 255, 255, 255),
        ("GRAY11", 28, 28, 28),
        ("GRAY12", 31, 31, 31),
        ("GRAY13", 33, 33, 33),
        ("GRAY14", 36, 36, 36),
        ("GRAY15", 38, 38, 38),
        ("GRAY16", 41, 41, 41),
        ("GRAY17", 43, 43, 43),
        ("GRAY18", 46, 46, 46),
        ("GRAY19", 48, 48, 48),
        ("GRAY2", 5, 5, 5),
        ("GRAY20", 51, 51, 51),
        ("GRAY21", 54, 54, 54),
        ("GRAY22", 56, 56, 56),
        ("GRAY23", 59, 59, 59),
        ("GRAY24", 61, 61, 61),
        ("GRAY25", 64, 64, 64),
        ("GRAY26", 66, 66, 66),
        ("GRAY27", 69, 69, 69),
        ("GRAY28", 71, 71, 71),
        ("GRAY29", 74, 74, 74),
        ("GRAY3", 8, 8, 8),
        ("GRAY30", 77, 77, 77),
        ("GRAY31", 79, 79, 79),
        ("GRAY32", 82, 82, 82),
        ("GRAY33", 84, 84, 84),
        ("GRAY34", 87, 87, 87),
        ("GRAY35", 89, 89, 89),
        ("GRAY36", 92, 92, 92),
        ("GRAY37", 94, 94, 94),
        ("GRAY38", 97, 97, 97),
        ("GRAY39", 99, 99, 99),
        ("GRAY4", 10, 10, 10),
        ("GRAY40", 102, 102, 102),
        ("GRAY41", 105, 105, 105),
        ("GRAY42", 107, 107, 107),
        ("GRAY43", 110, 110, 110),
        ("GRAY44", 112, 112, 112),
        ("GRAY45", 115, 115, 115),
        ("GRAY46", 117, 117, 117),
        ("GRAY47", 120, 120, 120),
        ("GRAY48", 122, 122, 122),
        ("GRAY49", 125, 125, 125),
        ("GRAY5", 13, 13, 13),
        ("GRAY50", 127, 127, 127),
        ("GRAY51", 130, 130, 130),
        ("GRAY52", 133, 133, 133),
        ("GRAY53", 135, 135, 135),
        ("GRAY54", 138, 138, 138),
        ("GRAY55", 140, 140, 140),
        ("GRAY56", 143, 143, 143),
        ("GRAY57", 145, 145, 145),
        ("GRAY58", 148, 148, 148),
        ("GRAY59", 150, 150, 150),
        ("GRAY6", 15, 15, 15),
        ("GRAY60", 153, 153, 153),
        ("GRAY61", 156, 156, 156),
        ("GRAY62", 158, 158, 158),
        ("GRAY63", 161, 161, 161),
        ("GRAY64", 163, 163, 163),
        ("GRAY65", 166, 166, 166),
        ("GRAY66", 168, 168, 168),
        ("GRAY67", 171, 171, 171),
        ("GRAY68", 173, 173, 173),
        ("GRAY69", 176, 176, 176),
        ("GRAY7", 18, 18, 18),
        ("GRAY70", 179, 179, 179),
        ("GRAY71", 181, 181, 181),
        ("GRAY72", 184, 184, 184),
        ("GRAY73", 186, 186, 186),
        ("GRAY74", 189, 189, 189),
        ("GRAY75", 191, 191, 191),
        ("GRAY76", 194, 194, 194),
        ("GRAY77", 196, 196, 196),
        ("GRAY78", 199, 199, 199),
        ("GRAY79", 201, 201, 201),
        ("GRAY8", 20, 20, 20),
        ("GRAY80", 204, 204, 204),
        ("GRAY81", 207, 207, 207),
        ("GRAY82", 209, 209, 209),
        ("GRAY83", 212, 212, 212),
        ("GRAY84", 214, 214, 214),
        ("GRAY85", 217, 217, 217),
        ("GRAY86", 219, 219, 219),
        ("GRAY87", 222, 222, 222),
        ("GRAY88", 224, 224, 224),
        ("GRAY89", 227, 227, 227),
        ("GRAY9", 23, 23, 23),
        ("GRAY90", 229, 229, 229),
        ("GRAY91", 232, 232, 232),
        ("GRAY92", 235, 235, 235),
        ("GRAY93", 237, 237, 237),
        ("GRAY94", 240, 240, 240),
        ("GRAY95", 242, 242, 242),
        ("GRAY96", 245, 245, 245),
        ("GRAY97", 247, 247, 247),
        ("GRAY98", 250, 250, 250),
        ("GRAY99", 252, 252, 252),
        ("HONEYDEW", 240, 255, 240),
        ("HONEYDEW1", 240, 255, 240),
        ("HONEYDEW2", 224, 238, 224),
        ("HONEYDEW3", 193, 205, 193),
        ("HONEYDEW4", 131, 139, 131),
        ("HOTPINK", 255, 105, 180),
        ("HOTPINK1", 255, 110, 180),
        ("HOTPINK2", 238, 106, 167),
        ("HOTPINK3", 205, 96, 144),
        ("HOTPINK4", 139, 58, 98),
        ("INDIANRED", 205, 92, 92),
        ("INDIANRED1", 255, 106, 106),
        ("INDIANRED2", 238, 99, 99),
        ("INDIANRED3", 205, 85, 85),
        ("INDIANRED4", 139, 58, 58),
        ("IVORY", 255, 255, 240),
        ("IVORY1", 255, 255, 240),
        ("IVORY2", 238, 238, 224),
        ("IVORY3", 205, 205, 193),
        ("IVORY4", 139, 139, 131),
        ("KHAKI", 240, 230, 140),
        ("KHAKI1", 255, 246, 143),
        ("KHAKI2", 238, 230, 133),
        ("KHAKI3", 205, 198, 115),
        ("KHAKI4", 139, 134, 78),
        ("LAVENDER", 230, 230, 250),
        ("LAVENDERBLUSH", 255, 240, 245),
        ("LAVENDERBLUSH1", 255, 240, 245),
        ("LAVENDERBLUSH2", 238, 224, 229),
        ("LAVENDERBLUSH3", 205, 193, 197),
        ("LAVENDERBLUSH4", 139, 131, 134),
        ("LAWNGREEN", 124, 252, 0),
        ("LEMONCHIFFON", 255, 250, 205),
        ("LEMONCHIFFON1", 255, 250, 205),
        ("LEMONCHIFFON2", 238, 233, 191),
        ("LEMONCHIFFON3", 205, 201, 165),
        ("LEMONCHIFFON4", 139, 137, 112),
        ("LIGHTBLUE", 173, 216, 230),
        ("LIGHTBLUE1", 191, 239, 255),
        ("LIGHTBLUE2", 178, 223, 238),
        ("LIGHTBLUE3", 154, 192, 205),
        ("LIGHTBLUE4", 104, 131, 139),
        ("LIGHTCORAL", 240, 128, 128),
        ("LIGHTCYAN", 224, 255, 255),
        ("LIGHTCYAN1", 224, 255, 255),
        ("LIGHTCYAN2", 209, 238, 238),
        ("LIGHTCYAN3", 180, 205, 205),
        ("LIGHTCYAN4", 122, 139, 139),
        ("LIGHTGOLDENROD", 238, 221, 130),
        ("LIGHTGOLDENROD1", 255, 236, 139),
        ("LIGHTGOLDENROD2", 238, 220, 130),
        ("LIGHTGOLDENROD3", 205, 190, 112),
        ("LIGHTGOLDENROD4", 139, 129, 76),
        ("LIGHTGOLDENRODYELLOW", 250, 250, 210),
        ("LIGHTGREEN", 144, 238, 144),
        ("LIGHTGRAY", 211, 211, 211),
        ("LIGHTPINK", 255, 182, 193),
        ("LIGHTPINK1", 255, 174, 185),
        ("LIGHTPINK2", 238, 162, 173),
        ("LIGHTPINK3", 205, 140, 149),
        ("LIGHTPINK4", 139, 95, 101),
        ("LIGHTSALMON", 255, 160, 122),
        ("LIGHTSALMON1", 255, 160, 122),
        ("LIGHTSALMON2", 238, 149, 114),
        ("LIGHTSALMON3", 205, 129, 98),
        ("LIGHTSALMON4", 139, 87, 66),
        ("LIGHTSEAGREEN", 32, 178, 170),
        ("LIGHTSKYBLUE", 135, 206, 250),
        ("LIGHTSKYBLUE1", 176, 226, 255),
        ("LIGHTSKYBLUE2", 164, 211, 238),
        ("LIGHTSKYBLUE3", 141, 182, 205),
        ("LIGHTSKYBLUE4", 96, 123, 139),
        ("LIGHTSLATEBLUE", 132, 112, 255),
        ("LIGHTSLATEGRAY", 119, 136, 153),
        ("LIGHTSTEELBLUE", 176, 196, 222),
        ("LIGHTSTEELBLUE1", 202, 225, 255),
        ("LIGHTSTEELBLUE2", 188, 210, 238),
        ("LIGHTSTEELBLUE3", 162, 181, 205),
        ("LIGHTSTEELBLUE4", 110, 123, 139),
        ("LIGHTYELLOW", 255, 255, 224),
        ("LIGHTYELLOW1", 255, 255, 224),
        ("LIGHTYELLOW2", 238, 238, 209),
        ("LIGHTYELLOW3", 205, 205, 180),
        ("LIGHTYELLOW4", 139, 139, 122),
        ("LIMEGREEN", 50, 205, 50),
        ("LINEN", 250, 240, 230),
        ("MAGENTA", 255, 0, 255),
        ("MAGENTA1", 255, 0, 255),
        ("MAGENTA2", 238, 0, 238),
        ("MAGENTA3", 205, 0, 205),
        ("MAGENTA4", 139, 0, 139),
        ("MAROON", 176, 48, 96),
        ("MAROON1", 255, 52, 179),
        ("MAROON2", 238, 48, 167),
        ("MAROON3", 205, 41, 144),
        ("MAROON4", 139, 28, 98),
        ("MEDIUMAQUAMARINE", 102, 205, 170),
        ("MEDIUMBLUE", 0, 0, 205),
        ("MEDIUMORCHID", 186, 85, 211),
        ("MEDIUMORCHID1", 224, 102, 255),
        ("MEDIUMORCHID2", 209, 95, 238),
        ("MEDIUMORCHID3", 180, 82, 205),
        ("MEDIUMORCHID4", 122, 55, 139),
        ("MEDIUMPURPLE", 147, 112, 219),
        ("MEDIUMPURPLE1", 171, 130, 255),
        ("MEDIUMPURPLE2", 159, 121, 238),
        ("MEDIUMPURPLE3", 137, 104, 205),
        ("MEDIUMPURPLE4", 93, 71, 139),
        ("MEDIUMSEAGREEN", 60, 179, 113),
        ("MEDIUMSLATEBLUE", 123, 104, 238),
        ("MEDIUMSPRINGGREEN", 0, 250, 154),
        ("MEDIUMTURQUOISE", 72, 209, 204),
        ("MEDIUMVIOLETRED", 199, 21, 133),
        ("MIDNIGHTBLUE", 25, 25, 112),
        ("MINTCREAM", 245, 255, 250),
        ("MISTYROSE", 255, 228, 225),
        ("MISTYROSE1", 255, 228, 225),
        ("MISTYROSE2", 238, 213, 210),
        ("MISTYROSE3", 205, 183, 181),
        ("MISTYROSE4", 139, 125, 123),
        ("MOCCASIN", 255, 228, 181),
        ("NAVAJOWHITE", 255, 222, 173),
        ("NAVAJOWHITE1", 255, 222, 173),
        ("NAVAJOWHITE2", 238, 207, 161),
        ("NAVAJOWHITE3", 205, 179, 139),
        ("NAVAJOWHITE4", 139, 121, 94),
        ("NAVY", 0, 0, 128),
        ("NAVYBLUE", 0, 0, 128),
        ("OLDLACE", 253, 245, 230),
        ("OLIVEDRAB", 107, 142, 35),
        ("OLIVEDRAB1", 192, 255, 62),
        ("OLIVEDRAB2", 179, 238, 58),
        ("OLIVEDRAB3", 154, 205, 50),
        ("OLIVEDRAB4", 105, 139, 34),
        ("ORANGE", 255, 165, 0),
        ("ORANGE1", 255, 165, 0),
        ("ORANGE2", 238, 154, 0),
        ("ORANGE3", 205, 133, 0),
        ("ORANGE4", 139, 90, 0),
        ("ORANGERED", 255, 69, 0),
        ("ORANGERED1", 255, 69, 0),
        ("ORANGERED2", 238, 64, 0),
        ("ORANGERED3", 205, 55, 0),
        ("ORANGERED4", 139, 37, 0),
        ("ORCHID", 218, 112, 214),
        ("ORCHID1", 255, 131, 250),
        ("ORCHID2", 238, 122, 233),
        ("ORCHID3", 205, 105, 201),
        ("ORCHID4", 139, 71, 137),
        ("PALEGOLDENROD", 238, 232, 170),
        ("PALEGREEN", 152, 251, 152),
        ("PALEGREEN1", 154, 255, 154),
        ("PALEGREEN2", 144, 238, 144),
        ("PALEGREEN3", 124, 205, 124),
        ("PALEGREEN4", 84, 139, 84),
        ("PALETURQUOISE", 175, 238, 238),
        ("PALETURQUOISE1", 187, 255, 255),
        ("PALETURQUOISE2", 174, 238, 238),
        ("PALETURQUOISE3", 150, 205, 205),
        ("PALETURQUOISE4", 102, 139, 139),
        ("PALEVIOLETRED", 219, 112, 147),
        ("PALEVIOLETRED1", 255, 130, 171),
        ("PALEVIOLETRED2", 238, 121, 159),
        ("PALEVIOLETRED3", 205, 104, 137),
        ("PALEVIOLETRED4", 139, 71, 93),
        ("PAPAYAWHIP", 255, 239, 213),
        ("PEACHPUFF", 255, 218, 185),
        ("PEACHPUFF1", 255, 218, 185),
        ("PEACHPUFF2", 238, 203, 173),
        ("PEACHPUFF3", 205, 175, 149),
        ("PEACHPUFF4", 139, 119, 101),
        ("PERU", 205, 133, 63),
        ("PINK", 255, 192, 203),
        ("PINK1", 255, 181, 197),
        ("PINK2", 238, 169, 184),
        ("PINK3", 205, 145, 158),
        ("PINK4", 139, 99, 108),
        ("PLUM", 221, 160, 221),
        ("PLUM1", 255, 187, 255),
        ("PLUM2", 238, 174, 238),
        ("PLUM3", 205, 150, 205),
        ("PLUM4", 139, 102, 139),
        ("POWDERBLUE", 176, 224, 230),
        ("PURPLE", 160, 32, 240),
        ("PURPLE1", 155, 48, 255),
        ("PURPLE2", 145, 44, 238),
        ("PURPLE3", 125, 38, 205),
        ("PURPLE4", 85, 26, 139),
        ("PY_COLOR", 240, 255, 210),
        ("RED", 255, 0, 0),
        ("RED1", 255, 0, 0),
        ("RED2", 238, 0, 0),
        ("RED3", 205, 0, 0),
        ("RED4", 139, 0, 0),
        ("ROSYBROWN", 188, 143, 143),
        ("ROSYBROWN1", 255, 193, 193),
        ("ROSYBROWN2", 238, 180, 180),
        ("ROSYBROWN3", 205, 155, 155),
        ("ROSYBROWN4", 139, 105, 105),
        ("ROYALBLUE", 65, 105, 225),
        ("ROYALBLUE1", 72, 118, 255),
        ("ROYALBLUE2", 67, 110, 238),
        ("ROYALBLUE3", 58, 95, 205),
        ("ROYALBLUE4", 39, 64, 139),
        ("SADDLEBROWN", 139, 69, 19),
        ("SALMON", 250, 128, 114),
        ("SALMON1", 255, 140, 105),
        ("SALMON2", 238, 130, 98),
        ("SALMON3", 205, 112, 84),
        ("SALMON4", 139, 76, 57),
        ("SANDYBROWN", 244, 164, 96),
        ("SEAGREEN", 46, 139, 87),
        ("SEAGREEN1", 84, 255, 159),
        ("SEAGREEN2", 78, 238, 148),
        ("SEAGREEN3", 67, 205, 128),
        ("SEAGREEN4", 46, 139, 87),
        ("SEASHELL", 255, 245, 238),
        ("SEASHELL1", 255, 245, 238),
        ("SEASHELL2", 238, 229, 222),
        ("SEASHELL3", 205, 197, 191),
        ("SEASHELL4", 139, 134, 130),
        ("SIENNA", 160, 82, 45),
        ("SIENNA1", 255, 130, 71),
        ("SIENNA2", 238, 121, 66),
        ("SIENNA3", 205, 104, 57),
        ("SIENNA4", 139, 71, 38),
        ("SKYBLUE", 135, 206, 235),
        ("SKYBLUE1", 135, 206, 255),
        ("SKYBLUE2", 126, 192, 238),
        ("SKYBLUE3", 108, 166, 205),
        ("SKYBLUE4", 74, 112, 139),
        ("SLATEBLUE", 106, 90, 205),
        ("SLATEBLUE1", 131, 111, 255),
        ("SLATEBLUE2", 122, 103, 238),
        ("SLATEBLUE3", 105, 89, 205),
        ("SLATEBLUE4", 71, 60, 139),
        ("SLATEGRAY", 112, 128, 144),
        ("SNOW", 255, 250, 250),
        ("SNOW1", 255, 250, 250),
        ("SNOW2", 238, 233, 233),
        ("SNOW3", 205, 201, 201),
        ("SNOW4", 139, 137, 137),
        ("SPRINGGREEN", 0, 255, 127),
        ("SPRINGGREEN1", 0, 255, 127),
        ("SPRINGGREEN2", 0, 238, 118),
        ("SPRINGGREEN3", 0, 205, 102),
        ("SPRINGGREEN4", 0, 139, 69),
        ("STEELBLUE", 70, 130, 180),
        ("STEELBLUE1", 99, 184, 255),
        ("STEELBLUE2", 92, 172, 238),
        ("STEELBLUE3", 79, 148, 205),
        ("STEELBLUE4", 54, 100, 139),
        ("TAN", 210, 180, 140),
        ("TAN1", 255, 165, 79),
        ("TAN2", 238, 154, 73),
        ("TAN3", 205, 133, 63),
        ("TAN4", 139, 90, 43),
        ("THISTLE", 216, 191, 216),
        ("THISTLE1", 255, 225, 255),
        ("THISTLE2", 238, 210, 238),
        ("THISTLE3", 205, 181, 205),
        ("THISTLE4", 139, 123, 139),
        ("TOMATO", 255, 99, 71),
        ("TOMATO1", 255, 99, 71),
        ("TOMATO2", 238, 92, 66),
        ("TOMATO3", 205, 79, 57),
        ("TOMATO4", 139, 54, 38),
        ("TURQUOISE", 64, 224, 208),
        ("TURQUOISE1", 0, 245, 255),
        ("TURQUOISE2", 0, 229, 238),
        ("TURQUOISE3", 0, 197, 205),
        ("TURQUOISE4", 0, 134, 139),
        ("VIOLET", 238, 130, 238),
        ("VIOLETRED", 208, 32, 144),
        ("VIOLETRED1", 255, 62, 150),
        ("VIOLETRED2", 238, 58, 140),
        ("VIOLETRED3", 205, 50, 120),
        ("VIOLETRED4", 139, 34, 82),
        ("WHEAT", 245, 222, 179),
        ("WHEAT1", 255, 231, 186),
        ("WHEAT2", 238, 216, 174),
        ("WHEAT3", 205, 186, 150),
        ("WHEAT4", 139, 126, 102),
        ("WHITE", 255, 255, 255),
        ("WHITESMOKE", 245, 245, 245),
        ("YELLOW", 255, 255, 0),
        ("YELLOW1", 255, 255, 0),
        ("YELLOW2", 238, 238, 0),
        ("YELLOW3", 205, 205, 0),
        ("YELLOW4", 139, 139, 0),
        ("YELLOWGREEN", 154, 205, 50),
        ]

def getColor(name):
    """Retrieve RGB color in PDF format by name.
    Returns a triple of floats in range 0 to 1. In case of name-not-found,
    "white" is returned.
    
    """
    try:
        c = getColorInfoList()[getColorList().index(name.upper())]
        return (c[1] / 255., c[2] / 255., c[3] / 255.)
    except:
        return (1, 1, 1)