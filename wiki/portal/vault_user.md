# Using Vault
For general information about Vault, please visit [Vault on github](https://github.com/hashicorp/vault).  

## Logging into Vault
You can find the Vault ui [here](https://cloud.denbi.de/ui/).  
Log in with OIDC as method and *your_compute_center* as role.  
The available compute center are:

* bielefeld  
* giessen  
* ...  

## Reading a secret
After logging in you should see the 'Secrets' tab. Click on your compute center, where you will find paths leading to a protected key/value store.  
Select the path with your Elixir ID. Here you will find kay/value pairs. Click on the eye-icon to read the secret value or click on the copy button next to it to copy the secret value directly.

## Share a one time secret
You have the possibility to have Vault wrap a JSON and create a token, which can be used to unwrap the JSON once.  
Every user that is able to log in with OIDC has access to the wrapping and unwrapping tools.

### Wrapping
In the headbar, click on 'Tools'. At the left, click on 'Wrap'. Here you can write a JSON and choose how long the token should be valid. Click on 'Wrap data' and afterwards you can share the token.

### Lookup
In the headbar, click on 'Tools'. At the left, click on 'Lookup'. Here you can input the wrapping token. If the token got already unwrapped or is not valid anymore, an error message appears.

### Unwrap
In the headbar, click on 'Tools'. At the left, click on 'Unwrap'. Here you can input the wrapping token. After clicking on 'Unwrap data' you should be able to see the whole JSON.

