def PrzeliczanieWit(dodanySkladnik,to_updade,rodzaj,ilosc):
    if dodanySkladnik=='witamina A':#to_update {'skladnik': 'witamina A', 'jednostka_z_recepty': 'solutio', 'ilosc_na_recepcie': '3', 'producent': 'Hasco 4500j.m./ml', 'gestosc': '1.082'}
        if to_updade['jednostka_z_recepty']=='solutio':#'jednostka_z_recepty','solutio','opakowania','gramy','jednostki'
            to_updade['opakowania']=str(round(float(to_updade['ilosc_na_recepcie'])/(float(to_updade['gestosc'])*10),3))
            if to_updade['producent']=='Hasco 45000j.m./ml':
                to_updade['jednostki']=str(round((float(to_updade['ilosc_na_recepcie'])/float(to_updade['gestosc'])*45000.0),3))
                to_updade['krople'] = str(round(float(to_updade['ilosc_na_recepcie']) / (float(to_updade['gestosc']))*28, 3))
                to_updade['mililitry'] = str(round(float(to_updade['ilosc_na_recepcie']) / (float(to_updade['gestosc'])), 3))
                to_updade['gramy']=to_updade['ilosc_na_recepcie']
            elif to_updade['producent']=='Medana 50000j.m./ml':
                to_updade['jednostki']=str(round(float(to_updade['ilosc_na_recepcie'])/(float(to_updade['gestosc'])*50000),3))
                to_updade['krople'] = str(round(float(to_updade['ilosc_na_recepcie']) / (float(to_updade['gestosc'])) * 30, 3))
                to_updade['mililitry']= str(round(float(to_updade['ilosc_na_recepcie'])/(float(to_updade['gestosc'])),3))
                to_updade['gramy'] = to_updade['ilosc_na_recepcie']
        elif to_updade['jednostka_z_recepty'] == 'jednostki':  # 'jednostka_z_recepty','solutio','opakowania','gramy','jednostki'
            if to_updade['producent'] == 'Hasco 45000j.m./ml':
                to_updade['mililitry'] = str(round(float(to_updade['ilosc_na_recepcie']) / 45000, 3))
                to_updade['gramy'] = str(round((float(to_updade['ilosc_na_recepcie']) / 45000)*float(to_updade['gestosc']), 3))
                to_updade['krople'] = str(round(float(to_updade['ilosc_na_recepcie']) / 45000 * 28, 3))
                to_updade['opakowania'] = str(round(float(to_updade['ilosc_na_recepcie']) / 4500, 3))
                to_updade['jednostki'] = to_updade['jednostki'] = str(round(float(to_updade['ilosc_na_recepcie']) , 3))
            elif to_updade['producent'] == 'Medana 50000j.m./ml':
                to_updade['mililitry'] = str(round(float(to_updade['ilosc_na_recepcie']) / 50000, 3))
                to_updade['gramy'] = str(round((float(to_updade['ilosc_na_recepcie']) / 50000)*float(to_updade['gestosc']), 3))
                to_updade['krople'] = str(round(float(to_updade['ilosc_na_recepcie']) / 50000 * 30, 3))
                to_updade['opakowania'] = str(round(float(to_updade['ilosc_na_recepcie']) / 5000, 3))
                to_updade['jednostki'] = str(round(float(to_updade['ilosc_na_recepcie']) , 3))
        elif to_updade['jednostka_z_recepty'] == 'krople':  # 'jednostka_z_recepty','solutio','opakowania','gramy','jednostki'
            if to_updade['producent'] == 'Hasco 45000j.m./ml':
                to_updade['mililitry'] = str(round(float(to_updade['ilosc_na_recepcie']) / 28, 3))
                to_updade['solutio'] = str(round((float(to_updade['ilosc_na_recepcie']) / 28)*float(to_updade['gestosc']), 3))
                to_updade['jednostki'] = str(round(float(to_updade['ilosc_na_recepcie']) / 28 * 45000, 3))
                to_updade['opakowania'] = str(round(float(to_updade['ilosc_na_recepcie']) / 280, 3))
                to_updade['gramy'] = str(round((float(to_updade['ilosc_na_recepcie']) / 28)*float(to_updade['gestosc']), 3))
            elif to_updade['producent'] == 'Medana 50000j.m./ml':
                to_updade['mililitry'] = str(round(float(to_updade['ilosc_na_recepcie']) / 28, 3))
                to_updade['solutio'] = str(round((float(to_updade['ilosc_na_recepcie']) / 28) * float(to_updade['gestosc']), 3))
                to_updade['jednostki'] = str(round(float(to_updade['ilosc_na_recepcie']) / 28 * 50000, 3))
                to_updade['opakowania'] = str(round(float(to_updade['ilosc_na_recepcie']) / 280, 3))
                to_updade['gramy'] = str(round((float(to_updade['ilosc_na_recepcie']) / 28) * float(to_updade['gestosc']), 3))
    if rodzaj == 'czopki_i_globulki':
        to_updade['krople']=str(round(float(to_updade['krople'])*float(ilosc),3))
        to_updade['mililitry'] = str(round(float(to_updade['mililitry']) * float(ilosc), 3))
        to_updade['opakowania'] = str(round(float(to_updade['opakowania']) * float(ilosc), 3))
        to_updade['jednostki'] = str(round(float(to_updade['jednostki']) * float(ilosc), 3))
        to_updade['gramy'] = str(round(float(to_updade['gramy']) * float(ilosc), 3))
    return to_updade
