from django.shortcuts import render
from recipes.models import Skladnik,Receptura
from .dane_do_wyswietlenia import dane_do_wyswietlenia as dane
import sys
import reportlab
import io
from django.http import FileResponse,response
from reportlab.pdfgen import canvas
#============================================================
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Paragraph,Indenter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter,A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm,cm
from django.conf import settings
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, NextPageTemplate, Paragraph, PageBreak, Table, \
    TableStyle


def to_pdf(request,pk):
    receptura = Receptura.objects.get(id=int(pk))

    Skladniki = Skladnik.objects.filter(receptura_id=int(pk))
    do_tabeli=[[receptura.nazwa,receptura.date],[receptura.rodzaj,receptura.czopki_czy_globulki,receptura.ilosc_czop_glob,receptura.masa_docelowa_czop_glob]]



    print('do_tabeli',do_tabeli)
    sys.stdout.flush()
    buffer = io.BytesIO()
    test=str(pk)
    p = canvas.Canvas(buffer, pagesize=A4)
    reportlab.rl_config.TTFSearchPath.append(str(settings.BASE_DIR) + '/to_pdf')
    pdfmetrics.registerFont(TTFont('polishFont', 'polishFont.ttf'))
    p.setFont('polishFont', 32)
    p.drawString(130, 780, 'Receptura '+receptura.nazwa+' '+test)

    # ======================================tabela==============================================

    width = 500
    height = 500
    x = 30
    y=700
    #y = b - (a * 15)
    table = Table(do_tabeli, colWidths=[50 * mm, 40* mm, 40 * mm, 40 * mm])

    ts = TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.transparent), ('FONT', (0, 0), (-1, -1), 'polishFont', 13),
                     ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'TOP')])
    table.setStyle(ts)

    table.wrapOn(p, width, height)
    table.drawOn(p, x, y)
    #===========================recepta================================================================================
    x=30
    y=600
    p.setFont('polishFont', 13)
    p.drawString(x, y, 'Rp.')
    y=580
    def skladnik(skl):
        str=''
        if skl.show==True:
            str=str+skl.skladnik+' '
            if skl.aa=='on':
                str=str+' aa'
            elif skl.qs=='on':
                str=str+' qs'
            elif skl.ad=='on':
                str=str+' ad'
            elif skl.aa_ad=='on':
                str=str+' aa ad '
            str=str+' '+skl.ilosc_na_recepcie
        return str
    for i in Skladniki:
        p.drawString(x, y, skladnik(i))
        y=y-15
    x=300
    y=600
    count=1
    for i in Skladniki:
        p.setFont('polishFont', 13)
        p.drawString(x, y, str(count)+')  '+i.skladnik)
        p.line(x+250,y-5,x,y-5)
        count=count+1
        p.setFont('polishFont', 10)
        y=y-20
        p.drawString(x, y, 'dane z recepty:')
        if i.ilosc_na_recepcie!='':
            y=y-10
            p.setFont('polishFont', 11)
            p.drawString(x, y,  'jednostka na recepcie: '+i.jednostka_z_recepty+'   '+'ilość: '+ i.ilosc_na_recepcie)
        if i.producent!='0':
            y = y - 10
            p.drawString(x, y, 'producent: ' + i.producent + '   ' +'gęstość: ' + i.gestosc)
        y=y-1
        p.setLineWidth(0.25)
        p.line(x + 250, y - 5, x, y - 5)
        y=y-15
        p.drawString(x, y, 'obliczenia:')
        y=y-10
        a=0
        for j in range(len(dane[i.skladnik])):
            parametr=dane[i.skladnik][j]
            p.drawString(x, y, parametr+':'+getattr(i, parametr ))
            y=y-10



        p.setLineWidth(1)
        y=y-25

    p.showPage()
    p.save()
    buffer.seek(0)


    return FileResponse(buffer, as_attachment=True, filename='receptura.pdf')
