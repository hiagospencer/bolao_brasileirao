import re
import datetime
import pytz

def validar_senha(senha, confirmar_senha):
  """Valida se a senha atende aos critérios de segurança e se as senhas coincidem.
      A senha deve ter pelo menos 8 caracteres, uma letra maiúscula e um número.

  Args:
    senha: A senha digitada pelo usuário.
    confirmar_senha: A confirmação da senha.

  Returns:
    True se a senha for válida e as senhas coincidirem, False caso contrário.
  """

  # Expressão regular para verificar a complexidade da senha
  regex = r'^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'

  # Verifica se a senha corresponde à expressão regular e se as senhas coincidem
  return re.match(regex, senha) is not None and senha == confirmar_senha




def utc_para_brasil(utc_string):
    """
    Converte uma string de data/hora UTC para o horário de Brasília.

    Args:
        utc_string: String representando a data/hora em UTC no formato ISO 8601.

    Returns:
        Objeto datetime representando a data/hora convertida para o horário de Brasília.
    """


   # Cria um objeto datetime a partir da string UTC
    utc_datetime = datetime.datetime.fromisoformat(utc_string)

    # Define os fusos horários
    utc = pytz.utc
    brasilia = pytz.timezone('America/Sao_Paulo')

    # Localiza a data/hora UTC e converte para o fuso horário de Brasília
    utc_datetime = utc.localize(utc_datetime)
    brasilia_datetime = utc_datetime.astimezone(brasilia)

    return brasilia_datetime
