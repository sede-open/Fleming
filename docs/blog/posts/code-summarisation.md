---
date: 2025-01-13
authors:
  - GBBBAS
---

# Introducing Project Fleming: Enhancing Code Reuse and Efficiency with AI Discovery

<center>
![code_summary](../images/code_summary.png){width=75%} 
</center>


We are delighted to announce the release of an enhancement to Project Fleming, with the addition of the Code Summary functionality. Once code has been summarised, this can be passed into Project Fleming's corpus to improve search for specific code functionality. 
 
<!-- more -->

## Code Summary

The purpose of the Code Summary package is to improve a user's search for explicit code functionality, by utilising LLMs to ingest source code of repositories and generate comprehensive and descriptive documentation, that can then be indexed by Project Fleming and consequently improving the quality of results.
 
The initial use-case of Project Fleming was to ingest repository readme contents into the search index, thereby allowing users to perform natural language searches, based off the information provided in the readme file by the developers. However, this was inherently limited by the fact it was reliant on the developer producing a descriptive readme. Furthermore, in some cases developers are unable to write a full functional description of all their code within a larger repository, as they are (reasonably) trying to give a high level overview of the entire project, instead of detailing specific code functionality.
 
Enter Project Fleming's Code Summary Package, which can be tailored to generate descriptive code functionality documentation for repositories, thus increasing the likelihood that specific code relevant to the users query is found when this documentation is ingested into the search index of Project Fleming. This use of LLMs is designed to allow users to find reusable code, that may have been previously hidden by the domain context it is situated in, as it is no longer reliant on the specific functionality being described in the readme.

## Further applications
 
We see this as having multiple applications, not only to enhance the findability of reusable code, but also to help organisations with large-scale code scanning to find specific types of projects. For example, the Code Summary package could be used to identify AI projects, which could then be assessed to see if they are compliant with the local regulations. This is only one of many potential applications, and as always, we actively welcome feedback and further contributions to further enhance Project Fleming.