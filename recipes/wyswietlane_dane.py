import sys
slownik_wyswietlane_dane={'Witamina A':['gramy_roztworu','krople','jednostki','producent','gestosc','opakowania','mililitry'],
                          'witamina E':['solutio','krople','gramy']
                      ,'Hydrokortyzon':['gramy'],'Wazelina':['gramy']
                    ,'Metronidazol':['gramy'],
                          "Detreomycyna":['gramy'],
                        'Mocznik':['gramy'],
                          'Etanol':['gramy','uzyte_stezenie','pozadane_stezenie','ilosc_etanolu','ilosc_wody_do_etanolu'],
                          'Woda destylowana':['ilosc_wody_do_etanolu','calkowita_ilosc_gramow_wody']
                          ,"Oleum Cacao":['gramy'],'Maść Cholesterolowa':['gramy'],
                          'Ichtiol':['gramy'],'Balsam Peruwiański':['gramy'],'Bizmutu węglan zasadowy':['gramy'], 'Bizmutu azotan zasadowy':['gramy'],'Oleum Menthae piperitae':['gramy','krople','gestosc','mililitry'],'Wazelina biała':['gramy'],'Prokaina':['gramy'],'Anestezyna':['gramy'],
                          'Hascobaza':['gramy'],"Neomycyna":['gramy'],'Efedryna':['gramy'],'Erytromycna':['gramy'],'Rezorcyna':['gramy'],'Lanolina':['gramy'],'Wazelina żółta':['gramy'],
                            'Tlenek Cynku':['gramy'],'Olej Rycynowy':['gramy'],'Papaweryna':['gramy'],'Mentol':['gramy'],'Laktoza':['gramy'],'Kwas Salicylowy':['gramy'],

             'Nystatyna':['gramy','jednostki'],'3% roztwór kwas borowy':['gramy','ilosc_kwasu_borowego_do_roztworu','woda_kwas_borowy'],
             'Euceryna':['gramy'],'Gliceryna 86%':['gramy'],

                          }

def wyswietlane_dane(objects):
    ret = {}

    for i in objects:
        if i['fields']['skladnik'] in slownik_wyswietlane_dane:
            ret[i['fields']['skladnik']]=slownik_wyswietlane_dane[i['fields']['skladnik']]
    print('ret', ret)
    sys.stdout.flush()
    return ret



