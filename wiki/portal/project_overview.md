In the sidebar under "Project Management" all projects you are a member of are listed. By clicking on the corresponding
project you will get to the project overview page, which contains all information about the project as well as the
possibility of adjustments.

![project_overview](img/project_overview.png)

### Quick overview

If the evaluation of your project application is not yet completed, the current status can be seen here. Depending on
the project type, several steps are necessary for the evaluation of the application, which are visible in the progress
display. If you move the mouse over a step in the display, more information will be shown.

![application_progress](img/application_progress.png)

The evaluation of the application is divided into the following steps:

* Submitting the application

* Approval of the Principal Investigator: The application must be submitted or confirmed by the responsible principal
  investigator

* Confirmation by the Cloud committee: The application must be approved by the committee of the de.NBI Virtual
  Organization

* **Only for OpenStack projects** - Approval of the Facility Manager: The application must be confirmed by the facility
  manager of the compute center to which their project was assigned by the VO

The upper part of the overview page summarizes the most important information about the project. This information
includes the runtime and the number of available virtual machines. In addition, the support of the project location
where the project is running can be contacted directly. It is possible
to [request extensions or resource modifications](modification.md) directly from the overview. With a click on "Show
more information" all further project information and currently requested changes/extensions can be displayed.
You are also able to [terminate your project](termination.md).

### Member management

In the area "Members of the Project" all members of the project can be viewed if granted by the administrators. Project administrators are also able to

* Invite further members

* Accept/reject member applications for the project

* Remove existing members from the project

* Promote members to administrators or revoke their status

* Adjust the visiblity of member names

* Prevent the starting of machines by non-administrator


!!! note ""
    Adding members to projects is now exclusively possible via invitation links.

You'll find an invitation link within the "Add Members" Modal, which you can send to desired individuals. These individuals must then register for a LifeScienceAAI and a de.NBI Cloud account. Once the invited person has completed this process and applied for your project, the project administrators will be notified via email. Subsequently, you can confirm or decline the addition of these individuals to the project under "Member Applications".
By default, only admins of a project see all project members. This option can be disabled and re-enabled by admins using
the "Show/Hide Member Names" button (as seen below). If the option is enabled, this is also indicated by a "(hidden)"
next to "Full Name" in the header of the member table.

Also all project members are able to start machines as soon as the project resources are available.
However, the startup of machines by participants of workshops who are not administrators is suspended by default.
Administators of SimpleVM projects are able to prevent machines from being started by non-administrators or to allow this again after the restriction has been made. The "Allow/Prevent starting of machines" button can be used for this purpose.

![member_overview](img/show_hide_members.png)

### Leaving a Project

It is possible for all project members except the PI to leave a project at any time by clicking the "Leave Project"
button in the project overview.

![leave_project](img/leaving_project.png)

The PI cannot leave the project as she/he is responsible for it. In order to leave the project, the PI must
contact <a href="mailto:cloud-helpdesk@denbi.de">cloud-helpdesk@denbi.de</a>  and clarify which person will take over further
responsibility for the project.

### Publications

Project administrators can add DOIs of publications that are related to the current project so that they are published
on the de.NBI cloud page. You can find more information on this topic [here](../citation_and_publication.md).
