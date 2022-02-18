from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse,response
from django.core import serializers
from .lista_składników import data
import sys
from .słownik_do_tabeli import table_dict

from .models import Receptura,Skladnik
from .forms import RecepturaForm,CzopkiGlobulkiForm
from .obliczenia import Przeliczanie
from .connon_fields import fields

def home (request):
    return render (request,'home.html')


def mojeRec (request):
    moje_receptury=Receptura.objects.filter(owner=request.user).order_by('date')
    context={'receptury':moje_receptury}
    return render(request,'mojerec.html',context)

def dodajRecForm(request):
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
        nazwa = request.POST.get("nazwa")
        dict={}
        parametry=fields[request.POST.get('rodzaj')]
        for i in parametry:
            if type(i) != list:
                dict[i]=request.POST.get(i)
            else:
                a = request.POST.get(str(i[0]))
                dict[i[0]] = a
        print('dict',dict)
        sys.stdout.flush()
        new_skl=Receptura.objects.create(owner=request.user,nazwa=nazwa)
        for key, value in dict.items():
            setattr(new_skl, key, value)
        new_skl.save()

        # for key, value in to_updade.items():
        #     setattr(new_skl, key, value)
        new_skl.save()
        return JsonResponse({'dict':dict})
    return JsonResponse({'nie dodano skladnika': False, }, safe=False)




def receptura (request,receptura_id):
    receptura=Receptura.objects.get(id=receptura_id)
    context={'receptura':receptura}
    return render(request,'receptura.html',context)

def formJson (request,skl):
    #skl zawiera tutaj nazwę składnika i id receptury
    ind=skl.index('&')
    formData={}
    datadict=data[skl[:ind]]
    receptura =Skladnik.objects.filter(receptura_id=int(skl[ind+1:]))
    for i in receptura:
        if i.skladnik ==skl[:ind] and i.show==True:
            datadict=['ten składnik już został dodany']

    formData['datadict']=datadict
    formData['table_dict']=table_dict
    #context = {'datadict': datadict}
    context={ 'formData':formData}
    return JsonResponse(context)


def dodajsklJson (request,sklId):
    if request.is_ajax():
        dodanySkladnik=request.POST.get("skladnik")
        receptura=Receptura.objects.get(id=int(sklId))
        ilosc=request.POST.get("ilosc_na_recepcie")

        new_skl=Skladnik.objects.create(skladnik=dodanySkladnik,receptura_id=receptura,ilosc_na_recepcie=ilosc)


        to_updade={'skladnik' :new_skl.skladnik, 'jednostka_z_recepty':new_skl.jednostka_z_recepty}
        for i in data[dodanySkladnik]:
            if type(i)!=list:
                a=request.POST.get(str(i))
                to_updade[i]=a
            else:
                a = request.POST.get(str(i[0]))
                to_updade[i[0]] = a
        print('to_update',to_updade)
        sys.stdout.flush()
        #==========wstawianie gramów==========================
        if to_updade['jednostka_z_recepty']=='gramy':
            to_updade['gramy']=ilosc
        #=====================================================
        if 'aa_ad' in to_updade:
            to_updade['aa_ad_gramy']=to_updade['gramy']
        # if 'dodaj_wode' in to_updade:
        #     to_updade['aa_ad_gramy']=to_updade['gramy']
        #to_updade=Przeliczanie(dodanySkladnik,to_updade)
        for key, value in to_updade.items():
            setattr(new_skl, key, value)
        new_skl.save()
        return JsonResponse({'tabela':to_updade})
    return JsonResponse({'nie dodano skladnika': False, }, safe=False)



def aktualizujTabela (request,sklId):
    last=Skladnik.objects.filter(receptura_id=int(sklId)).last()
    g = last.gramy
    l = last.pk
    all = Skladnik.objects.filter(receptura_id=int(sklId))
    jestwoda = None
################sprawdzanie czy jest woda i mocznik################################
    woda = False
    for i in all:
        if i.skladnik=='Woda destylowana':
            woda =True
            jestwoda=i
    print('woda', woda)
    sys.stdout.flush()
    ilosc_mocznika=0
    mocznik=False
    czy_woda_do_mocznika=False
    for i in all:
        if i.skladnik=='Mocznik':
            mocznik =True
            ilosc_mocznika=i.gramy
            if i.dodaj_wode=='on':
                czy_woda_do_mocznika = True

    print('mocznik', mocznik)
    sys.stdout.flush()
