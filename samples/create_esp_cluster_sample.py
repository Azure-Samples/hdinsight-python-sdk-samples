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

    # Parse AAD-DS DNS Domain name from resource id
    aadds_dns_domain_name = AADDS_RESOURCE_ID.split('/')[-1]

    # Prepare cluster create parameters
    create_params = ClusterCreateParametersExtended(
        location=LOCATION,
        tags={},
        properties=ClusterCreateProperties(
            cluster_version="3.6",
            os_type=OSType.linux,
            tier=Tier.premium,
            cluster_definition=ClusterDefinition(
                kind="Spark",
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
                        ),
                        virtual_network_profile=VirtualNetworkProfile(
                            id=VIRTUAL_NETWORK_RESOURCE_ID,
                            subnet='{}/subnets/{}'.format(VIRTUAL_NETWORK_RESOURCE_ID, SUBNET_NAME)
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
                        virtual_network_profile=VirtualNetworkProfile(
                            id=VIRTUAL_NETWORK_RESOURCE_ID,
                            subnet='{}/subnets/{}'.format(VIRTUAL_NETWORK_RESOURCE_ID, SUBNET_NAME)
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
            ),
            security_profile=SecurityProfile(
                directory_type=DirectoryType.active_directory,
                ldaps_urls=[LDAPS_URL],
                domain_username=DOMAIN_USER_NAME,
                domain=aadds_dns_domain_name,
                cluster_users_group_dns=[CLUSTER_ACCESS_GROUP],
                aadds_resource_id=AADDS_RESOURCE_ID,
                msi_resource_id=MANAGED_IDENTITY_RESOURCE_ID
            )
        ),
        identity=ClusterIdentity(
            type=ResourceIdentityType.user_assigned,
            user_assigned_identities={MANAGED_IDENTITY_RESOURCE_ID: {}}
        )
    )

    print('Start to create HDInsight Spark cluster {} with Enterprise Security Package'.format(CLUSTER_NAME))
    client.clusters.create(RESOURCE_GROUP_NAME, CLUSTER_NAME, create_params)


if __name__ == "__main__":
    main()