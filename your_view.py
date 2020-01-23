"""
Insira este metodo na classe que possui valor financeiro passado a ser corrigido pelo IPCA.
Basta chamar o metodo para obter o valor corrigido. 
Altere conforme a necessidade.
"""

from your_model.models import Ipca_ibge

def valor_concedido_ipca(self):
    """
    Traz a valor presente, um valor passado corrigido pelo IPCA
    Formula = (valor a ser corrigido / multiplicador passado ) * multiplicador presente
    """
    try:
        ultimo_mes = Ipca_ibge.objects.latest('ano_mes_passado')
        indice = Ipca_ibge.objects.get(ano_mes_passado = self.data_inicio)
        valor_concedido_ipca = (self.valor_a_corrigir/indice.multiplicador) * ultimo_mes.multiplicador
        valor_concedido_ipca = str(round(valor_concedido_ipca, 2))
        return valor_concedido_ipca
    except:
        # Na data corrente, ainda nao existe o IPCA.
        return self.valor_concedido
        return None
