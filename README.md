# Adaptive Big Data Pipelines

This project allows users to:

1. Migrate existing data sets to the cloud
2. Easily build ETL pipelines based on custom SQL queries
3. Schedule those ETLs
4. Automatically plot the lineage DAG of the ETL.

### Prerequisites

After cloning this repository, you will need the following code pieces:

```
1. Python3.7: python3.7, python3.7-pip
   1.1. Install awscli with pip3.7
1. Docker Community Edition (including Docker compose)
2. AWS account:
   2.1. A user with programatic access as well as the following permissions:
     Full access: VPC, S3, IAM, and EC2
   2.2. Configure the user following this guide: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html
```

### Launch

Move to the `services` folder and run the following command:

```
./setup.sh local
```

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

### Authors

This project is currently maintained by:

* **Aldo Orozco <aldo.orozco.g@gmail.com>** - *Initial work*
