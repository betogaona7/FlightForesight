-- stress_test.lua
request_rate = 514 --1111.11 -- requests per second
interval = 1 / request_rate -- interval between requests in seconds

function delay()
    return math.floor(interval * 1000000) -- delay in microseconds
end

function request()
    wrk.method = "GET"
    wrk.path = "/foresight/v1/predict?DIA=1&MES=8&temporada_alta=1&DIANOM=Domingo&TIPOVUELO=I&OPERA=Aeromexico&SIGLAORI=Santiago&SIGLADES=Cancun&periodo_dia=tarde"
    return wrk.format(nil)
end
