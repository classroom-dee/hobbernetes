## The Project
### 3.9. DBaaS vs DIY
**DB as a service** is a **cloud managed DB** and **the latter** is the one that you **deploy yourself with PV** attached to it.
1. Operation
   |Type|Setup Overhead|Maintenance Overhead|Networking|
   |-|-|-|-|
   |DBaaS|Only need few tweaks|Cloud-managed|Managed VPC + LB|
   |DIY|Image+storageclass+secrets+networking...|Manual|Services+DNS+in/egress|
2. Cost
   |Type|Cost|
   |-|-|
   |DBaaS|Predictable storage + compute + I/O but high baseline|
   |DIY|Lower raw cost but hidden cost can rise from ops and reliability|
3. Availability
   |Type|Scalability|HA|
   |-|-|-|
   |DBaaS|Vertical/horizontal + autoscaling|Multi-AZ replica, auto failover|
   |DIY|Manual resize|DIY replication + quorum|
4. Durability
   |Type|Backup|Recovery|
   |-|-|-|
   |DBaaS|Automated|Cross-region replication/restoration + ease of use|
   |DIY|Manual CronJobs scheduling|Manual replication, multi-region setup|
5. Security
   |Type|Compliance|Measures|
   |-|-|-|
   |DBaaS|Provider-managed|Provider-managed|
   |DIY|Manual audit management|Manual configuration of encryption, firewall, IAM|
6. Freedom
   |Type|Customization|Performance Tuning|
   |-|-|-|
   |DBaaS|Restricted root, limited version and extensions|Limited low-level control|
   |DIY|Full control 🤪|Full control|
7. Use Case Fit
   |Type|Ease of Use|Vendor Lock|Mission Fit|
   |-|-|-|-|
   |DBaaS|Click-and-go level easy|Migration could be a pain|Production where minimal overhead is a must|
   |DIY|You own up to what you have built! 🙀|Portable|Dev env or an optimized prod env where control is chosen over convenience|