from django.shortcuts import render,redirect
from django.http import JsonResponse,response
from django.core import serializers
import sys
from .models import Receptura
from .forms import RecepturaForm
from .models import roboczareceptura
from .algorytmy import Przeliczanie


data={'witamina A':[['jednostka_z_recepty','opakowania','gramy','jednostki'],'ilosc_na_recepcie',['producent','Hasco 4500j.m./ml','Medana 50000j.m./ml'],],'witamina E':['opakowania','gramy','jednostki',['producent','Hasco 0,3g/ml']],'Hydrokortyzon':['gramy','aa'],'Metronidazol':['gramy','aa'],'Wazelina':['gramy','aa','aa_ad']}
def home (request):
    skladniki = roboczareceptura.objects.all()
    t = []
    for i in skladniki:
        t.append(i.skladnik)
    datax = serializers.serialize("python", roboczareceptura.objects.all())
    return render(request,'home.html',{'tabela2':datax})

def formJson (request,skl):
    datadict=data[skl]
    context={ 'datadict':datadict}
    return JsonResponse(context)


def dodajsklJson (request):
    if request.is_ajax():
        dodanySkladnik=request.POST.get("skladnik")

        roboczareceptura.objects.create(skladnik=dodanySkladnik,)
        ostatniskl = roboczareceptura.objects.last()
        to_updade={'skladnik' :ostatniskl.skladnik}

        for i in data[dodanySkladnik]:
            if type(i)!=list:
                a=request.POST.get(str(i))

                to_updade[i]=a
            else:
                a = request.POST.get(str(i[0]))
                to_updade[i[0]] = a
        print('to_update',to_updade)
        sys.stdout.flush()
        if 'aa_ad' in to_updade:
            to_updade['aa_ad_gramy']=to_updade['gramy']
        to_updade=Przeliczanie(dodanySkladnik,to_updade)
        for key, value in to_updade.items():
            setattr(ostatniskl, key, value)
        # if ostatniskl.aa_ad=='on':
        #     ostatniskl.aa_ad_gramy=ostatniskl.gramy
        ostatniskl.save()

        return JsonResponse({'tabela':to_updade})
    return JsonResponse({'nie dodano skladnika': False, }, safe=False)


def aktualizujTabela (request):
    #########uwzględniaie aa################################
    print('roboczareceptura.objects.last()', roboczareceptura.objects.last(),roboczareceptura.objects.last().aa)
    sys.stdout.flush()
    g=roboczareceptura.objects.last().gramy
    l=roboczareceptura.objects.last().pk
    print('g', g)
    sys.stdout.flush()
    #auto aa

    all=roboczareceptura.objects.all()
    last=roboczareceptura.objects.last()
    sumskl = 0
    for i in all:
        if i.gramy.isdigit() and i.gramy!='0':
            sumskl+=int(i.gramy)
    print('sumskl', sumskl)
    sys.stdout.flush()

    if len(all)>1 and last.aa=='off' and last.gramy!=""  and all.order_by('-pk')[1].gramy=="":
       last.aa ="on"
       last.save()
    if last.aa_ad=='on' and last.aa=='on':
        last.aa='off'
        last.save()
    print('roboczareceptura.objects.last().aa',roboczareceptura.objects.last().aa)
    if roboczareceptura.objects.last().aa=='on':
        for el in roboczareceptura.objects.all().order_by('-pk'):#order_by('-pk')
            if el.pk<l and el.gramy != "":
                break
            else:
                el.gramy = g
                el.obey=l
                el.save()

    ####################################################
    ########### kasowanie ilości g po usunięciu skłądnika z aa#########################
    for el in roboczareceptura.objects.all():

        if roboczareceptura.objects.filter(pk=el.obey).exists():
            pass
        else:
            if el.obey!=None:
                el.gramy=''
                el.obey= None
                el.save()
    ########################################################################################
    ################uwzględnianie aa ad#####################################################

    a = 0
    if roboczareceptura.objects.last().aa_ad=='on':#tutaj sprawdzam na ile składników trzeba podzielić ilość gramów z aa ad

        last.gramy = ''
        last.save()
        sumskl = sumskl - int(last.aa_ad_gramy)
        for el in roboczareceptura.objects.all().order_by('-pk'):#order_by('-pk')
            print('el.gramy:', el.gramy,'el.obey!=None',el.obey!=None)
            sys.stdout.flush()
            if el.obey!=None or el.gramy=='':
                a=a+1
            else:
                break
            print('dzelnik', a)
            sys.stdout.flush()
        print('dzelnik', a)
        sys.stdout.flush()

        # if last.aa_ad_gramy=='':
        #     last.aa_ad_gramy=last.gramy
        #     last.save()

        for el in roboczareceptura.objects.all().order_by('-pk'):#order_by('-pk')
            if el.pk<l and el.gramy != "":
                break
            else:
                if last.aa_ad_gramy!='' and a>0:

                    el.gramy = str(round((int(last.aa_ad_gramy)-sumskl)/a,2))
                    el.obey = l
                    el.save()
        sumskl=0
        for el in all:
            if el.obey!=l:
                sumskl+=int(el.gramy)

        for el in roboczareceptura.objects.all().order_by('-pk'):#order_by('-pk')
            if  el.obey !=l or el.gramy=='':
                break
            else:
                if last.aa_ad_gramy!='' and a>0:

                    el.gramy = str(round((int(last.aa_ad_gramy)-sumskl)/a,2))

                    el.save()

    #####################################################################################
    datax = serializers.serialize("python", roboczareceptura.objects.all())
    return JsonResponse({'tabela_zbiorcza':datax})


def delSkl (request, id):
    deletedElement=roboczareceptura.objects.filter(pk=id)
    response=serializers.serialize("python", deletedElement)
    deletedElement.delete()
    print('response', response)
    sys.stdout.flush()
    return JsonResponse({'response':response})

#########################################################################################
def mojeRec (request):
    moje_receptury=Receptura.objects.all()
    context={'receptury':moje_receptury}
    return render(request,'mojerec.html',context)

def dodajRec(request):
    if request.method != 'POST':
      form=RecepturaForm
    else:
        # create a form instance and populate it with data from the request:
        form = RecepturaForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return redirect('mojerec')
    context = {'form': form}
    return render(request, 'dodajrec.html', context)

def receptura (request,receptura_id):
    receptura=Receptura.objects.get(id=receptura_id)
    context={'receptura':receptura}
    return render(request,'receptura.html',context)


def dodajskladnikJson (request):
    if request.is_ajax():
        dodanySkladnik=request.POST.get("skladnik")

        roboczareceptura.objects.create(skladnik=dodanySkladnik,)
        ostatniskl = roboczareceptura.objects.last()
        to_updade={'skladnik' :ostatniskl.skladnik}

        # for i in data[dodanySkladnik]:
        #     if type(i)!=list:
        #         a=request.POST.get(str(i))
        #
        #         to_updade[i]=a
        #     else:
        #         a = request.POST.get(str(i[0]))
        #         to_updade[i[0]] = a
        # print('to_update',to_updade)
        # sys.stdout.flush()
        # if 'aa_ad' in to_updade:
        #     to_updade['aa_ad_gramy']=to_updade['gramy']
        # to_updade=Przeliczanie(dodanySkladnik,to_updade)
        # for key, value in to_updade.items():
        #     setattr(ostatniskl, key, value)
        # # if ostatniskl.aa_ad=='on':
        # #     ostatniskl.aa_ad_gramy=ostatniskl.gramy
        # ostatniskl.save()

        return JsonResponse({'tabela':to_updade})
    return JsonResponse({'nie dodano skladnika': False, }, safe=False)


