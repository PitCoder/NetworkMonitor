# Network Services Management (Network Monitor)

> This repository contains the implementation of a network monitor step by step. All topics viewed during the Network Services Management course 2018-2 ESCOM IPN are covered.

### Content
- Introduction to Network Service Management

- Network Monitoring using SNMP

- Perfomance Monitoring and Failure Detection

- Configuration Management and Server Monitoring

### Introduction to Network Service Management
<p align="justify">
When hundreds or thousands of components (links, bridges, routers, hosts, etc...) are cobbled together by an organization to form a network, it is not surprising that components will occasionally malfunction, network elements will be misconfigured, resources be overutilized, or that network components will simply "break". The network administrator, whose job is to keep the network "up and running" must be able to respond to (and better yet, avoid) such mishaps. With potentially thousands of network components spread out over a wide area, the network administrator in a network operations center (NOC) clearly needs tools to help monitor, manage, and control the network. These tools must offer cover to the following scenarios:

- **Failure of an interface card at a host** 
- **Monitoring traffic to aid in resource development**
- **Detecting rapid changes in routing tables**
- **Monitoring for SLA's (Service Level Agreements)
- **Intrusion Detection**

The ISO states in the well known 7-layer ISO reference model the following five areas that network management must cover:

- **Performance management**
- **Fault management**
- **Configuration management**
- **Accounting management**
- **Security management**

This Network Monitor covers all the previously mentioned scenarios, as well the first 3 areas stated by the ISO. 
</p>

### Network Monitoring using SNMP
<p align="justify">
SNMP has been used in the implementation of this Network Monitor since it provides a framework which makes the communication and information exchange easier between one or more management systems and a number of agents. A SNMP network consists of the following elements:

- **Management Stations**: Elements that manage the network agents.
- **Network Agents**: Passive elements located at host nodes, routers, modems, multiplexors and more, that will be managed.
</p>

#### MIB (Management Information Base)
<p align="justify">
The Management Information Base is a type of database that contains hierarchical information, structured in tree shape of all  the manageable parameters in each device managed in the communications network. Through this database polling of the network agents is possible, allowing monitoring the whole network.

MIB v2.0 has been used in this project, therefore monitoring of the following structural nodes is possible:

- **SYSTEM**: Provides generic information about the managed system.
- **INTERFACES**:  Provides information about the network interfaces that are in the system (Includes statistics of the events).
- **AT**: Provides the link level addresses corresponding to an IP address (This is a legacy node).
- **IP**: Provides information about the IP layer (Includes configuration parameters and statistics).
- **ICMP**: Stores the counters of the in/out ICMP packets.
- **TCP**: Provides information corresponding to the current TCP protocol (Includes configuration parameters, statistics and states).
- **UDP**: Provides information corresponding to the current UDP protocol (Includes configuration parameters, statistics and states).
- **EGP**: Here it is grouped all information corresponding to configuration and operation of the EGP protocol.
- **TRANSMISSION**: Contains many groups that are addressed to different technologies of the link level, that are implemented in the network interfaces of the managed system.
</p>

#### Codebase

#### Screenshots

### Performance Monitoring and Failure Detection

### Configuration Management and Server Monitoring



### Team
> This is the team that made this Network Monitor possible:

<p align="center">
  
| <a href="https://github.com/PitCoder" target="_blank">**Eric Alejandro López Ayala**</a> | <a href="github.com/JoelRomeroJL" target="_blank">**Joel Romero López**</a> |
| :---:| :---:|
| [![Eric Alejandro López Ayala](https://avatars3.githubusercontent.com/u/22123865?s=200&v=2)](https://github.com/PitCoder)  | [![Joel Romero López](https://avatars2.githubusercontent.com/u/43273506?s=200&v=2)](https://github.com/JoelRomeroJL) |
| <p>System Architect and Fullstack Developer</p> | <p>System Architect and Fullstack Developer</p> |

</p>

### License
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](https://github.com/PitCoder/NetworkMonitor/blob/master/LICENSE)

- **[MIT license](https://github.com/PitCoder/NetworkMonitor/blob/master/LICENSE)**
- Copyright 2018 © <a href="https://github.com/PitCoder" target="_blank">Eric Alejandro López Ayala</a>
<a href="https://github.com/JoelRomeroJL" target="_blank">Joel Romero López</a>..
