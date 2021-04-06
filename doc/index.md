# Guidelines for operating large stake pools

This section provides guidelines for operators of large stake pools, specifically how to manage the risks and complexity of maintaining significant stake or multiple pools. Operators of smaller stake pools may also find much of this advice useful to them.

## Main recommendations

1. **Consider reliability and robustness**. Stake pools require high-reliability servers with:
    + Resilient compute capability.
    + Robust networking capability.
2. **Consider networking requirements** carefully:
    + High bandwidth connections are essential to run a relay node (e.g., 5 Mbit/s + 0.1 Mbit/s per downstream peer as a capacity planning number).
3. **Operate sufficient relay nodes** as well as stake pools:
    + Relay nodes are necessary for the maintenance of the network.
    + Provision two relay nodes for each active stake pool.
4. **Be aware of system and network performance**, especially if using virtualized or shared servers:
    + Each stake pool may need its own dedicated hardware resources (compute, memory, and network).
    + It is recommended to use different servers for stake pools and relay nodes.
    + Virtualization may complicate the process of determining whether stake pools have adequate resources.
5. **Do not replicate stake pools** on the network:
    + Stake pool replication is adversarial behavior, which may lead to blocks being rejected.
    + Use high-reliability techniques to switch between duplicate or back-up servers without exposing both simultaneously to the network.
6. **Stake pools should have limited network connections**:
    + This reduces stake pool exposure to denial-of-service (DOS) attacks and improves performance.
    + Relay nodes should handle the larger portion of network traffic.
    + Stake pools should only be connected to trusted nodes (relay and/or stake generating).
    + Stake pools and relay nodes should restrict the services that are exposed (e.g., using a firewall).
7. **Security is paramount**:
    + Use *airgapping* when signing transactions – do not store cold keys on an online server (including the one that is running a stake pool or a relay node).
    + Use hardware wallets for high-value private keys, where possible.
    + Where private keys cannot be stored in hardware wallets (e.g., cold keys), store them offline.
    + Be aware of and plan for enforced key rotations using the key evolving signature (KES) scheme. 

## Managing risks and complexity

Operating stake pools effectively is crucial to ensure the long-term health and liveliness of decentralization on Cardano. When a stake pool operator (SPO) operates multiple stake pools (or has a single pool that directly controls a significant percentage of the total staked ada), they may have a significant effect on the overall system throughput as a consequence of the “proof-of-stake” principle. 

The Cardano design and security analysis assume that each stake pool operates in a broadly independent and mutually supportive (non-adversarial) manner. This means that large SPOs have a particular responsibility to ensure that their operation supports the needs of the network as a whole. For this, it is essential to evaluate and address common risks that may be experienced in stake pool operations. 

**Virtualization and containerization risks**

Because stake pools and relay nodes have specific real-time requirements, it is generally not recommended to run Cardano nodes on virtualized resources without undertaking careful performance, reliability, and security analyses. The mapping of Cardano nodes to the underlying physical infrastructure must consider timing issues for block production and propagation.

**Security and common-mode failures**

The risks of operating a stake pool using container-based virtualization include increased chances of common-mode system failures, resource contention, and increased exposure to security risks (including DOS attacks and loss of private keys). The use of containerized environments, where relay nodes share the same physical infrastructure as stake pool nodes, may impact real-time requirements on block production and networking infrastructure, thus reducing stake pool income. Moreover, concentrating network connections (as may happen with virtualized or containerized services) increases the chances of a DOS attack, as well as reduces network redundancy in non-obvious ways. In a virtualized or shared environment, a single NIC/cable failure or DOS attack, for instance, might then affect multiple stake pools or relay nodes, including those that might be run by different SPOs.

**Shared resources**

The diffusion of a newly minted block causes a “pulse” of activity to occur. Stake pools and relay nodes that share physical computing resources will be forced to compete for shared CPU, memory, storage, networking, and other resources. The demand for these resources is not smooth, it is correlated by the block diffusion. This can negatively affect block production or result in blockchain synchronization failures. Under some conditions, performance can degrade in a non-linear way (e.g., adding a second node may reduce performance by more than 50%). To eliminate such risks, it is important to analyze performance requirements not only for the typical load but also for limit cases. 

