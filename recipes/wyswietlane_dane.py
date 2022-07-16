import sys
slownik_wyswietlane_dane={'Vitaminum A':['gramy_roztworu','krople','jednostki','producent','gestosc','opakowania','mililitry'],
                          'witamina E':['solutio','krople','gramy']
                      ,'Hydrokortyzon':['gramy'],'Wazelina':['gramy']
                    ,'Metronidazol':['gramy'],
                          "Detreomycyna":['gramy'],
                        'Mocznik':['gramy'],
                          'Etanol':['gramy','uzyte_stezenie','pozadane_stezenie','ilosc_etanolu','ilosc_wody_do_etanolu'],
                          'Woda destylowana':['ilosc_wody_do_etanolu','calkowita_ilosc_gramow_wody']
                          ,"Oleum Cacao":['gramy'],'Maść Cholesterolowa':['gramy'],
                          'Ichtiol':['gramy'],'Balsam Peruwiański':['gramy'],'Bizmutu węglan zasadowy':['gramy'], 'Bizmutu azotan zasadowy':['gramy'],'Oleum Menthae piperitae':['gramy','krople','gestosc','mililitry']}

def wyswietlane_dane(objects):
    ret = {}

    for i in objects:
        if i['fields']['skladnik'] in slownik_wyswietlane_dane:
            ret[i['fields']['skladnik']]=slownik_wyswietlane_dane[i['fields']['skladnik']]
    print('ret', ret)
    sys.stdout.flush()
    return ret



