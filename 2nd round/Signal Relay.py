import heapq

# Problem 4: Signal Relay (medium)
#
# n relay robots (numbered 0 to n-1) are linked by two-way cables:
#   links[i] = (u, v, latency_ms)  -> a cable between u and v that takes latency_ms
#
# Each relay also has a processing delay: delay[i] ms.
# A relay adds its delay whenever a signal PASSES THROUGH it.
# The source and destination do NOT add their own delay.
#
# Return the minimum time (ms) for a signal to get from src to dst, or -1 if unreachable.
#
# Example 1:
#   n = 4
#   links = [(0, 1, 1), (1, 3, 1), (0, 2, 2), (2, 3, 2)]
#   delay = [0, 10, 1, 0]
#   src = 0, dst = 3
#   -> 5
#   (0 -> 1 -> 3 = 1 + 10 + 1 = 12;  0 -> 2 -> 3 = 2 + 1 + 2 = 5)
#
# Example 2:
#   n = 3
#   links = [(0, 1, 4), (1, 2, 4)]
#   delay = [100, 1, 100]
#   src = 0, dst = 2
#   -> 9
#   (4 + 1 + 4; relays 0 and 2 are the ends, so their delays don't count)
#
# Example 3:
#   n = 3
#   links = [(0, 1, 5)]
#   delay = [0, 0, 0]
#   src = 0, dst = 2
#   -> -1
#   (relay 2 isn't connected to anything)
#
# Example 4:
#   n = 2
#   links = [(0, 1, 7)]
#   delay = [3, 3]
#   src = 1, dst = 1
#   -> 0
#   (already there)
#
# Constraints:
#   - 1 <= n <= 10,000
#   - 0 <= len(links) <= 50,000
#   - all latencies and delays are >= 0
#
# Think about: your Network Delay Time template handles edge weights.
# Where does a relay's delay fit in? Could you fold it into the edge cost somehow?
# Careful with the "source and destination don't add their delay" rule.


def min_signal_time(n, links, delay, src, dst) -> int:

    # here we can do djikstras i believe but include the delay time in the processing when pushing onto the minheap
    # build adj list with both directions

    adj = {i: [] for i in range(n)}

    for node, dest, weight in links:
        adj[node].append([dest, weight])
        adj[dest].append([node, weight])

    minHeap = [[0, src]]

    visited = set()

    while minHeap:

        w1, n1 = heapq.heappop(minHeap)

        if n1 == dst:
            return w1

        node_delay = 0
        if n1 != src and n1 != dst:
            node_delay = delay[n1]

        if n1 in visited:
            continue

        visited.add(n1)

        for n2, w2 in adj[n1]:
            if n2 not in visited:
                heapq.heappush(minHeap, [w1+w2+node_delay, n2])

    return -1
