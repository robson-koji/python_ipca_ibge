# -*- coding: utf-8 -*-

"""
Faz um crawler no site do IBGE e captura o fator de calculo do IPCA
a valor presente.

Os dados sao capturados em um AJAX a partir desta pagina
https://sidra.ibge.gov.br/tabela/1737#resultado

Caso quebre ou haja inconsistencia, acessar a URL acima para verificar.
"""

import os, sys, time, django

from your.models import Your_model

import requests
import datetime
import json


data_corrente_obj = datetime.date.today()

def get_range_meses():
    """ 
    Monta a range de meses para capturar o indice de correcao.
    Eh passado no params do request para o IBGE.
    """
    
    # Escolha o ano de inicio. 
    # Julho de 1994 eh a adocao da moeda corrente (Real).     
    ano_inicio = 1994
    ano_corrente = data_corrente_obj.year

    range_meses = ''
    while ano_inicio <= ano_corrente:
        mes = 1
        while mes < 13:
            data_loop = "%d%d" % (ano_inicio, mes)
            data_loop_obj = datetime.datetime.strptime(data_loop, '%Y%m').date()

            if data_loop_obj> data_corrente_obj:
                break
            if mes < 10:
                mes_str = '0' + str(mes)
            else:
                mes_str = mes
            range_meses += "%s%s%s" % (str(ano_inicio), mes_str, ',')
            mes += 1
        ano_inicio += 1

    range_meses = range_meses[:-1]
    return range_meses



def get_params():
    """ Monta a string params para passar no request para o IBGE """
    range_meses = get_range_meses()

    # Adiciona valores a string params.
    params = 't/1737/f/c/h/n/n1/all/V/2266/P/' + range_meses + '/d/v2266 13'
    return params



def get_ipca_ibge(params):
    sess = requests.Session()
    IBGE_IPCA_AJAX_URL = 'https://sidra.ibge.gov.br/Ajax/JSon/Valores/1/1737'

    data = {
        'params': params,
        'versao': '-1',
        'desidentifica': 'false'
    }

    # Download do arquivo
    json_response = sess.post(IBGE_IPCA_AJAX_URL, data=data)
    return json_response



def grava_arquivo_db(json_response):
    # Converte para dict
    loaded_json = json.loads(json_response.content)

    # Armazenando o arquivo para fins de auditoria.
    file_path = 'arquivos/' + str(data_corrente_obj) + '.json'
    with open(file_path, 'wb') as f:
        f.write(json_response.content)

    # Apaga dados da tabela do DB.
    Your_model.objects.all().delete()

    # Insere os dados na tabela do DB.
    for lj in loaded_json:
        # dict_convert[lj['D3C']] = float(lj['V'])
        data_passado_obj = datetime.datetime.strptime(lj['D3C'], '%Y%m')
        multiplicador = lj['V']

        # Recria tabela
        Your_model.objects.create(data_presente=data_corrente_obj,
                                 ano_mes_passado=data_passado_obj,
                                 multiplicador=multiplicador)



if __name__ == "__main__":
    params = get_params()
    json_response = get_ipca_ibge(params)
    grava_arquivo_db(json_response)