**Maintenance and upgrade**

System maintenance and upgrades should be always taken into consideration. Although migration of a virtualized instance to new hardware, or duplication of a running instance might seem easy, this commonly results in some timing disruption. This is more significant in a real-time setting (such as Cardano) than for typical data processing applications, which often have high levels of replication and redundancy. System upgrades may also have unexpected effects on the virtualized system’s performance, or occasionally, functionality. SPOs, therefore, need to be aware of underlying system maintenance and take appropriate action to avoid losing blocks (and income).

**Geographical and physical concentration**

Virtualized systems are often concentrated into a few large data centers. This creates potential points of common network failures, including reliance on specific portions of national infrastructures (internet backbones, power grids, etc). Large SPOs should aim to disperse their operations across multiple regions, and very large operators should aim for a global presence.

## Provisioning

To ensure overall network resilience and robustness, SPOs that operate large stake pools must take special care of:

**Stake pool configuration**

1. Network configurations should ensure sufficient connectivity to other stake pools (including those that are run by other operators).  
2. The effects of virtualization should be considered carefully: given the pulsed-nature of block diffusion, it is easy to overload physical compute, memory, and networking resources. Unlike a typical database or web service operation, Cardano stake pools have real-time compute and networking requirements. Failure to observe these requirements may have an impact on stake pool returns. It is generally not recommended to share server resources between multiple stake pools or relay nodes.
3. Stake pools should always be supported by sufficient relay nodes (two or more). This reduces the risk of a single relay node failure, which can potentially isolate a block-producing node. Failure of a block-producing node should only affect block production for that single stake pool. It is particularly important that large SPOs take on this responsibility since they are receiving a higher proportion of the operating rewards for the network.
4. To support the relay capacity scaling, it is desirable to use DNS names that map to multiple IP addresses and/or use multiple on-chain DnsName entries. Ideally, these entries should be supported over disjointed network infrastructure (e.g., different ISPs or physical paths).

**Security preferences**

1. Cold keys should never be stored on active servers (especially cloud servers).
2. Payment keys should be kept separate from block signing keys. Airgaps should be maintained between stake pools and systems used for transaction signing.
3. Hardware wallets or other secure means should be used to protect cold keys. One hardware wallet may be needed per set of keys (e.g., per stake pool), and these may need to be physically secured.
4. Back-up keys should be also securely maintained for each stake pool.

**General advice**:

1. Consider hardware performance, including memory, storage, and networking capabilities.
2. Perform failure-mode-effects analysis to ensure that single failures of a delivery component are suitably constrained.
3. Carefully consider containerization and virtualization performance to eliminate excessive contention for common resources (e.g., CPU cores).
4. Submit stake pool certificates that include both the IP address and DNS names.
5. Ensure that suitable monitoring is in place:
    + Receiving the vast majority of (>90%) blocks within 4,000ms of their associated slot time.
    + Track block production times to ensure that allocated resources remain sufficient (this will increase as transaction rates and block sizes increase).
6. Plan the expansion of relay nodes (potentially at a different location) that are associated with your stake registration (DDoS mitigation / rapid increases in load due to increase of delegation to SPO’s stake pools, etc.).
7. Plan for regular maintenance events (to minimize stake pool downtime and/or to perform maintenance when the leadership schedule indicates a good interval).
8. Plan and exercise disaster recovery every 3 to 6 months.
9. When operating multiple stake pools, spread out your block producer nodes across multiple continents to limit block production disruption and eliminate large-scale network outages.

### Example system and relay topology configurations

There is no standard system configuration as every stake pool has different operational requirements and preferences. It is the choice of an SPO on how to configure the topology. 

However, taking into account the earlier advice, it is recommended that an SPO maintains at least two and an additional relay node(s) per a stake pool. In the case of running multiple stake pools, it is best that SPOs use geographically diverse peers, spread relay nodes across the world, and reach out to other SPOs (particularly other large ones) making agreements to add each other's relay nodes. The more SPOs they have peer-sharing agreements with, the more likely their blocks will propagate and get included in the chain. 

