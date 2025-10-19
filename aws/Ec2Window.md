# Ec2Window

Features

- 虚拟计算环境instances
- instances的配置模板，AMIs，包括操作系统和附加软件
- instance-type：不同的CPU、memory、storage和networking capacity的配置
- intance安全登录信息 key-pairs（Aws存储公钥，你存储私钥）
- 临时数据存储容量，它们在停止或终止instance时删除，instance store volumes
- 持久存储容量，Amazon Elastic Block Store（EBS volumes）
- 资源（Ec2，EBS）的多物理位置，Regions和Availablity Zones
- 防火墙，指定到达instance的protocols、ports和source IP范围，使用security groups
- 静态IPv4地址，Elastic IP addresses
- 元数据，tags，创建并赋予Ec2资源
- 创建与Aws cloud其他部分隔离的虚拟网络，virtual private clouds（VPCs）