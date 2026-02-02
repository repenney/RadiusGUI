from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import base64


def get_ssh_key_from_keyvault(keyvault_name: str, secret_name: str) -> str:
    """
    Retrieves an SSH private key stored in Azure Key Vault.

    Args:
        keyvault_name (str): The name of the Azure Key Vault.
        secret_name (str): The name of the secret storing the SSH key.

    Returns:
        str: The SSH key (private key) as a string.
    """
    
    vault_url = f"https://{keyvault_name}.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    secret = client.get_secret(secret_name)


    encoded_key = secret.value  # Retrieved from Azure Key Vault
    private_key_str = base64.b64decode(encoded_key).decode('utf-8')    #decode the base64-encoded key


    return private_key_str




#Use when testing this script locally
if __name__ == "__main__":
    # Example usage
    keyvault_name = "radius-server-kv"
    secret_name = "s2c2-ssh-private-key"
    get_ssh_key_from_keyvault(keyvault_name, secret_name)
    print("SSH Key retrieved successfully.")