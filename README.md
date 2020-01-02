# Adaptive Big Data Pipelines

This project allows users with minimum experience on SQL to be able to:

1. Migrate existing data sets to the cloud
2. Automatically build ETL pipelines based on custom SQL queries
3. Schedule the ETL to run on a regular basis

This project encompasses the best of three worlds:

* DevOps Infrastructure as Code (IaC)
* Data Engineering ETL pipelines
* Microservices

### Prerequisites

After cloning this repository, you will need the following code pieces:

```
1. Python 3: python3, python3-pip, python3-devel
2. Docker Community Edition (including Docker compose)
3. AWS account: user with programatic access (credentials file). Copy the file to `services`
4. ...
```

### Launch

Move to the services folder and run the following command:

```
./setup.sh local
```

### Credits

This project is currently maintained by:

* Aldo Orozco <aldo.orozco.g@gmail.com>
