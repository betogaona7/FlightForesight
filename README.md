# FlightForesight

API to predict whether a flight can be delayed or not.

## Installation 

Run the following command:

```
    conda env create -f conda_env.yaml
```

Note: be sure of having [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html) installed. 

## Testing

Run the following command:

```
    bash flightforesight_api/scripts/run_flask_server.sh 
```

It will start the server with the default configuration that is set in `flightforesight_api/flightforesight_api/settings.py`. You can access the endpoints docs using the Swagger UI at http://127.0.0.1:8081/ff_docs/

The API currently has only two endpoints under the namespace `/foresight/v1`: 
- `/predict` - Takes as input DIA, MES, temporada_alta, DIANOM, TIPOVUELO, OPERA, SIGLAORI, SIGLADES, periodo_dia variables. It predicts the Flight Delay.
- `/preload` - Doesn't need input. It is a warmup endpoint that loads the ML model.

**NOTE:** This code assumes the input info coming from a frontend side will follow some nomenclature and will be restricted to specific options. Please refer to [dataset info](assets/datasets/README.md) or to `flightforesight_api/flightforesight_api/utils/encoding_dict.py` along with `flightforesight_api/flightforesight_api/routes/routes.py/predict_flight_delay`. 

## ML Model 

Pre-trained model is saved under `assets/models`. To read how it was created please refer to [build_model.ipynb](assets/notebooks/) 

## Stress test

Using the [stress_test.lua](flightforesight_api/scripts/stress_test.lua) script, update the `request_rate` and adapt the following command based on your machine:

```
    wrk -t8 -c2000 -d140s -s flightforesight_api/scripts/stress_test.lua http://127.0.0.1:8081
```

For example if the target is to do at least 50000 requests in 45 seconds, then 
- `request_rate` would be 50000req/45s=1111.11. My machine can only send around 514 request max per second.
- `-t` (threads) should match your system's number of CPU threads. You can check yours with the command `lscpu`, in my case it was 8. 
- `-c` (concurrent connections) I used a max of 2000 connections since my threads could not cope with more.
- `-d` (time for the test) It would be 45s. In my case, to reach the 50,000 I had to increase the time to 140s.

**Stress output example**
```
Running 2m test @ http://127.0.0.1:8081
  8 threads and 2000 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   687.36ms  508.36ms   2.00s    63.80%
    Req/Sec    71.13     82.64   595.00     84.55%
  50704 requests in 2.33m, 12.91MB read
  Socket errors: connect 0, read 546, write 0, timeout 1151
Requests/sec:    361.93
Transfer/sec:     94.37KB
```

Based on the stats, since FlightForesight is not a real-time application, we can say that the latency is acceptable (around 0.5 seconds). We can also see that the test averaged 361 requests per second with a max of 595, this number might be sufficient if we don't expect higher traffic, otherwise, we could try to add more resources to handle more requests... 

Besides the stress output, compute times in my local machine were: 
- `/preload`: around 0.9 seconds
- `/predict`: around 0.04 seconds if the model was previously loaded in `/preload`;  Around 0.94 seconds for the first run if the model wasn't previously loaded in `/preload`

## Contribution 

To keep code good practices and a standarized format, please install the pre-commit git hooks scripts by running ```pre-commit install``` in the root directory of the repo. Please point your PRs to the development branch.