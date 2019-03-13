from azure.mgmt.hdinsight import HDInsightManagementClient
from azure.common.credentials import ServicePrincipalCredentials
from sample_settings import *
from azure.mgmt.hdinsight.models import *


def main():
    # Authentication
    credentials = ServicePrincipalCredentials(
        client_id=CLIENT_ID,
        secret=CLIENT_SECRET,
        tenant=TENANT_ID
    )

    client = HDInsightManagementClient(credentials, SUBSCRIPTION_ID)

    # Prepare cluster create parameters
    create_params = ClusterCreateParametersExtended(
        location=LOCATION,
        tags={},
        properties=ClusterCreateProperties(
            cluster_version="3.6",
            os_type=OSType.linux,
            tier=Tier.standard,
            cluster_definition=ClusterDefinition(
                kind="Kafka",
                configurations={
                    "gateway": {
                        "restAuthCredential.isEnabled": "true",
                        "restAuthCredential.username": CLUSTER_LOGIN_USER_NAME,
                        "restAuthCredential.password": PASSWORD
                    }
                }
            ),
            compute_profile=ComputeProfile(
                roles=[
                    Role(
                        name="headnode",
                        target_instance_count=2,
                        hardware_profile=HardwareProfile(vm_size="Large"),
                        os_profile=OsProfile(
                            linux_operating_system_profile=LinuxOperatingSystemProfile(
                                username=SSH_USER_NAME,
                                password=PASSWORD
                            )
                        )
                    ),
                    Role(
                        name="workernode",
                        target_instance_count=3,
                        hardware_profile=HardwareProfile(vm_size="Large"),
                        os_profile=OsProfile(
                            linux_operating_system_profile=LinuxOperatingSystemProfile(
                                username=SSH_USER_NAME,
                                password=PASSWORD
                            )
                        ),
                        data_disks_groups = [
                            DataDisksGroups(
                                disks_per_node=2
                            )
                        ]
                    ),
                    Role(
                        name="zookeepernode",
                        target_instance_count=3,
                        hardware_profile=HardwareProfile(vm_size="Small"),
                        os_profile=OsProfile(
                            linux_operating_system_profile=LinuxOperatingSystemProfile(
                                username=SSH_USER_NAME,
                                password=PASSWORD
                            )
                        )
                    )
                ]
            ),
            storage_profile=StorageProfile(
                storageaccounts=[
                    StorageAccount(
                        name=STORAGE_ACCOUNT_NAME + BLOB_ENDPOINT_SUFFIX,
                        key=STORAGE_ACCOUNT_KEY,
                        container=CONTAINER_NAME.lower(),
                        is_default=True
                    )
                ]
            )
        )
    )

    print('Start to create HDInsight Kafka cluster {}'.format(CLUSTER_NAME))
    client.clusters.create(RESOURCE_GROUP_NAME, CLUSTER_NAME, create_params)


if __name__ == "__main__":
    main()