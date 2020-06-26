# Using Vault
For general information about Vault, please visit [Vault on github](https://github.com/hashicorp/vault).  

## Logging into Vault
You can find the Vault ui [here](https://cloud.denbi.de/ui/).  
Log in with OIDC as method and leave the role field blank.
![login_vault](../cloud_admin/images/vault/login.png)  

## Reading a secret
After logging in you should see the 'Secrets' tab.  
![secrets_overview](../cloud_admin/images/vault/secrets_overview.png)  
To access a secret, go to the URL of this format:  
```
https://cloud.denbi.de/ui/vault/secrets/<COMPUTE CENTER>/show/<YOUR ELIXIR ID>  

Example:
https://cloud.denbi.de/ui/vault/secrets/de.NBI%20Cloud%20Bielefeld%20-%20Production/show/b70a5363fe253d6b083ed81af01641e1d34ea97b@elixir-europe.org  
```
![user2_version_2](../cloud_admin/images/vault/user2_version2.png)  
Click on the eye-icon to read the secret value or click on the copy button next to it to copy the secret value directly.

### Share a one time secret
You have the possibility to have Vault wrap a JSON and create a token, which can be used to unwrap the JSON once.  
Every user that is able to log in with OIDC has access to the wrapping and unwrapping tools.

#### Wrapping
In the headbar, click on 'Tools'. At the left, click on 'Wrap'.  
![wrap_json](../cloud_admin/images/vault/wrap_json.png)  
Here you can write a JSON and choose how long the token should be valid. Click on 'Wrap data' and afterwards you can share the token.  
![wrapping_token](../cloud_admin/images/vault/wrapping_token.png)  
#### Lookup
In the headbar, click on 'Tools'. At the left, click on 'Lookup'.  
![token_lookup](../cloud_admin/images/vault/wrapping_token_lookup.png)  
Here you can input the wrapping token. If the token got already unwrapped or is not valid anymore, an error message appears.  
![token_error](../cloud_admin/images/vault/wrapping_token_error.png)
#### Unwrap
In the headbar, click on 'Tools'. At the left, click on 'Unwrap'. Here you can input the wrapping token. After clicking on 'Unwrap data' you should be able to see the whole JSON.  
![unwrap_json](../cloud_admin/images/vault/unwrap_json.png)  
