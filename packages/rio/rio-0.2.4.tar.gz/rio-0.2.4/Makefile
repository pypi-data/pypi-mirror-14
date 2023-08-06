# CLUSTER REDIS NODES
define NODE1_CONF
daemonize yes
port 7000
cluster-node-timeout 5000
pidfile /tmp/redis_cluster_node1.pid
logfile /tmp/redis_cluster_node1.log
save ""
appendonly no
cluster-enabled yes
cluster-config-file /tmp/redis_cluster_node1.conf
endef

define NODE2_CONF
daemonize yes
port 7001
cluster-node-timeout 5000
pidfile /tmp/redis_cluster_node2.pid
logfile /tmp/redis_cluster_node2.log
save ""
appendonly no
cluster-enabled yes
cluster-config-file /tmp/redis_cluster_node2.conf
endef

define NODE3_CONF
daemonize yes
port 7002
cluster-node-timeout 5000
pidfile /tmp/redis_cluster_node3.pid
logfile /tmp/redis_cluster_node3.log
save ""
appendonly no
cluster-enabled yes
cluster-config-file /tmp/redis_cluster_node3.conf
endef

export NODE1_CONF
export NODE2_CONF
export NODE3_CONF


start_redis_cluster: cleanup_redis_cluster
	echo "$$NODE1_CONF" | redis-server -
	echo "$$NODE2_CONF" | redis-server -
	echo "$$NODE3_CONF" | redis-server -

cleanup_redis_cluster:
	- rm -vf /tmp/redis_cluster_node*.conf 2>/dev/null
	- rm -f /tmp/redis_cluster_node1.conf
	- rm dump.rdb appendonly.aof - 2>/dev/null

stop_redis_cluster:
	kill `cat /tmp/redis_cluster_node1.pid` || true
	kill `cat /tmp/redis_cluster_node2.pid` || true
	kill `cat /tmp/redis_cluster_node3.pid` || true
	make cleanup_redis_cluster
