### Website Checker

Check arbitrary website health using aiven.io services.


#### Installing Dependencies  

```
pip install -r requirements.txt
```

### Running The App

1. Grab the source code.
2. Create .env file with
   ```
   SERVICE_URI=<kafka uri>
   CA_PATH=<path to ca.pem>
   KEY_PATH=<path to service.key>
   CERT_PATH=<path to service.cert>

   DB_URI=<postgres uri>

   ```
   In my case all certificates and services keys are located in `cert` folder.
3. Starting Kafka producer:
    ```
    python main.py --producer --url=https.google.com
    ```
4. Starting Kafka consumer:
    ```
    python main.py --consumer
    ```

### TODO

1. Unit tests
2. Code refactoring (packages, configurations, logging)
3. Dockerize the app
4. Etc