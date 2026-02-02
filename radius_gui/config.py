# config.py
from env_loader import required, required_split, required_pair

# -------- Static UI Data --------
SYSTEMS_CLUSTERS = {
    "System 1": ["Cluster 1", "Cluster 2"],
    "System 2": ["Cluster 1", "Cluster 2"],
    "System Test": ["Cluster Test"],
}

# -------- VMS --------
VMS = {
    "System 1": {
        "Cluster 1": required_split("SYSTEM_1_CLUSTER_1_VMS"),
        "Cluster 2": required_split("SYSTEM_1_CLUSTER_2_VMS"),
    },
    "System 2": {
        "Cluster 1": required_split("SYSTEM_2_CLUSTER_1_VMS"),
        "Cluster 2": required_split("SYSTEM_2_CLUSTER_2_VMS"),
    },
    "System Test": {
        "Cluster Test": required_split("SYSTEM_TEST_CLUSTER_TEST_VMS"),
    },
}

# -------- Keys --------
KEYS = {
    "System 1": {
        "Cluster 1": [
            required("KEYS_SYSTEM1_CLUSTER1_TYPE"),
            required("KEYS_SYSTEM1_CLUSTER1_VALUE"),
        ],
        "Cluster 2": [
            required("KEYS_SYSTEM1_CLUSTER2_TYPE"),
            required("KEYS_SYSTEM1_CLUSTER2_VALUE"),
        ],
    },
    "System 2": {
        "Cluster 1": [
            required("KEYS_SYSTEM2_CLUSTER1_TYPE"),
            required("KEYS_SYSTEM2_CLUSTER1_VALUE"),
        ],
        "Cluster 2": [
            required("KEYS_SYSTEM2_CLUSTER2_TYPE"),
            required("KEYS_SYSTEM2_CLUSTER2_VALUE"),
        ],
    },
    "System Test": {
        "Cluster Test": [
            required("KEYS_SYSTEMTEST_CLUSTERTEST_NAME"),
            required("KEYS_SYSTEMTEST_CLUSTERTEST_KEY"),
        ]
    },
}

# -------- Resource Groups --------
RESOURCE_GROUPS = {
    "System 1": [
        required_pair("RESOURCEGROUPS_SYSTEM1_EAST_NAME", "RESOURCEGROUPS_SYSTEM1_EAST_RULE"),
        required_pair("RESOURCEGROUPS_SYSTEM1_WEST_NAME", "RESOURCEGROUPS_SYSTEM1_WEST_RULE"),
    ],
    "System 2": [
        required_pair("RESOURCEGROUPS_SYSTEM2_EAST_NAME", "RESOURCEGROUPS_SYSTEM2_EAST_RULE"),
        required_pair("RESOURCEGROUPS_SYSTEM2_WEST_NAME", "RESOURCEGROUPS_SYSTEM2_WEST_RULE"),
    ],
    "System Test": [
        required_pair("RESOURCEGROUPS_SYSTEMTEST_TEST_NAME", "RESOURCEGROUPS_SYSTEMTEST_TEST_RULE"),
    ],
}

# -------- System IPs --------
SYSTEM_IPS = {
    "System 1": {
        "east": required_pair("SYSTEMIPS_SYSTEM1_EAST_HOST", "SYSTEMIPS_SYSTEM1_EAST_IP"),
        "west": required_pair("SYSTEMIPS_SYSTEM1_WEST_HOST", "SYSTEMIPS_SYSTEM1_WEST_IP"),
    },
    "System 2": {
        "east": required_pair("SYSTEMIPS_SYSTEM2_EAST_HOST", "SYSTEMIPS_SYSTEM2_EAST_IP"),
        "west": required_pair("SYSTEMIPS_SYSTEM2_WEST_HOST", "SYSTEMIPS_SYSTEM2_WEST_IP"),
    },
    "System Test": {
        "east": required_pair("SYSTEMIPS_SYSTEMTEST_EAST_HOST", "SYSTEMIPS_SYSTEMTEST_EAST_IP"),
        "west": required_pair("SYSTEMIPS_SYSTEMTEST_WEST_HOST", "SYSTEMIPS_SYSTEMTEST_WEST_IP"),
    },
}











