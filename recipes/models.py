from django.db import models
from django.contrib.auth.models import User

class Receptura (models.Model):
    rodzaje=(('1','Maść'),('2','czopki i globulki'),('3','receptura płynna'))
    nazwa=models.CharField( max_length=30)
    date=models.DateTimeField(auto_now_add=True)
    rodzaj=models.TextField(choices=rodzaje,blank=True, null=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.nazwa


class Skladnik(models.Model):
    receptura_id=models.ForeignKey(Receptura,on_delete=models.CASCADE)
    producenci = (('1', 'Hasco 4500j.m./ml'), ('2', 'Medana 50000j.m./ml'), ('3', 'Hasco 0,3g/ml'))
    skladnik = models.CharField(max_length=40)
    jednostka_z_recepty = models.CharField(max_length=40, blank=True,default='gramy')
    ilosc_na_recepcie = models.CharField(max_length=40, blank=True,null=True,default='')
    gramy = models.CharField(max_length=40, default='0')
    mililitry = models.CharField(max_length=40, default='0')
    krople = models.CharField(max_length=40, default='0')
    opakowania = models.CharField(max_length=40, default='0')
    jednostki = models.CharField(max_length=40, default='0')
    sztuki = models.CharField(max_length=40, default='0')
    tabletki = models.CharField(max_length=40, default='0')
    czesci = models.CharField(max_length=40, default='0')
    producent = models.TextField(choices=producenci, blank=True, null=True)
    aa = models.CharField(max_length=20, default='off')
    obey = models.IntegerField(null=True)
    sumg = models.IntegerField(default=0)
    aa_ad = models.CharField(max_length=20, default='off')
    aa_ad_gramy = models.CharField(max_length=40, default='')
    show=models.BooleanField(default=True)
    dodaj_wode = models.CharField(max_length=20, default='off')
    def __str__(self):
        return self.skladnik