Monitoring is important for all SPOs, and it is essentially a responsibility of an operator to ensure the quality of their pools’ functionality. As an example of a monitoring process that reflects Prometheus rules alerting on thresholds, one can take a look at the [cardano-ops repository here](https://github.com/input-output-hk/cardano-ops/blob/master/modules/monitoring-cardano.nix#L13).

**Example relay topology**

*Please note that IOHK relay nodes are outlined as examples.* 

```
{
  "Producers": [
	{
  	"addr": "north-america.relays-new.cardano-mainnet.iohk.io",
  	"port": 3001,
  	"valency": 4
	},
	{
  	"addr": "asia-pacific.relays-new.cardano-mainnet.iohk.io",
  	"port": 3001,
  	"valency": 4
	},
	{
  	"addr": "europe.relays-new.cardano-mainnet.iohk.io",
  	"port": 3001,
  	"valency": 4
	}
  ]
}
```

### Node configuration options

The `MaxConcurrencyDeadline` configuration option controls how many attempts the node will run in parallel to fetch the same block. Considering that getting the same block as soon as possible is important for both relay nodes and block producer nodes, we recommend setting the MaxConcurrencyDeadline value to 8.

## Delegation and pledging advice

**Delegation**

Stake delegation is the process of allocating individual stakeholders’ funds to collective stake pools. Delegation is performed for block production purposes to ensure that the block creation complies with the *proof-of-stake* consensus. By delegating, stakeholders do not transfer stake ownership, voting or other rights. 

Large SPOs will generally control a significant amount of third-party stake to maintain trust in the blockchain, thus being responsible for:

+ producing blocks
+ processing transactions
+ maintaining the Cardano network
+ ensuring that the owner pledge is made
+ securing the pool (e.g., protecting its private keys)
+ providing public communications about the pool, including retirement announcements, changes in pricing or other pool parameters.

Large operators are not responsible for distributing block production rewards to delegators as this is handled automatically by the blockchain. SPOs are also not responsible for securing delegator keys or taking delegation, voting, or other actions on behalf of stakeholders. Individual stakeholders must take personal responsibility for their own security and must make their own decisions in terms of delegation, voting, etc.

**Pledging**

Pledging is an important mechanism for producing Cardano’s healthy ecosystem. SPOs may opt to pledge some, or all, of their ada to the pool in order to make it more attractive to other delegators, and thus to grow the size of the pool as a whole. Pledged ada may be supplied either by an SPO or by other owners.

**Pledging rewards**

Pledge influences the rewards that a stake pool can earn, and thus the rewards that delegators can obtain from the pool. The pledging amount may be specified, if desired, during the pool registration, and can then be changed on an epoch-by-epoch basis. No minimum pledge is required, however, there is also no maximum pledge.

Given two equivalent stake pools, the one with the greater pledge will earn more rewards, and therefore be more attractive to other delegators. However, the SPO or other pool owners should collectively meet the pledge by delegating. It is also important to ensure that there are enough funds in addresses that use the pool owner's address(es) as stake reference. **Failure to meet the pledge** will mean that no rewards can be earned for the pool by any owner or delegator. This will generally result in loss of delegation and *perhaps* pool collapse.

*Unlike delegation, the SPO is responsible for distributing all pledging rewards. This may be done in any agreed manner and is not enforced by the blockchain*.

Collective stake pool operation (maintained by an operator and a group of owners, pledging their stake) requires mutual trust and is a good way to build a larger pool while sharing the risks and rewards. 

**Defense against Sybil attacks**

The pledging mechanism is designed to mitigate against [Sybil attacks](https://iohk.io/en/blog/posts/2018/10/29/preventing-sybil-attacks/), which could theoretically allow a proof-of-stake network to be taken over without supplying a significant personal stake. By making pools with higher pledges more attractive, such attacks are prevented. The pledge formula is designed so that a pool with a higher pledge will produce higher rewards and thus become more attractive. To conduct a Sybil attack, an adversary must divide their pledge amongst a large number of pools. Since this will dilute each pool pledge, delegators will be motivated by the rewards mechanism to re-delegate to non-adversarial pools.





















