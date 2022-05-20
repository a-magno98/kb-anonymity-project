def exec_pc_infortuni(t):
    pc = []
    if t['LuogoNascita'] == 0:
        pc.append(('LuogoNascita', '==', 0))
        
        #DataAccadimento
        if 20210101 <= t['DataAccadimento'] <= 20210401:
            pc.append(('DataAccadimento', '<=', 20210401))
            pc.append(('DataAccadimento', '>=', 20210101))
        
        elif 20220101 <= t['DataAccadimento'] <= 20220401:
            pc.append(('DataAccadimento', '<=', 20220401))
            pc.append(('DataAccadimento', '>=', 20220101))

        #Genere
        if t['Genere'] == 0:
            pc.append(('Genere', '==', 0))

        else:
            pc.append(('Genere', '==', 1))	

    else:
        pc.append(('LuogoNascita', '!=', 0))

    if t['SettoreAttivitaEconomica'] >= -1 and t['SettoreAttivitaEconomica'] <= 3:
        pc.append(('SettoreAttivitaEconomica', '>=', -1))
        pc.append(('SettoreAttivitaEconomica', '<=', 3))

        #GestioneTariffaria
        if t['GestioneTariffaria'] >= -1 and t['GestioneTariffaria'] <= 4:
            pc.append(('GestioneTariffaria', '>=', -1))
            pc.append(('GestioneTariffaria', '<=', 4))
    else:
        pc.append(('SettoreAttivitaEconomica', '>=', 10))
        pc.append(('SettoreAttivitaEconomica', '<=', 96))
    
    if t['Eta'] <= 20:
        pc.append(('Eta', '<=', 20))

    elif  t['Eta'] > 20 and t['Eta'] <= 55:
        pc.append(('Eta', '>', 20))
        pc.append(('Eta', '<=', 55))

    else:
        pc.append(('Eta', '>', 55))

    #ModalitaAccadimento
    if t['ModalitaAccadimento'] == 0:
        pc.append(('ModalitaAccadimento', '==', 0))

        #ConSenzaMezzoTrasporto
        if t['ConSenzaMezzoTrasporto'] == 0:
            pc.append(('ConSenzaMezzoTrasporto', '==', 0))
        
        else:
            pc.append(('ConSenzaMezzoTrasporto', '==', 1))

    else:
        pc.append(('ModalitaAccadimento', '==', 1))

    if 20210101 <= t['DataProtocollo'] <= 20210401:		
        pc.append(('DataProtocollo', '<=', 20191231))
        pc.append(('DataProtocollo', '>=', 20191201))
        
        #GrandeGruppoTariffario
        if t['GrandeGruppoTariffario'] >= -1 and t['GrandeGruppoTariffario'] <= 9:
            pc.append(('GrandeGruppoTariffario', '>=', -1))
            pc.append(('GrandeGruppoTariffario', '<=', 9))

    elif 20220101 <= t['DataProtocollo'] <= 20220401:
            pc.append(('DataProtocollo', '<=', 20220401))
            pc.append(('DataProtocollo', '>=', 20220101))
    
    return pc