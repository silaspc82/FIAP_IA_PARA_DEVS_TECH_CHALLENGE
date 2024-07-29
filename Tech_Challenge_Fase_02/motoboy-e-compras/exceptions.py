class FitValidacaoException(Exception):
    pass

class TempoDecorridoException(FitValidacaoException):
    pass

class PopulacaoInexistenteException(FitValidacaoException):
    pass

class PesoException(FitValidacaoException):
    pass

class SuperMercadoSemCompraException(FitValidacaoException):
    pass