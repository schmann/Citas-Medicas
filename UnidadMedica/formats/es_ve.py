# Formatos para español de Venezuela
# https://docs.djangoproject.com/en/5.2/topics/i18n/formatting/

# Formato de fecha
DATE_FORMAT = 'd/m/Y'       # 25/10/2023
TIME_FORMAT = 'h:i A'       # 02:30 PM
DATETIME_FORMAT = 'd/m/Y h:i A'  # 25/10/2023 02:30 PM

# Formatos abreviados
DATE_INPUT_FORMATS = [
    '%d/%m/%Y',  # '25/10/2023'
    '%Y-%m-%d',  # '2023-10-25'
    '%d/%m/%y',  # '25/10/23'
]

DATETIME_INPUT_FORMATS = [
    '%d/%m/%Y %H:%M:%S',     # '25/10/2023 14:30:59'
    '%d/%m/%Y %H:%M',        # '25/10/2023 14:30'
    '%Y-%m-%d %H:%M:%S',     # '2023-10-25 14:30:59'
    '%Y-%m-%d %H:%M',        # '2023-10-25 14:30'
]

# Nombres de meses y días
MONTH_NAMES = ('', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
               'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre')

MONTH_ABBREVIATIONS = ('', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                      'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic')

DAY_NAMES = ('Domingo', 'Lunes', 'Martes', 'Miércoles', 
             'Jueves', 'Viernes', 'Sábado')

DAY_ABBREVIATIONS = ('Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb')

# Configuración de separadores
DECIMAL_SEPARATOR = ','
THOUSAND_SEPARATOR = '.'
NUMBER_GROUPING = 3

# Formato de hora de 12 horas con AM/PM
TIME_INPUT_FORMATS = [
    '%H:%M:%S',  # '14:30:59'
    '%H:%M',     # '14:30'
    '%I:%M %p',  # '02:30 PM'
    '%I:%M%p',   # '02:30PM'
]

# Primer día de la semana (0=Domingo, 1=Lunes)
FIRST_DAY_OF_WEEK = 1  # Lunes
