\* ComputerPlantProblem *\
Minimize
totalCosts: 10000 BuildPlant_CDMX + 8000 BuildPlant_Guadalajara
 + 6000 BuildPlant_Merida + 12000 BuildPlant_Monterrey
 + 5000 BuildPlant_Queretaro + 80 Route_CDMX_Aguscalientes
 + 100 Route_CDMX_Campeche + 10 Route_CDMX_Cuernavaca + 60 Route_CDMX_Xalapa
 + 22 Route_Guadalajara_Aguscalientes + 100 Route_Guadalajara_Campeche
 + 60 Route_Guadalajara_Cuernavaca + 150 Route_Guadalajara_Xalapa
 + 150 Route_Merida_Aguscalientes + 30 Route_Merida_Campeche
 + 200 Route_Merida_Cuernavaca + 100 Route_Merida_Xalapa
 + 80 Route_Monterrey_Aguscalientes + 120 Route_Monterrey_Campeche
 + 80 Route_Monterrey_Cuernavaca + 80 Route_Monterrey_Xalapa
 + 80 Route_Queretaro_Aguscalientes + 80 Route_Queretaro_Campeche
 + 40 Route_Queretaro_Cuernavaca + 50 Route_Queretaro_Xalapa
Subject To
SumProductIntoStore_Aguscalientes: Route_CDMX_Aguscalientes
 + Route_Guadalajara_Aguscalientes + Route_Merida_Aguscalientes
 + Route_Monterrey_Aguscalientes + Route_Queretaro_Aguscalientes >= 3000
SumProductIntoStore_Campeche: Route_CDMX_Campeche + Route_Guadalajara_Campeche
 + Route_Merida_Campeche + Route_Monterrey_Campeche + Route_Queretaro_Campeche
 >= 2000
SumProductIntoStore_Cuernavaca: Route_CDMX_Cuernavaca
 + Route_Guadalajara_Cuernavaca + Route_Merida_Cuernavaca
 + Route_Monterrey_Cuernavaca + Route_Queretaro_Cuernavaca >= 5500
SumProductIntoStore_Xalapa: Route_CDMX_Xalapa + Route_Guadalajara_Xalapa
 + Route_Merida_Xalapa + Route_Monterrey_Xalapa + Route_Queretaro_Xalapa
 >= 3000
SumProductOutPlant_CDMX: - 5000 BuildPlant_CDMX + Route_CDMX_Aguscalientes
 + Route_CDMX_Campeche + Route_CDMX_Cuernavaca + Route_CDMX_Xalapa <= 0
SumProductOutPlant_Guadalajara: - 2500 BuildPlant_Guadalajara
 + Route_Guadalajara_Aguscalientes + Route_Guadalajara_Campeche
 + Route_Guadalajara_Cuernavaca + Route_Guadalajara_Xalapa <= 0
SumProductOutPlant_Merida: - 1500 BuildPlant_Merida
 + Route_Merida_Aguscalientes + Route_Merida_Campeche
 + Route_Merida_Cuernavaca + Route_Merida_Xalapa <= 0
SumProductOutPlant_Monterrey: - 3500 BuildPlant_Monterrey
 + Route_Monterrey_Aguscalientes + Route_Monterrey_Campeche
 + Route_Monterrey_Cuernavaca + Route_Monterrey_Xalapa <= 0
SumProductOutPlant_Queretaro: - 1000 BuildPlant_Queretaro
 + Route_Queretaro_Aguscalientes + Route_Queretaro_Campeche
 + Route_Queretaro_Cuernavaca + Route_Queretaro_Xalapa <= 0
Bounds
0 <= Route_CDMX_Aguscalientes
0 <= Route_CDMX_Campeche
0 <= Route_CDMX_Cuernavaca
0 <= Route_CDMX_Xalapa
0 <= Route_Guadalajara_Aguscalientes
0 <= Route_Guadalajara_Campeche
0 <= Route_Guadalajara_Cuernavaca
0 <= Route_Guadalajara_Xalapa
0 <= Route_Merida_Aguscalientes
0 <= Route_Merida_Campeche
0 <= Route_Merida_Cuernavaca
0 <= Route_Merida_Xalapa
0 <= Route_Monterrey_Aguscalientes
0 <= Route_Monterrey_Campeche
0 <= Route_Monterrey_Cuernavaca
0 <= Route_Monterrey_Xalapa
0 <= Route_Queretaro_Aguscalientes
0 <= Route_Queretaro_Campeche
0 <= Route_Queretaro_Cuernavaca
0 <= Route_Queretaro_Xalapa
Generals
Route_CDMX_Aguscalientes
Route_CDMX_Campeche
Route_CDMX_Cuernavaca
Route_CDMX_Xalapa
Route_Guadalajara_Aguscalientes
Route_Guadalajara_Campeche
Route_Guadalajara_Cuernavaca
Route_Guadalajara_Xalapa
Route_Merida_Aguscalientes
Route_Merida_Campeche
Route_Merida_Cuernavaca
Route_Merida_Xalapa
Route_Monterrey_Aguscalientes
Route_Monterrey_Campeche
Route_Monterrey_Cuernavaca
Route_Monterrey_Xalapa
Route_Queretaro_Aguscalientes
Route_Queretaro_Campeche
Route_Queretaro_Cuernavaca
Route_Queretaro_Xalapa
Binaries
BuildPlant_CDMX
BuildPlant_Guadalajara
BuildPlant_Merida
BuildPlant_Monterrey
BuildPlant_Queretaro
End
