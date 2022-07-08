from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse,response
from django.core import serializers
from django.contrib.sessions.models import Session
from django.contrib import messages
from .lista_składników import data
import sys
from .słownik_do_tabeli import table_dict
from django.contrib.auth.decorators import login_required
from .models import Receptura,Skladnik
from .forms import RecepturaForm,CzopkiGlobulkiForm
from .obliczenia import Przeliczanie_etanolu,Kasowanie_wody,Sumowanie_wody,Sumskl,get_super
from .tabela_etanolowa import tabela_etanolowa
from .connon_fields import fields
from .wspolczynniki_wyparcia import wspolczynniki_wyparcia
from .przelWitamin import PrzeliczanieWit
from .wyswietlane_dane import wyswietlane_dane
from colorama import Fore, Style

def home (request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    print("request.session.session_key", request.session.session_key)
    sys.stdout.flush()
    return render (request,'home.html')

#@login_required
def mojeRec (request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    print("request.session.session_key", request.session.session_key)
    sys.stdout.flush()
    if request.user.is_anonymous ==False:
        moje_receptury=Receptura.objects.filter(owner=request.user).order_by('date')
    else:
        moje_receptury = Receptura.objects.filter(session=request.session.session_key).order_by('date') #request.session.get("name")

    context={'receptury':moje_receptury}
    return render(request,'mojerec.html',context)

def dodajRecForm(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    context={'fields':fields}
    return JsonResponse(context)


def dodajRec(request):
    form_czopki = CzopkiGlobulkiForm
    if request.method != 'POST':
      form=RecepturaForm

    else:
        # create a form instance and populate it with data from the request:
        form = RecepturaForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            new_pres=form.save(commit=False)
            new_pres.owner=request.user
            new_pres.save()
            return redirect('mojerec')
    context = {'form': form,'form_czopki':form_czopki}
    return render(request, 'dodajrec.html', context)

def dodawanieRecJson(request):

    if request.is_ajax():
        ilosc_receptur=0
        if request.user.is_anonymous is False:
            ilosc_receptur = len(Receptura.objects.filter(owner=request.user))
        else:
            pass

        nazwa = request.POST.get("nazwa")
        rodzaj=request.POST.get("rodzaj")
        parametryDict={}
        parametry=fields[request.POST.get('rodzaj')]
        #######################sprawdzanie czy user jest zalogowany######################################
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
        ###################################################################################################
        for i in parametry:
            if type(i) != list:
                parametryDict[i]=request.POST.get(i)
            else:
                a = request.POST.get(str(i[0]))
                parametryDict[i[0]] = a
        print('dict',parametryDict)
        sys.stdout.flush()
        this_session_rec=Receptura.objects.filter(session=request.session.session_key)
        if len(this_session_rec)>0:
            this_session_rec.delete()
        new_skl=None
        if ilosc_receptur<15 or request.user.is_anonymous is True:
            new_skl=Receptura.objects.create(owner=user,nazwa=nazwa,rodzaj=rodzaj)#Session.objects.get(session_key=request.session.session_key)
            print( 'ciekawe czy się wyprintuje dwa razy')#new_skl=Receptura.objects.create(owner=user,nazwa=nazwa,rodzaj=rodzaj)#Session.objects.get(session_key=request.session.session_key)
            sys.stdout.flush()
        else:
            parametryDict['res']='przekroczona liczba'
        if request.user.is_anonymous is True:
            new_skl.session=Session.objects.get(session_key=request.session.session_key)
        if new_skl!=None:
            for key, value in parametryDict.items():
                print('key', key,'value',value)
                sys.stdout.flush()
                setattr(new_skl, key, value)
            new_skl.save()
            print('new_skl',new_skl.id)
            sys.stdout.flush()
            # for key, value in to_updade.items():
            #     setattr(new_skl, key, value)
            new_skl.save()
            parametryDict['id']=new_skl.id
        return JsonResponse({'dict':parametryDict})
    return JsonResponse({'nie dodano skladnika': False, }, safe=False)


def ParamRecJson(request ,recId):
    parametry = serializers.serialize("python", Receptura.objects.filter(pk=int(recId)))

    parametry[0]['slownik']=table_dict
    print('parametry', parametry)
    sys.stdout.flush()
    return JsonResponse({'parametry': parametry})

#@login_required
def receptura (request,receptura_id):
    current_user=None
    session=None
    if request.user.is_authenticated:
        current_user = request.user
    else:
        session = request.session.session_key
    try:
        receptura=Receptura.objects.get(id=receptura_id)
        if request.user.is_authenticated and receptura in Receptura.objects.filter(owner=current_user):
            context={'receptura':receptura}
            return render(request,'receptura.html',context)
        elif  request.user.is_authenticated is False and receptura in Receptura.objects.filter(session=session):
            context = {'receptura': receptura}
            return render(request, 'receptura.html', context)
        else:
            return render(request, '404.html',)
    except Receptura.DoesNotExist:
        return render(request, '404.html', )

def formJson (request,skl):
    #skl zawiera tutaj nazwę składnika i id receptury
    ind=skl.index('&')
    formData={}
    datadict=data[skl[:ind]]
    all =Skladnik.objects.filter(receptura_id=int(skl[ind+1:]))
    last=all.last()
    # sprawdzanie czy receptura zawiera ad lub aa_ad##########################################
    jest_ad = False
    skladnik_z_ad = None
    jest_aa_ad = False
    skladnik_z_aa_ad = None
    for i in all:
        if i.ad == 'on':
            jest_ad = True
            skladnik_z_ad = i
        elif i.aa_ad == 'on':
            jest_aa_ad = True
            skladnik_z_aa_ad = i
    ############# kończenie receptury jeżeli zawiera składnik z ad lun aa ad ####################################
    if  (skladnik_z_ad!= None and jest_ad ==True) or (skladnik_z_aa_ad!= None and jest_aa_ad ==True):
            datadict=['receptura zakończona. Ostatni skladnik zawiera ad lub aa ad. Aby konynuować musisz usunąć bądź edytować ostatni skladnik ']


    for i in all:
        if i.skladnik ==skl[:ind] and i.show==True:
            datadict=['ten składnik już został dodany']

    formData['datadict']=datadict
    formData['table_dict']=table_dict
    #context = {'datadict': datadict}
    context={ 'formData':formData}
    return JsonResponse(context)


def dodajsklJson (request,sklId):
    if request.is_ajax():
        previous_skl = Skladnik.objects.filter(receptura_id=int(sklId)).last()
        new_skl=None
        dodanySkladnik=request.POST.get("skladnik")
        receptura=Receptura.objects.get(id=int(sklId))
        ilosc=request.POST.get("ilosc_na_recepcie")
        all = Skladnik.objects.filter(receptura_id=int(sklId))
        to_updade={}
        if len(all)<11:
            ###########sprawdzanie czy jest woda################
            woda=None
            jestwoda = False
            for i in all:
                if i.skladnik == 'Woda destylowana':
                    jestwoda = True
                    woda = i
            mocznik = None
            jestmocznik = False
            for i in all:
                if i.skladnik == 'Mocznik':
                    jestmocznik = True
                    mocznik = i

            ################################################################################
            if dodanySkladnik=='Woda destylowana':
                if jestwoda==False:
                    new_skl = Skladnik.objects.create(skladnik=dodanySkladnik, receptura_id=receptura,
                                                      ilosc_na_recepcie=ilosc)

                    jestwoda=True
                else:
                    woda.delete()
                    new_skl = Skladnik.objects.create(skladnik=dodanySkladnik, receptura_id=receptura,
                                                      ilosc_na_recepcie=ilosc)

                    #woda.save()

            else:
                new_skl=Skladnik.objects.create(skladnik=dodanySkladnik,receptura_id=receptura,ilosc_na_recepcie=ilosc,)

            if new_skl!=None:
                to_updade={'skladnik' :new_skl.skladnik, 'jednostka_z_recepty':new_skl.jednostka_z_recepty}
                for i in data[dodanySkladnik]:
                    if type(i)!=list:
                        a=request.POST.get(str(i))
                        to_updade[i]=a
                    else:
                        a = request.POST.get(str(i[0]))
                        to_updade[i[0]] = a

                #==========wstawianie gramów==========================
                if to_updade['jednostka_z_recepty']=='gramy':
                    to_updade['gramy']=ilosc
                if receptura.ilosc_czop_glob!='' and new_skl.ilosc_na_recepcie!='':
                    if to_updade['jednostka_z_recepty']=='gramy':
                        to_updade['gramy']=str(round(float(ilosc)*float(receptura.ilosc_czop_glob),3))
                #do wywalenia jak popraeię obliczenia witamin
                    elif to_updade['jednostka_z_recepty']=='solutio':
                        to_updade['gramy']=str(round(float(ilosc)*float(receptura.ilosc_czop_glob),3))

                #=====================================================
                if 'aa_ad' in to_updade:
                    if to_updade['aa_ad']=='on':
                        to_updade['aa_ad_gramy']=ilosc

                #=================przelicanie witamin======================================
                print('new_skl.skladnik',new_skl.skladnik)
                sys.stdout.flush()
                if (new_skl.skladnik=='Vitaminum A' or new_skl.skladnik=='witamina E' or new_skl.skladnik=='Oleum Menthae piperitae' or new_skl.skladnik=='Nystatyna'or new_skl.skladnik=='Mocznik') and to_updade['ilosc_na_recepcie']!='' :
                   to_updade=PrzeliczanieWit(dodanySkladnik,to_updade,receptura.rodzaj,receptura.ilosc_czop_glob)
                print('to_ptade bo nie wiem gdzie te gramy',to_updade)
                sys.stdout.flush()

                for key, value in to_updade.items():
                    setattr(new_skl, key, value)
                new_skl.save()
                print('new_skl.gramy bo nie wiem gdzie te gramy', new_skl.gramy)
                sys.stdout.flush()
                ####################dodawanie aut aa bo w uptade Table trzeba było odświerzać to dodaję tu
                if previous_skl != None and previous_skl.gramy == '' and new_skl.gramy != '' and new_skl.ilosc_na_recepcie.isnumeric() :
                    new_skl.aa = 'on'
                    new_skl.save()
                #############zamienianie ad na aa_ad jeżeli nie podano wartości w poprzednim składniku############
                if previous_skl!=None and previous_skl.ilosc_na_recepcie == '' and previous_skl.show==True and new_skl.ad=='on':
                    new_skl.ad='off'
                    new_skl.aa_ad='on'
                    new_skl.save()

        else:
            to_updade['za_duzo_skladnikow']='za_duzo_skladnikow'

        return JsonResponse({'tabela':to_updade})
    return JsonResponse({'nie dodano skladnika': False, }, safe=False)


#@login_required
def aktualizujTabela (request,sklId):
    gramy_po_podziale = 0
    alerty={'alert': ''}
    skl_previous_aa_ad=None
    previous_skl=None
    if len(Skladnik.objects.filter(receptura_id=int(sklId)))>1:
        previous_skl = Skladnik.objects.filter(receptura_id=int(sklId)).order_by('-pk')[1]

    last=None
    last=Skladnik.objects.filter(receptura_id=int(sklId)).last()
    receptura = Receptura.objects.get(id=int(sklId))
    #############zamienianie ad na aa_ad jeżeli nie podano wartości w poprzednim składniku############
    if previous_skl != None and previous_skl.ilosc_na_recepcie == '' and previous_skl.show == True and last.ad == 'on':
        last.ad = 'off'
        last.aa_ad = 'on'
        last.save()
    ###########################################################################################################
    if last!=None:
        if last.jednostka_z_recepty == 'gramy':

            last.gramy = last.ilosc_na_recepcie
            last.save()
        if receptura.ilosc_czop_glob != '' and last.ilosc_na_recepcie != '':
            if last.jednostka_z_recepty == 'gramy':
                last.gramy = str(round(float(last.gramy) * float(receptura.ilosc_czop_glob), 3))
                last.save()
        print('last.skladnik',last.skladnik,'last,gramy',last.gramy,)
        g = last.gramy
        l = last.pk
        all = Skladnik.objects.filter(receptura_id=int(sklId))
    ################sprawdzanie czy jest woda i roztw kwasu borowegoi etanol i inne składniki################################
        jest_roztw_kw=False
        roztw_kw=None
        woda = None
        jestwoda = False
        etanol = None
        jestetanol = False
        mocznik = None
        jestmocznik = False
        for i in all:

            if i.skladnik == 'Woda destylowana':
                jestwoda = True
                woda = i
            elif i.skladnik=='3% roztwór kwas borowy':
                jest_roztw_kw = True
                roztw_kw = i
            elif i.skladnik=='Etanol':
                jestetanol = True
                etanol = i
            elif i.skladnik=='Mocznik':
                jestmocznik = True
                mocznik = i
            ####################k
            #sprawdzanie czy receptura zawiera ad lub aa_ad##########################################
        jest_ad=False
        skladnik_z_ad=None
        jest_aa_ad = False
        skladnik_z_aa_ad = None
        for i in all:
            if i.ad == 'on':
                jest_ad = True
                skladnik_z_ad = i
            elif i.aa_ad == 'on':
                jest_aa_ad = True
                skladnik_z_aa_ad = i

        ########################################################################################
        print('lastTutaj', last)
        if  skladnik_z_aa_ad != None and skladnik_z_aa_ad.aa=='on':
            skladnik_z_aa_ad.aa='off'
            skladnik_z_aa_ad.save()
        ###################### nowe aa################################################
        print('if jestwoda==True:1', jestwoda == True)
        if jestwoda == True:
            print('woda.gramy Tutaj', woda.gramy,'woda.obey',woda.obey)
        print("last.aa = 'on'", last.aa == 'on')
        if len(all) > 1:
            ind=0
            for el in all:
                print("el.aa = 'on'", el.aa)
                if el.aa == 'on':
                    print('Czy konie mnie słyszą', el.aa == 'on',el.skladnik)

                    sys.stdout.flush()
                    collection=all[:ind]
                    print('collection',collection)
                    sys.stdout.flush()
                    for obj in collection[::-1]:
                        print('obj', obj)
                        sys.stdout.flush()
                        if obj.gramy == '' or obj.obey == el.pk:
                            obj.gramy = el.gramy
                            obj.obey = el.pk
                            obj.save()
                        else:
                            break
                ind=ind+1


        ####################################################
        ########### kasowanie ilości g po usunięciu skłądnika z aa#########################
        for el in all:

            if all.filter(pk=el.obey).exists():
                pass
            else:
                if el.obey != None and el.obey!=0 :
                    el.gramy = ''
                    el.obey = None
                    el.save()
        print('if jestwoda==True:2', jestwoda == True)
        if jestwoda == True:
            print('woda.gramy Tutaj', woda.gramy,'woda.obey',woda.obey)
        ######################uwzględnianie ad#############################################
        if jest_ad ==True and skladnik_z_ad != None:
            skladnik_z_ad .aa_ad_gramy = skladnik_z_ad.ilosc_na_recepcie
            skladnik_z_ad .save()
            print('skladnik_z_ad .aa_ad_gramy', skladnik_z_ad .aa_ad_gramy)
            sys.stdout.flush()
            if skladnik_z_ad.ilosc_na_recepcie=='' or float(skladnik_z_ad.ilosc_na_recepcie)<Sumskl(sklId):
                alerty['alert']='ilość dodanego składnika z ad musi być większ niż masa dotychczasowych skladników'
                skladnik_z_ad.delete()
                jest_ad = False
            else:
                skladnik_z_ad.gramy = str(float(skladnik_z_ad.ilosc_na_recepcie) - Sumskl(sklId))
                gramy_po_podziale=skladnik_z_ad.gramy
                skladnik_z_ad.save()
        elif jest_ad ==True and skladnik_z_ad != None and skladnik_z_ad.ad == 'on' and skladnik_z_ad.aa == 'on':
            skladnik_z_ad.aa_ad = 'on'
            skladnik_z_ad.aa = 'off'
            skladnik_z_ad.ad = 'off'
            jest_ad = False
            jest_aa_ad = True
            skladnik_z_aa_ad = skladnik_z_ad
            skladnik_z_ad.aa_ad_gramy = skladnik_z_ad.ilosc_na_recepcie
            skladnik_z_ad.save()


        ################uwzględnianie aa ad#####################################################

        a = 0

        if jest_aa_ad==True and  skladnik_z_aa_ad!=None :  # tutaj sprawdzam na ile składników trzeba podzielić ilość gramów z aa ad
            aa_ad_gramy='0'
            skladnik_z_aa_ad.gramy = ''
            skladnik_z_aa_ad.save()

            for el in all.order_by('-pk'):  # order_by('-pk')
                print('el.gramy:', el.gramy,'el.skladnik:', el.skladnik, 'el.obey!=None', el.obey != None)
                sys.stdout.flush()
                if  el.ilosc_na_recepcie == '' or el.aa_ad=='on' and el.show is True:
                    a = a + 1
                elif el.show is False:
                    pass
                else:
                    break
                print('dzelnik', a)
                sys.stdout.flush()


            reversed_list=all.order_by('-pk')
            if skladnik_z_aa_ad.ilosc_na_recepcie!='':
                skladnik_z_aa_ad.aa_ad_gramy=skladnik_z_aa_ad.ilosc_na_recepcie
                skladnik_z_aa_ad.save()
                gramy_po_podziale=str(round((float(skladnik_z_aa_ad.aa_ad_gramy) - Sumskl(sklId)) / a, 2))
            print('gramy_po_podziale', gramy_po_podziale,'Sumskl(sklId)',Sumskl(sklId),'a',a)
            sys.stdout.flush()
            print(' reversed_list[0]',  reversed_list[0].skladnik)
            sys.stdout.flush()
            print('a', a)
            sys.stdout.flush()
            b=0


            while b<a:
                print(' reversed_list[b].skladnik',reversed_list[b].skladnik )
                print('gramy_po_podziale', gramy_po_podziale)
                sys.stdout.flush()
                ob=reversed_list[b]
                if ob.show==True:
                    ob.gramy=gramy_po_podziale
                    ob.obey=skladnik_z_aa_ad.pk
                    ob.save()
                    if ob.skladnik=='Etanol':
                        etanol.gramy=gramy_po_podziale
                        etanol.save()
                    elif ob.skladnik=='3% roztwór kwas borowy' and roztw_kw!=None:
                        roztw_kw.gramy=gramy_po_podziale
                        roztw_kw.save()
                    elif ob.skladnik=='Woda destylowana' and woda!=None:
                        woda.gramy=gramy_po_podziale
                        woda.save()
                    print(' ob.skladnik', ob.skladnik)
                    print('ob.gramy', ob.gramy)
                    b = b + 1
                elif ob.show is False:
                    b=b+1
                    a=a+1
                else:
                    b=b+1


        print('Sumskl(sklId)',Sumskl(sklId))
        sys.stdout.flush()
        #########################uwzględnianie mocznika i wody##############################
        receptura = Receptura.objects.get(id=int(sklId))

        if jestmocznik==True and mocznik.dodaj_wode=='on':
            mocznik.woda_mocznik = str(float(mocznik.ilosc_na_recepcie) * 1.5)
            mocznik.save()
            if jestwoda == True:
                woda.woda_mocznik = str(float(mocznik.ilosc_na_recepcie)*1.5)
                woda.save()
            elif jestwoda==False:
                Skladnik.objects.create(receptura_id=receptura,skladnik='Woda destylowana',show=False,woda_mocznik=mocznik.woda_mocznik)
                Sumowanie_wody(sklId,None)
                jestwoda=True
        Kasowanie_wody(sklId)

        #########################komponowanie roztworu kwasu bornego z kwasu i wody##############################
        if jest_roztw_kw!=False and roztw_kw!=None and (roztw_kw.gramy=='' or roztw_kw.gramy=='0'):
            if roztw_kw.czy_zlozyc_roztwor_ze_skladnikow_prostych == 'on':
                roztw_kw.woda_kwas_borowy = '0'
                roztw_kw.ilosc_kwasu_borowego_do_roztworu = '0'
                roztw_kw.save()
        if jest_roztw_kw!=False and roztw_kw!=None and roztw_kw.gramy!='':
            if  roztw_kw.czy_zlozyc_roztwor_ze_skladnikow_prostych=='on':
                roztw_kw.woda_kwas_borowy=str(round(float(roztw_kw.gramy)-float(roztw_kw.gramy)*0.03,2))
                roztw_kw.ilosc_kwasu_borowego_do_roztworu=str(round(float(roztw_kw.gramy)*0.03,2))
                roztw_kw.save()
                print('jestwoda==True', jestwoda)
                sys.stdout.flush()
                if jestwoda==True and woda!=None:
                    woda.woda_kwas_borowy=roztw_kw.woda_kwas_borowy
                    woda.save()
                elif jestwoda==False:
                    woda=Skladnik.objects.create(receptura_id=receptura,skladnik='Woda destylowana',show=False,woda_kwas_borowy=roztw_kw.woda_kwas_borowy)
                    jestwoda = True

                    #Sumowanie_wody(sklId)
                print('jestwoda==True2', jestwoda)


        ##############usuwanie kwasu bornego po usunięciu roztworu penie ten fragment do wywalenia################################
        print('lastTeraz',last.skladnik)
        sys.stdout.flush()
        if roztw_kw!=None and roztw_kw.czy_zlozyc_roztwor_ze_skladnikow_prostych == 'off' and jestwoda==True:
            print('dupa  z tą wodą')
            roztw_kw.woda_kwas_borowy='0'
            roztw_kw.ilosc_kwasu_borowego_do_roztworu='0'
            woda.woda_kwas_borowy='0'
            roztw_kw.save()
            woda.save()

        #####################obliczenia###################################################################


        if jestetanol==True and etanol !=None :
            to_updade = Przeliczanie_etanolu(etanol.skladnik, etanol.pk,etanol.gramy)
            print('etanol.gramy', etanol.gramy)
            sys.stdout.flush()
            if to_updade['ilosc_etanolu']=='dupa':#jeżeli stężenie użytego jest mniejsz niż potrzebnego
                alerty['alert'] = 'Stężenie Etanolu na recepcie musi być mniejsze niż posiadanego do sporządzenia roztworu'
                etanol.delete()
                jestetanol = False
            else:
                etanol.ilosc_etanolu=to_updade["ilosc_etanolu"]
                etanol.ilosc_wody_do_etanolu=to_updade["ilosc_wody_do_etanolu"]
                etanol.save()

            if jestwoda==True and woda!=None:
                woda.ilosc_wody_do_etanolu=etanol.ilosc_wody_do_etanolu
                woda.save()

            elif jestwoda==False:
                woda = Skladnik.objects.create(receptura_id=receptura,skladnik='Woda destylowana',show=False,ilosc_wody_do_etanolu=etanol.ilosc_wody_do_etanolu)
                jestwoda =True
            etanol.save()

        if jestetanol==False and jestwoda==True and woda!= None:
            woda.ilosc_wody_do_etanolu='0'


        if last.skladnik == 'Oleum Cacao':
            obiekt = Skladnik.objects.get(pk=last.pk)
            receptura = Receptura.objects.get(pk=obiekt.receptura_id.pk)
            print('receptura', receptura)
            sys.stdout.flush()
            if obiekt.qs == 'on':
                a = 0.0
                for el in all:
                    if el.skladnik!='Oleum Cacao':
                        a=a+float(el.gramy)*wspolczynniki_wyparcia[el.skladnik]
                last.gramy=str(round(float(receptura.masa_docelowa_czop_glob)*float(receptura.ilosc_czop_glob) - a,3 ))
                last.save()
            elif obiekt.ad == 'on':
                last.gramy=str(round(float(last.ilosc_na_recepcie)*float(receptura.ilosc_czop_glob)-Sumskl(sklId),3 ))
                last.save()
            if obiekt.czy_powiekszyc_mase_oleum == 'on':
                last.gramy = str(float(last.gramy)+float(receptura.masa_docelowa_czop_glob))
                last.save()
       
        Sumowanie_wody(sklId,gramy_po_podziale)
        Kasowanie_wody(sklId)
        objects = serializers.serialize("python", Skladnik.objects.filter(receptura_id=int(sklId)))
        parametry = serializers.serialize("python", Receptura.objects.filter(pk=int(sklId)))
        datax={}
        datax['slownik'] = table_dict
        datax['parametry']=parametry[0]
        datax['objects']=objects
        datax['alerty']=alerty
        datax['wyswietlane_dane']=wyswietlane_dane(objects)

    else:
        datax = {}
        parametry = serializers.serialize("python", Receptura.objects.filter(pk=int(sklId)))
        datax['slownik'] = table_dict
        datax['parametry'] = parametry[0]
        datax['objects'] = None
        datax['alerty'] = None
        #datax['wyswietlane_dane'] = wyswietlane_dane(objects)
    return JsonResponse({'tabela_zbiorcza':datax})


def delSkl (request,id):
    deletedElement=Skladnik.objects.filter(pk=id)
    print('deletedElement',deletedElement)
    sys.stdout.flush()
    skl=Skladnik.objects.get(pk=id)
    all = Skladnik.objects.filter(receptura_id=skl.receptura_id)
    ################sprawdzanie czy jest woda ################################
    woda = None
    jestwoda = False
    for i in all:
        if i.skladnik == 'Woda destylowana':
            jestwoda = True
            woda = i
    ########################################################################################
    if skl.skladnik=='Mocznik':
        if jestwoda==True and woda:
            woda.woda_mocznik='0'
            woda.save()
    if skl.skladnik=='Etanol':
        if jestwoda==True and woda:
            woda.ilosc_wody_do_etanolu='0'
            woda.save()
    if skl.skladnik=='3% roztwór kwas borowy':
        if jestwoda==True and woda:
            woda.woda_kwas_borowy='0'
            woda.save()

    ####################################################################
    Kasowanie_wody(id)
    Sumowanie_wody(id,None)
    # if jestwoda == True and woda != None:
    #     if woda.ilosc_na_recepcie == '0' and woda.ilosc_wody_do_etanolu == '0' and woda.woda_mocznik == '0' and woda.woda_kwas_borowy == '0':
    #         woda.delete()

    ####################################################################
    response=serializers.serialize("python", deletedElement)
    deletedElement.delete()
    print('response', response)
    sys.stdout.flush()
    return JsonResponse({'response':response})

def editFormJson(request,skl):
    # skl zawiera tutaj nazwę składnika i id receptury
    ind = skl.index('&')
    datadict = {'form':data[skl[:ind]],'values':{}}
    receptura = Skladnik.objects.filter(receptura_id=int(skl[ind + 1:]))
    lastEdit = Skladnik.objects.filter(receptura_id=int(skl[ind + 1:])).last().skladnik
    lista_el_do_edycji=[]
    if skl[:ind]!=lastEdit:
        print('skl[:ind]!=lastEdit', skl[:ind]!=lastEdit)
        sys.stdout.flush()
        for i in data[skl[:ind]]:
            print('i do edycji', i)
            if i not in ['aa','ad','aa_ad','qs','dodaj_wode','czy_zlozyc_roztwor_ze_skladnikow_prostych']:
                print('znalazłem')
                lista_el_do_edycji.append(i)
    else:
        lista_el_do_edycji=data[skl[:ind]]
    # for i in data[skl[:ind]]:
    #     if i not in ['aa','ad','aa_ad']:
    #         print('znalazłem')
    #         lista_el_do_edycji.append(i)
    datadict['form']=lista_el_do_edycji



    for i in receptura:
        if i.skladnik == skl[:ind] and i.show == True:
            print('znalazłem składnik',i)
            sys.stdout.flush()
            for j in lista_el_do_edycji:
                print('j do edycji', j)
                sys.stdout.flush()
                if type(j)==list:
                    j=j[0]
                    datadict['values'][str(j)] = getattr(i, j)
                else:
                    datadict['values'][str(j)] = getattr(i, j)
    print('datadict', datadict)
    sys.stdout.flush()
    context = {'datadict': datadict,'slownik' : table_dict}
    return JsonResponse(context)

def edytujsklJson (request,sklId):
    if request.is_ajax():
        ind = sklId.index('&')
        dodanySkladnik=request.POST.get("skladnik")
        ilosc=request.POST.get("ilosc_na_recepcie")
        receptura = Receptura.objects.get(pk=int(sklId[ind + 1:]))
        print('int(sklId[ind + 1:])', int(sklId[ind + 1:]))
        sys.stdout.flush()
        sklreceptury = Skladnik.objects.filter(receptura_id=int(sklId[ind + 1:]))
        print('edycjareceptura', sklreceptury)
        sys.stdout.flush()
        elmenty_do_imputa = {}
        for i in sklreceptury:
            if i.skladnik == sklId[:ind] and i.show == True:
                print('znalazłem składnik', i)
                to_edit = {'skladnik': i.skladnik, 'jednostka_z_recepty': i.jednostka_z_recepty}
                for j in data[dodanySkladnik]:
                    if type(j) != list:
                        if str(j) in request.POST:
                            a = request.POST.get(str(j))
                            to_edit[j] = a
                        else:
                            pass

                    else:
                        if str(j[0]) in request.POST:
                            a = request.POST.get(str(j[0]))
                            to_edit[j[0]] = a
                        else:
                            pass
                    # if receptura['rodzaj']=='czopki_i_globulki':
                    #     sklreceptury[sklreceptury['jednostka_z_recepty']]=str(float(sklreceptury['ilosc_na_recepcie'])*float(receptura['ilosc_czop_glob']))
                print('to_edit', to_edit)
                sys.stdout.flush()
                # ==========wstawianie gramów==========================
                if to_edit['jednostka_z_recepty'] == 'gramy':
                    to_edit['gramy'] = ilosc
                    #to_edit['gramy'] = to_edit['ilosc_na_recepcie']
                print('recepturarrr', receptura)
                sys.stdout.flush()
                if receptura.rodzaj == 'czopki_i_globulki' and to_edit['ilosc_na_recepcie']!='':
                    to_edit[to_edit['jednostka_z_recepty']] = str(round(
                    float(to_edit['ilosc_na_recepcie']) * float(receptura.ilosc_czop_glob),3))


                # =====================================================
                if 'aa_ad' in to_edit:
                    to_edit['aa_ad_gramy'] = to_edit['gramy']
                # if 'dodaj_wode' in to_updade:
                #     to_updade['aa_ad_gramy']=to_updade['gramy']
                # to_updade=Przeliczanie(dodanySkladnik,to_updade)
                if to_edit['skladnik'] == 'Vitaminum A' or to_edit['skladnik'] == 'witamina E' or to_edit['skladnik'] == 'Oleum Menthae piperitae' or to_edit['skladnik'] == 'Nystatyna':
                    to_edit = PrzeliczanieWit(to_edit['skladnik'], to_edit, receptura.rodzaj, receptura.ilosc_czop_glob)
                    print('to_edit', to_edit, 'to_updade,rodzaj,ilosc', 'receptura',sklreceptury, receptura.rodzaj, receptura.ilosc_czop_glob)
                    sys.stdout.flush()

                for key, value in to_edit.items():
                    setattr(i, key, value)
                i.save()
                return JsonResponse({'tabela': to_edit})


    return JsonResponse({'nie dodano skladnika': False, }, safe=False)


def slownikJson(request):
    #response = serializers.serialize("python", deletedElement)
    return JsonResponse({'table_dict': table_dict})


def usunRec (request,id):
    deletedElement=Receptura.objects.filter(pk=id)
    print('deletedElement',deletedElement)
    sys.stdout.flush()
    deletedElement.delete()
    t=[]
    return redirect('mojerec')



def obliczeniaOlCac(request,sklId):
    skladniki = Skladnik.objects.filter(receptura_id=int(sklId))
    receptura = Receptura.objects.get(id=int(sklId))
    print('receptura Obl Ol', receptura)
    sys.stdout.flush()
    print('skladniki', skladniki)
    sys.stdout.flush()
    obl=''
    a='dddd'
    temp='$8^{a}'
    for i in skladniki:
        if i.skladnik!='Oleum Cacao':
            obl = obl +  " + "+i.gramy +'g. '+ get_super('('+'ilosc gramow '+i.skladnik+ ')') + " x " +str(wspolczynniki_wyparcia[i.skladnik])+  ' '+get_super('('+'wspolczynnik wypacia '+i.skladnik+ ')')
    obl = obl + ' = '
    for i in skladniki:
        if i.skladnik!='Oleum Cacao':
            obl = obl +str(round(float(i.gramy)*float(wspolczynniki_wyparcia[i.skladnik]),3)) + get_super('('+'ilosc gramow '+i.skladnik + " x " +'wspolczynnik wypacia '+i.skladnik +')')+' + '
    obl = obl[:-3]
    obl= obl +' = '
    for i in skladniki:
        if i.skladnik == 'Oleum Cacao' and i.czy_powiekszyc_mase_oleum == 'off':
            obl = obl + i.gramy+'.g'
        elif i.skladnik == 'Oleum Cacao' and i.czy_powiekszyc_mase_oleum == 'on':
            obl = obl + str(float(i.gramy)-float(receptura.masa_docelowa_czop_glob))+'.g + '+receptura.masa_docelowa_czop_glob+'g.'+get_super('(masa dodatkowego czopka/globulki)') +'= '+i.gramy+'g.'



    return JsonResponse({'tabela': obl[3:]})

def obliczeniaEt(request,sklId):
    etanol=None
    skladniki = Skladnik.objects.filter(receptura_id=int(sklId))
    for i in skladniki:
        if i.skladnik=='Etanol':
            etanol=i

    receptura = Receptura.objects.get(id=int(sklId))
    obl=''
    obl+='Ilość potrzebnych gramów etanolu '+ etanol.pozadane_stezenie+'° wynosi '+etanol.gramy+' \n'
    obl+='Stężenie etanolu jakim dysponujeny  wynosi '+etanol.uzyte_stezenie+'° t.j. '+ tabela_etanolowa[etanol.uzyte_stezenie]+'% w stężeniu wagowym'+'\n'
    obl+=etanol.gramy+' x '+tabela_etanolowa[etanol.pozadane_stezenie]+'               '+etanol.uzyte_stezenie+' \n'
    obl += 'to be continued'+' \n'

    return JsonResponse({'tabela': obl})