# Network Services Management (Network Monitor)

> This repository contains the implementation of a network monitor step by step. All topics viewed during the Network Services Management course 2018-2 ESCOM IPN are covered.

### Content
- Introduction to Network Service Management

- Network Monitoring using SNMP

- Perfomance Monitoring and Failure Detection

- Configuration Management and Server Monitoring

### Introduction to Network Service Management


### Network Monitoring using SNMP
<p align="justify">
SNMP has been used in the implemenation of this Network Monitor since it provides a framework which makes the communication and information exchange easier between one or more management systems and a number of agents. A SNMP network consists of the following elements:

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

| <a href="https://github.com/PitCoder" target="_blank">**Eric Alejandro López Ayala**</a> | <a href="github.com/JoelRomeroJL" target="_blank">**Joel Romero López**</a> |
| :---:| :---:|
| [![Eric Alejandro López Ayala](https://avatars3.githubusercontent.com/u/22123865?s=200&v=2)](https://github.com/PitCoder)  | [![Joel Romero López](https://avatars2.githubusercontent.com/u/43273506?s=200&v=2)](https://github.com/JoelRomeroJL) |
| <p>System Architect and Fullstack Developer</p> | <p>System Architect and Fullstack Developer</p> |

### License
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](https://github.com/PitCoder/NetworkMonitor/blob/master/LICENSE)

- **[MIT license](https://github.com/PitCoder/NetworkMonitor/blob/master/LICENSE)**
- Copyright 2018 © <a href="https://github.com/PitCoder" target="_blank">Eric Alejandro López Ayala</a>
<a href="https://github.com/JoelRomeroJL" target="_blank">Joel Romero López</a>..
