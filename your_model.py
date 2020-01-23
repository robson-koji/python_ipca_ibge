class Ipca_ibge(models.Model):
    """ Armazena data e indice de calculo a ser aplicado """
    data_presente = models.DateTimeField(u"Data atual para qdo os valores passados serão calculados. Este campo é atualizado quando a tabela é atualizada pelo script.")
    ano_mes_passado = models.DateTimeField(blank=True, null=True)
    multiplicador = models.DecimalField(u"Indice a ser aplicado ao valor passado para trazer a valor da data presente.", max_digits=15, decimal_places=4, blank=True, null=True)