'''
import env_loader # noqa: F401
import os




# VM List of systems and clusters for cluster selection page
SYSTEMS_CLUSTERS = {"System 1": ["Cluster 1", "Cluster 2"],
                    "System 2": ["Cluster 1", "Cluster 2"], 
                    "System Test": ["Cluster Test"]
}



# VMS Dict created from environment variables
VMS = {
    "System 1": {
        "Cluster 1": os.getenv("SYSTEM_1_CLUSTER_1_VMS").split(","),
        "Cluster 2": os.getenv("SYSTEM_1_CLUSTER_2_VMS").split(","),
    },
    "System 2": {
        "Cluster 1": os.getenv("SYSTEM_2_CLUSTER_1_VMS").split(","),
        "Cluster 2": os.getenv("SYSTEM_2_CLUSTER_2_VMS").split(",")
    },
    "System Test": {
        "Cluster Test": os.getenv("SYSTEM_TEST_CLUSTER_TEST_VMS").split(","),
    },
}

# Keys dict created from environment variables
KEYS = {
    "System 1": {
        "Cluster 1": [
            os.getenv("KEYS_SYSTEM1_CLUSTER1_TYPE"),
            os.getenv("KEYS_SYSTEM1_CLUSTER1_VALUE")
        ],
        "Cluster 2": [
            os.getenv("KEYS_SYSTEM1_CLUSTER2_TYPE"),
            os.getenv("KEYS_SYSTEM1_CLUSTER2_VALUE")
        ],
    },
    "System 2": {
        "Cluster 1": [
            os.getenv("KEYS_SYSTEM2_CLUSTER1_TYPE"),
            os.getenv("KEYS_SYSTEM2_CLUSTER1_VALUE")
        ],
        "Cluster 2": [
            os.getenv("KEYS_SYSTEM2_CLUSTER2_TYPE"),
            os.getenv("KEYS_SYSTEM2_CLUSTER2_VALUE")
        ]
    },
    "System Test": {
        "Cluster Test": [
            os.getenv("KEYS_SYSTEMTEST_CLUSTERTEST_NAME"),
            os.getenv("KEYS_SYSTEMTEST_CLUSTERTEST_KEY")
        ]
    }
}


# Resource Groups dict created from environment variables
RESOURCE_GROUPS = {
    "System 1": [
        (os.getenv("RESOURCEGROUPS_SYSTEM1_EAST_NAME"), os.getenv("RESOURCEGROUPS_SYSTEM1_EAST_RULE")),
        (os.getenv("RESOURCEGROUPS_SYSTEM1_WEST_NAME"), os.getenv("RESOURCEGROUPS_SYSTEM1_WEST_RULE"))
    ],
    "System 2": [
        (os.getenv("RESOURCEGROUPS_SYSTEM2_EAST_NAME"), os.getenv("RESOURCEGROUPS_SYSTEM2_EAST_RULE")),
        (os.getenv("RESOURCEGROUPS_SYSTEM2_WEST_NAME"), os.getenv("RESOURCEGROUPS_SYSTEM2_WEST_RULE"))
    ],
    "System Test": [
        (os.getenv("RESOURCEGROUPS_SYSTEMTEST_TEST_NAME"), os.getenv("RESOURCEGROUPS_SYSTEMTEST_TEST_RULE"))
    ]
}



# System IPs dict created from environment variables for results page
SYSTEM_IPS = {
    "System 1": {
        "east": (
            os.getenv("SYSTEMIPS_SYSTEM1_EAST_HOST"),
            os.getenv("SYSTEMIPS_SYSTEM1_EAST_IP")
        ),
        "west": (
            os.getenv("SYSTEMIPS_SYSTEM1_WEST_HOST"),
            os.getenv("SYSTEMIPS_SYSTEM1_WEST_IP")
        )
    },
    "System 2": {
        "east": (
            os.getenv("SYSTEMIPS_SYSTEM2_EAST_HOST"),
            os.getenv("SYSTEMIPS_SYSTEM2_EAST_IP")
        ),
        "west": (
            os.getenv("SYSTEMIPS_SYSTEM2_WEST_HOST"),
            os.getenv("SYSTEMIPS_SYSTEM2_WEST_IP")
        )
    },
    "System Test": {
        "east": (
            os.getenv("SYSTEMIPS_SYSTEMTEST_EAST_HOST"),
            os.getenv("SYSTEMIPS_SYSTEMTEST_EAST_IP")
        ),
        "west": (
            os.getenv("SYSTEMIPS_SYSTEMTEST_WEST_HOST"),
            os.getenv("SYSTEMIPS_SYSTEMTEST_WEST_IP")
        )
    }
}
'''