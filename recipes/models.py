from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

class Receptura (models.Model):
    rodzaje=(('1','Maść'),('2','czopki i globulki'),('3','receptura płynna'))
    czop_czy_glob=(('1','czopki'),('2','globulki'))
    tak_czy_nie = (('1', 'tak'), ('2', 'nie'))
    nazwa=models.CharField( max_length=30)
    date=models.DateTimeField(auto_now_add=True)
    rodzaj=models.TextField(choices=rodzaje,blank=True, null=True)
    czopki_czy_globulki=models.TextField(choices=czop_czy_glob, blank=True, null=True)
    ilosc_czop_glob = models.CharField(max_length=40, blank=True, null=True, default='')
    masa_docelowa_czop_glob = models.CharField(max_length=40, blank=True, null=True, default='')
    czy_ilosc_oleum_pomnozyc =models.TextField(choices=czop_czy_glob, blank=True, null=True)
    ilosc_masci =models.CharField(max_length=40, blank=True, null=True, default='')
    ilosc_gramow = models.CharField(max_length=40, blank=True, null=True, default='')
    owner=models.ForeignKey(User,blank = True, null = True,on_delete=models.CASCADE)
    session = models.ForeignKey(Session, null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.nazwa


class Skladnik(models.Model):
    receptura_id=models.ForeignKey(Receptura,on_delete=models.CASCADE)
    producenci = (('1', 'Hasco 4500j.m./ml'), ('2', 'Medana 50000j.m./ml'), ('3', 'Hasco 0,3g/ml'))
    skladnik = models.CharField(max_length=40)
    jednostka_z_recepty = models.CharField(max_length=40, blank=True,default='gramy')
    ilosc_na_recepcie = models.CharField(max_length=40, blank=True,null=True,default='0')
    gramy = models.CharField(max_length=40, default='0')
    mililitry = models.CharField(max_length=40, default='0')
    solutio = models.CharField(max_length=40, default='0')
    krople = models.CharField(max_length=40, default='0')
    opakowania = models.CharField(max_length=40, default='0')
    jednostki = models.CharField(max_length=40, default='0')
    gestosc = models.CharField(max_length=40, default='0')
    sztuki = models.CharField(max_length=40, default='0')
    tabletki = models.CharField(max_length=40, default='0')
    czesci = models.CharField(max_length=40, default='0')
    producent = models.CharField(max_length=40, default='0')
    aa = models.CharField(max_length=20, default='off')
    obey = models.IntegerField(null=True,default=0)
    sumg = models.IntegerField(default=0)
    aa_ad = models.CharField(max_length=20, default='off')
    aa_ad_gramy = models.CharField(max_length=40, default='0')
    show=models.BooleanField(default=True)
    dodaj_wode = models.CharField(max_length=20, default='off')
    pozadane_stezenie = models.CharField(max_length=40, blank=True,null=True,default='')
    uzyte_stezenie = models.CharField(max_length=40, blank=True,null=True,default='')
    ilosc_etanolu = models.CharField(max_length=40, blank=True,null=True,default='')
    ilosc_wody_do_etanolu = models.CharField(max_length=40, blank=True,null=True,default='0')
    qs = models.CharField(max_length=20, default='off')
    ad = models.CharField(max_length=20, default='off')
    woda_mocznik=models.CharField(max_length=40, default='0')
    UI_w_mg = models.CharField(max_length=40, default='0')
    czy_zlozyc_roztwor_ze_skladnikow_prostych = models.CharField(max_length=20, default='off')
    woda_kwas_borowy = models.CharField(max_length=40, default='0')
    ilosc_kwasu_borowego_do_roztworu = models.CharField(max_length=40, default='0')
    calkowita_ilosc_gramow_wody = models.CharField(max_length=40, default='0')
    czy_powiekszyc_mase_oleum=models.CharField(max_length=20, default='off')
    gramy_czystej_vit_e = models.CharField(max_length=20, default='0')
    gramy_roztworu=models.CharField(max_length=20, default='0')

    def __str__(self):
        return self.skladnik


    
