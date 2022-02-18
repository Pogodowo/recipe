from .tabela_etanolowa import tabela_etanolowa
from .models import Skladnik

def Przeliczanie(skladnik,pk):
    ret={}

    if skladnik=='Etanol':
        obiekt=Skladnik.objects.get(pk=pk)
        pozadane_stezenie=tabela_etanolowa[obiekt.pozadane_stezenie]
        uzyte_stezenie=tabela_etanolowa[obiekt.uzyte_stezenie]
        ilosc_etanolu_z_rec=obiekt.gramy
        if pozadane_stezenie<uzyte_stezenie:
            czysty_etanol=(float(pozadane_stezenie)/100)*float(ilosc_etanolu_z_rec)
            ilosc_etanolu=(100*float(czysty_etanol))/float(uzyte_stezenie)
            ilosc_wody=float(float(ilosc_etanolu_z_rec)-ilosc_etanolu)
            ret["ilosc_etanolu"]=str(round(ilosc_etanolu,2))
            ret["ilosc_wody_do_etanolu"] = str(round(ilosc_wody,2))
    return ret


