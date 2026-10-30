---
hide:
  - toc
---

# de.NBI Cloud Wiki

The de.NBI Cloud provides free computing and storage resources for academic life science research in Germany.
This wiki explains how to get access, how to work with your project and what is specific to each cloud site.

[Get started](registration.md){ .md-button .md-button--primary }
[Service status](https://status.cloud.denbi.de/){ .md-button }
[Get help](#get-help){ .md-button }

## What do you want to do?

<div class="grid cards" markdown>

-   :material-rocket-launch-outline:{ .lg .middle } **I'm new to the de.NBI Cloud**

    ---

    Get an account, choose a project type and start your first virtual machine.

    - [Register for an account](registration.md)
    - [Choose a project type](#which-project-type-fits-me)
    - [Apply for a project](portal/allocation.md)
    - Start a virtual machine with [SimpleVM]({{ extra.simplevm_wiki_link }})
      or the [OpenStack quickstart](quickstart.md)

-   :material-account-tie-outline:{ .lg .middle } **I lead a project as Principal Investigator**

    ---

    Approve applications, manage your team and keep your project running.

    - [What a Principal Investigator does](portal/allocation.md#principal-investigator)
    - [Add or remove members](portal/project_overview.md#member-management)
    - [Extend the project or request more resources](portal/modification.md)
    - [Cloud Credits](portal/credits.md)
    - [Acknowledge the de.NBI Cloud and add publications](citation_and_publication.md)
    - [End a project](portal/termination.md)
    - [Terms of use](https://cloud.denbi.de/about/policies/)

-   :material-console:{ .lg .middle } **I want full control with OpenStack**

    ---

    Configure networks, volumes and clusters, and automate them through the API.

    - [OpenStack quickstart](quickstart.md)
    - [Concepts: networks, volumes, images, flavors](Concept/basics.md)
    - [Your cloud site's endpoints and specifics](#find-your-cloud-site)
    - Automation with [Ansible](Tutorials/Ansible/index.md),
      [Terraform](Compute_Center/Heidelberg.md#terraform) and
      [BiBiGrid clusters](Tutorials/BiBiGrid/index.md)
    - [Object storage (S3)](Tutorials/ObjectStorage/index.md)
    - [All tutorials](Tutorials/index.md)

-   :material-shield-lock-outline:{ .lg .middle } **I work with sensitive data**

    ---

    Find out whether and how you can process personal or health data in the de.NBI Cloud.

    - [Sensitive data offering and application process](https://cloud.denbi.de/about/spe/)
    - [What counts as sensitive data](portal/personal_data.md)
    - [Your security responsibilities](security.md#security-aspects-of-cloud-computing)

    State that you will process sensitive data, and which kind, in your project application.

-   :material-school-outline:{ .lg .middle } **I'm running a workshop or course**

    ---

    Provide identical environments for every participant.

    - [Set up a SimpleVM workshop]({{ extra.simplevm_wiki_link }}simple_vm/workshop/)
    - [Public SimpleVM workshops](https://cloud.denbi.de/about/simplevm-workshops/)
    - [Galaxy training infrastructure (TIaaS) in Freiburg](Compute_Center/Freiburg.md#special-infrastructure-for-training-workshops-and-e-learning)

-   :material-kubernetes:{ .lg .middle } **I want to run containers on Kubernetes**

    ---

    Deploy and scale containerised services and workflows.

    - [Kubernetes project type](https://cloud.denbi.de/about/project-types/kubernetes/)
    - [Kubernetes at EMBL](Compute_Center/EMBL.md)
    - [Kubermatic in Berlin](Tutorials/Kubermatic/index.md)
    - [JupyterHub on Kubernetes](Tutorials/JupyterHub/index.md)

-   :material-lifebuoy:{ .lg .middle } **Something isn't working**

    ---

    Check for known problems first, then contact the right support team.

    - [Service status](https://status.cloud.denbi.de/) and
      [maintenance announcements](https://cloud.denbi.de/news/facility-news/)
    - [I can't access my virtual machine](FAQ.md#i-cannot-access-my-virtual-machine)
    - [My project is about to expire](FAQ.md#my-project-is-about-to-expire-can-i-extend-it-what-happens-to-my-virtual-machines)
    - [I need more Cloud Credits](portal/credits.md#requesting-more-cloud-credits)
    - [All frequently asked questions](FAQ.md)
    - [Who to contact](#get-help)

-   :material-server-network:{ .lg .middle } **I administer a cloud site**

    ---

    Guides for de.NBI Cloud site administrators.

    - [Project management](cloud_admin/project_management.md)
    - [News management](cloud_admin/news_management.md)
    - [Vault management](cloud_admin/vault_admin.md)
    - [LifeScience AAI for OpenStack](cloud_admin/elixir_OIDC.md)
    - [Register your identity provider](cloud_admin/identity_provider.md)

</div>

## Which project type fits me?

|                         | SimpleVM                                              | OpenStack                                                      | Kubernetes                                          |
|-------------------------|-------------------------------------------------------|----------------------------------------------------------------|-----------------------------------------------------|
| **Good for**            | Single VMs, remote desktops, RStudio, workshops       | Custom networks, clusters, API automation, hosting services    | Containerised services and workflows                |
| **Cloud experience**    | None needed                                           | Linux and basic networking                                     | Containers and Kubernetes                           |
| **Documentation**       | [SimpleVM wiki]({{ extra.simplevm_wiki_link }})       | [OpenStack quickstart](quickstart.md)                          | [Kubernetes at EMBL](Compute_Center/EMBL.md)        |
| **Support**             | Cloud Portal Helpdesk                                 | Your cloud site                                                | Your cloud site                                     |

See the [project type comparison](https://cloud.denbi.de/about/project-types/) for details.
If you are unsure, start with SimpleVM or ask the [Cloud Portal Helpdesk](#get-help).

## Find your cloud site

The portal assigns each project to one of the de.NBI Cloud sites.
You can see yours as **Facility** on the [project overview](portal/project_overview.md) page in the
[de.NBI Cloud Portal](https://cloud.denbi.de/portal/).
The site pages describe login, networks, storage and API access for OpenStack and Kubernetes projects.

<div class="grid cards" markdown>

-   :material-map-marker-outline: [Berlin](Compute_Center/Berlin.md)
-   :material-map-marker-outline: [Bielefeld](Compute_Center/Bielefeld.md)
-   :material-map-marker-outline: [EMBL Heidelberg](Compute_Center/EMBL.md)
-   :material-map-marker-outline: [Freiburg](Compute_Center/Freiburg.md)
-   :material-map-marker-outline: [Giessen](Compute_Center/Giessen.md)
-   :material-map-marker-outline: [Heidelberg University](Compute_Center/Heidelberg.md)
-   :material-map-marker-outline: [Heidelberg DKFZ](Compute_Center/Heidelberg-DKFZ.md)
-   :material-map-marker-outline: [Tübingen](Compute_Center/Tuebingen.md)

</div>

## Get help

1. **Check for known problems.** Outages and maintenance are announced on the
   [status page](https://status.cloud.denbi.de/) and in the
   [facility news](https://cloud.denbi.de/news/facility-news/).
2. **Contact the right team.**
    - **SimpleVM projects, the portal, applications and general questions:** Cloud Portal Helpdesk,
      [cloud-helpdesk@denbi.de](mailto:cloud-helpdesk@denbi.de)
    - **OpenStack and Kubernetes projects:** the support team of your cloud site.

    For an existing project, **Contact Support** under **Facility** on the
    [project overview](portal/project_overview.md) page opens an email to the right team.
    All contact addresses are listed on the [support page](https://cloud.denbi.de/support/).
