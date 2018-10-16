# Register your identity provider for [Elixir](https://www.elixir-europe.org/)

## Introduction

This document is intended for system administrators who would like to register their identity provider for the [Elixir Authentication and Authorization Infrastructure (AAI)](https://www.elixir-europe.org/services/compute/aai).
An AAI delegates the process of registration, authentication and the defining of access rules to different parties:
Universities as an example are responsible for registration and authentication of members. Services like e-Learning
systems provide the rules for accessing the service. This federated concept shows multiple benefits to services and identity
providers such as

* Services do not have to provide or implement an authentication and authorization system on its own.

* Integration among identity providers such as universities is not needed.

* Users do not have to manage multiple accounts and associated passwords (see [Single-Sign-On](https://en.wikipedia.org/wiki/Single_sign-on)).

## Pre-condition

The institution responsible for registration and authentication must install a Shibboleth identity provider. 
[Shibboleth](https://www.shibboleth.net/) is an open source project which is based on the SAML protocol and is designed for federated identity management.
As stated on the Shibboleth [website](https://www.shibboleth.net/products/identity-provider/) it provides support for LDAP, Kerberos and JAAS, and many more.

## Step 1: Registration in the DFN

The [DFN](https://www.dfn.de/) aims to build an authentication federation ([DFN AAI](https://www.aai.dfn.de/en/)) of research institutes and universities and provides a service for aggregating multiple
identity providers. This information can later be used by relying services to offer a user to choose his home institutional account.
The condition for participating with your Shibboleth installation as an identity provider in the DFN AAI is explained on the [DFN registration site](https://wiki.aai.dfn.de/en:registration)

One part of the registration process is also an opt in to the participation in eduGAIN which will be explained in the next section.

## Step 2: Opt in for eduGAIN

In order to allow interfederational access for researchers, the [eduGAIN](https://edugain.org/) (EDUcation Global Authentication INfrastructure) project in the context of [GEANT](https://www.geant.org/Services) was created. 
From a technical perspective eduGAIN aggregates the data of participating federations and serves the data to relying services.
By participating in the DFN you are free to decide whether your identity provider should also be referenced by eduGAIN.
Any conditions that must be met by the provider are listed on the [DFN eduGAIN page](https://wiki.aai.dfn.de/de:edugain#edugain_interfederation)

## Step 3: Elixir

Elixir unites Europe`s leading life science organisations and offers for services and identity providers an authentication and authorization infrastructure (Elixir-AAI).
The infrastructure offers participating services and identity providers additional functionality like group management or a dataset authorization system. 
The de.NBI Cloud is fully integrated with Elixir AAI. A user can use his university account to access the cloud and any other service provided by de.NBI Cloud.
Elixir lists all idenity providers on a [test page](https://perun.elixir-czech.cz/attribute-check/). If your identity provider is not listed you can contact Elixir AAI support (aai-contact@elixir-europe.org).