########################################################################################
    print('last', last)
    sys.stdout.flush()
    sumskl = 0
    for i in all:
        if i.gramy.isdigit() and i.gramy != '0':
            sumskl += int(i.gramy)
    print('sumskl', sumskl)
    sys.stdout.flush()

    if len(all) > 1 and last.aa == 'off' and last.gramy != "" and all.order_by('-pk')[1].gramy == "":
        last.aa = "on"
        last.save()
    if last.aa_ad == 'on' and last.aa == 'on':
        last.aa = 'off'
        last.save()
    if last.aa == 'on':
        for el in all.order_by('-pk'):  # order_by('-pk')
            if el.pk < l and el.gramy != "":
                print('break')
                break
            else:
                el.gramy = g
                el.obey = l
                el.save()


    ####################################################
    ########### kasowanie ilości g po usunięciu skłądnika z aa#########################
    for el in all:

        if all.filter(pk=el.obey).exists():
            pass
        else:
            if el.obey != None:
                el.gramy = ''
                el.obey = None
                el.save()
    ########################################################################################
    ################uwzględnianie aa ad#####################################################

    a = 0
    print('last.aa_ad == "on"', last.aa_ad == 'on', 'last.gramy', last.gramy)
    sys.stdout.flush()
    if last.aa_ad == 'on':  # tutaj sprawdzam na ile składników trzeba podzielić ilość gramów z aa ad

        last.gramy = ''
        last.save()
        sumskl = sumskl - int(last.aa_ad_gramy)
        for el in all.order_by('-pk'):  # order_by('-pk')
            print('el.gramy:', el.gramy,'el.skladnik:', el.skladnik, 'el.obey!=None', el.obey != None)
            sys.stdout.flush()
            if  (el.ilosc_na_recepcie == '' or el.gramy=='') and el.show==True:
                a = a + 1
            else:
                break
            print('dzelnik', a)
            sys.stdout.flush()


        # if last.aa_ad_gramy=='':
        #     last.aa_ad_gramy=last.gramy
        #     last.save()

        for el in all.order_by('-pk'):  # order_by('-pk')
            if el.pk < l and el.gramy != "":
                break
            else:
                if last.aa_ad_gramy != '' and a > 0:
                    el.gramy = str(round((int(last.aa_ad_gramy) - sumskl) / a, 2))
                    el.obey = l
                    el.save()
        sumskl = 0
        for el in all:
            if el.pk != l and el.obey!=l and el.gramy!='':
                sumskl += float(el.gramy)

        for el in all.order_by('-pk'):  # order_by('-pk')
            if el.obey != l:# or el.gramy == '':
                break
            else:
                print('dzelnik', a)
                sys.stdout.flush()
                print('sumskl', sumskl)
                sys.stdout.flush()
                print('last.aa_ad_gramy', last.aa_ad_gramy)
                sys.stdout.flush()
                if last.aa_ad_gramy != '' and a > 0:
                    el.gramy = str(round((int(last.aa_ad_gramy) - sumskl) / a, 2))

                    el.save()

    #########################uwzględnianie mocznika i wody##############################
    receptura = Receptura.objects.get(id=int(sklId))
    if mocznik==True and woda ==False and czy_woda_do_mocznika == True and ilosc_mocznika !='':
        Skladnik.objects.create(skladnik='Woda destylowana',receptura_id=receptura,show=False,gramy=(str(int(ilosc_mocznika)*1.5)))
    elif mocznik==True and woda ==True and czy_woda_do_mocznika == True and ilosc_mocznika !='':
        if jestwoda.gramy<(str(int(ilosc_mocznika)*1.5)):
            jestwoda.gramy=(str(int(ilosc_mocznika)*1.5))
            jestwoda.save()

    #####################obliczenia###################################################################
    # for el in all:
    #     to_updade = Przeliczanie(el.skladnik, el.pk)
    #     for key, value in to_updade.items():
    #         setattr(el, key, value)
    #     el.save()


    datax = serializers.serialize("python", Skladnik.objects.filter(receptura_id=int(sklId)))
    return JsonResponse({'tabela_zbiorcza':datax})


def delSkl (request,id):
    deletedElement=Skladnik.objects.filter(pk=id)
    print('deletedElement',deletedElement)
    sys.stdout.flush()
    skl=Skladnik.objects.get(pk=id)
    all = Skladnik.objects.filter(receptura_id=skl.receptura_id)
    for i in all:
        if skl.skladnik=='Mocznik' and i.skladnik == 'Woda destylowana' and i.show==False:
            i.delete()
        elif skl.skladnik=='Mocznik' and i.skladnik == 'Woda destylowana' and i.show==True:
            i.gramy=i.ilosc_na_recepcie
            i.save()

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
    print('edycjareceptura',receptura)
    sys.stdout.flush()
    elmenty_do_imputa={}
    for i in receptura:
        if i.skladnik == skl[:ind] and i.show == True:
            print('znalazłem składnik',i)
            sys.stdout.flush()
            for j in datadict['form']:
                datadict['values'][str(j)] = getattr(i, j)
    context = {'datadict': datadict}
    return JsonResponse(context)

def edytujsklJson (request,sklId):
    if request.is_ajax():
        ind = sklId.index('&')
        dodanySkladnik=request.POST.get("skladnik")
        ilosc=request.POST.get("ilosc_na_recepcie")
        receptura = Skladnik.objects.filter(receptura_id=int(sklId[ind + 1:]))
        print('edycjareceptura', receptura)
        sys.stdout.flush()
        elmenty_do_imputa = {}
        for i in receptura:
            if i.skladnik == sklId[:ind] and i.show == True:
                print('znalazłem składnik', i)
                to_edit = {'skladnik': i.skladnik, 'jednostka_z_recepty': i.jednostka_z_recepty}
                for j in data[dodanySkladnik]:
                    if type(j) != list:
                        a = request.POST.get(str(j))
                        to_edit[j] = a
                    else:
                        a = request.POST.get(str(j[0]))
                        to_edit[j[0]] = a
                print('to_update', to_edit)
                sys.stdout.flush()
                # ==========wstawianie gramów==========================
                if to_edit['jednostka_z_recepty'] == 'gramy':
                    to_edit['gramy'] = ilosc
                # =====================================================
                if 'aa_ad' in to_edit:
                    to_edit['aa_ad_gramy'] = to_edit['gramy']
                # if 'dodaj_wode' in to_updade:
                #     to_updade['aa_ad_gramy']=to_updade['gramy']
                # to_updade=Przeliczanie(dodanySkladnik,to_updade)
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



