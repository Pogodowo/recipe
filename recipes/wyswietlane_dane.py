import sys
slownik_wyswietlane_dane={'witamina A':['solutio','krople','jednostki'],
                          'witamina E':['solutio','krople','gramy']
                      ,'Hydrokortyzon':['gramy'],'Wazelina':['gramy'],
                          'Etanol':['gramy','uzyte_stezenie','pozadane_stezenie','ilosc_etanolu','ilosc_wody_do_etanolu'],
                          'Woda destylowana':['ilosc_wody_do_etanolu','calkowita_ilosc_gramow_wody']}

def wyswietlane_dane(objects):
    ret = {}

    for i in objects:
        if i['fields']['skladnik'] in slownik_wyswietlane_dane:
            ret[i['fields']['skladnik']]=slownik_wyswietlane_dane[i['fields']['skladnik']]
    print('ret', ret)
    sys.stdout.flush()
    return ret



