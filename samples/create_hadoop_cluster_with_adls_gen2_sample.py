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

    # Parse ADLS Gen2 storage account name from resource id
    adls_gen2_account_name = ADLS_GEN2_RESOURCE_ID.split('/')[-1]

    # Prepare cluster create parameters
    create_params = ClusterCreateParametersExtended(
        location=LOCATION,
        tags={},
        properties=ClusterCreateProperties(
            cluster_version="3.6",
            os_type=OSType.linux,
            tier=Tier.standard,
            cluster_definition=ClusterDefinition(
                kind="Hadoop",
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
                        )
                    )
                ]
            ),
            storage_profile=StorageProfile(
                storageaccounts=[
                    StorageAccount(
                        name=adls_gen2_account_name + DFS_ENDPOINT_SUFFIX,
                        is_default=True,
                        file_system=ADLS_GEN2_FILE_SYSTEM_NAME.lower(),
                        resource_id=ADLS_GEN2_RESOURCE_ID,
                        msi_resource_id=MANAGED_IDENTITY_RESOURCE_ID
                    )
                ]
            )
        ),
        identity=ClusterIdentity(
            type=ResourceIdentityType.user_assigned,
            user_assigned_identities={MANAGED_IDENTITY_RESOURCE_ID: {}}
        )
    )

    print('Starting to create HDInsight Hadoop cluster {} with Azure Data Lake Storage Gen2'.format(CLUSTER_NAME))
    client.clusters.create(RESOURCE_GROUP_NAME, CLUSTER_NAME, create_params)


if __name__ == "__main__":
    main()