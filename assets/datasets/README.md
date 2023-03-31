# Datasets

- **SCL_flights_data.csv** has public data of flights that arrived or left the SCL airport in 2018:
    - _Fecha-I_: Fecha y hora programada del vuelo. 
    - _Vlo-I_: Número de vuelo programado.
    - _Ori-I_: Código de ciudad de origen programado. 
    - _Des-I_: Código de ciudad de destino programado. 
    - _Emp-I_: Código aerolínea de vuelo programado. 
    - _Fecha-O_: Fecha y hora de operación del vuelo. 
    - _Vlo-O_: Número de vuelo de operación del vuelo. 
    - _Ori-O_: Código de ciudad de origen de operación 
    - _Des-O_: Código de ciudad de destino de operación. 
    - _Emp-O_: Código aerolínea de vuelo operado.
    - _DIA_: Día del mes de operación del vuelo.
    - _MES_: Número de mes de operación del vuelo. 
    - _AÑO_: Año de operación del vuelo.
    - _DIANOM_: Día de la semana de operación del vuelo. 
    - _TIPOVUELO_  Tipo de vuelo, I =Internacional, N =Nacional. 
    - _OPERA_: Nombre de aerolínea que opera.
    - _SIGLAORI_: Nombre ciudad origen.
    - _SIGLADES_: Nombre ciudad destino.

- **SCL_flights_data_extra** has generated data from SCL_flight:
    - _temporada_alta_: 1 si Fecha-I está entre 15-Dic y 3-Mar, o 15-Jul y 31-Jul, o 11-Sep y 30-Sep, 0 si no.
    - _dif_min_: diferencia en minutos entre Fecha-O y Fecha-I.
    - _atraso_15_: 1 si dif_min > 15, 0 si no.
    - _periodo_dia_: mañana (entre 5:00 y 11:59), tarde (entre 12:00 y 18:59) y noche (entre 19:00 y 4:59), en base a Fecha-I.

- **SCL_flights_full** contains both of the above data: original and generated one.


# Value options 

The next are the possibles values for each column, this is relevant for prediction inference: 

- Fecha-I(Date) - YYYY-MM-DD HH:MM:SS
- Fecha-O(Date) - YYYY-MM-DD HH:MM:SS
- Dia (Int) - from 1 to 31
- Mes (Int) - from 1 to 12
- AÑO (Int) - YYYY
- temporada_alta (Int) - 0 or 1

You can check the possible values for the categorical features (Vlo-I, Ori-I,Des-I, Emp-I, Vlo-O, Ori-O, Des-O, Emp-O, DIANOM, TIPOVUELO, OPERA, SIGLAORI, SIGLADES, temporada_alta, dif_min, atraso_15, periodo_dia) with the following code snippet: 

```
import pandas as pd

df = pd.read_csv('SCL_flights_full.csv') # path to csv file

feature_name = "OPERA" # name of the categorical feature
for value in df[feature_name].unique():
    print(value)
```