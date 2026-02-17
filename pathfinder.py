import matplotlib.pyplot as plt
import numpy as np
import collections
import heapq

class AIPathfinder:
    def __init__(self, grid_size=10):
        self.grid_size = grid_size
        self.grid = np.zeros((grid_size, grid_size))
        
        # Mandatory Movement Order
        # 1.Up, 2.Right, 3.Bottom, 4.Bottom-Right, 5.Left, 6.Top-Left
        self.moves = [(-1, 0), (0, 1), (1, 0), (1, 1), (0, -1), (-1, -1)]
        
        self.start = (7, 7)
        self.target = (8, 1)
        self.grid[2:8, 5] = -1  # Static wall

    def is_valid(self, pos):
        r, c = pos
        return 0 <= r < self.grid_size and 0 <= c < self.grid_size and self.grid[r, c] != -1

    def visualize(self, current, frontier, explored, algorithm_name, path=None):
        """GUI """
        plt.clf()
        plt.gcf().set_facecolor('#ffe6f2')  # soft baby pink background
        
        # Soft lavender grid
        plt.imshow(self.grid, cmap='Pastel2', origin='upper')
        
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                plt.text(c, r, str(int(self.grid[r, c])), 
                         va='center', ha='center', 
                         color='#cc6699', alpha=0.4)

        # Explored nodes – light pink squares
        if explored:
            ex_r, ex_c = zip(*explored)
            plt.scatter(ex_c, ex_r, color='#ff99cc', marker='s', s=200, alpha=0.6)
            
        # Frontier – soft purple circles
        if frontier:
            f_coords = [n[1] if isinstance(n, tuple) and len(n) == 2 else n for n in frontier]
            f_nodes = [n for n in f_coords if isinstance(n, tuple)]
            if f_nodes:
                fr_r, fr_c = zip(*f_nodes)
                plt.scatter(fr_c, fr_r, color='#cc99ff', marker='o', s=120)

        # Final path – bright magenta line
        if path:
            p_r, p_c = zip(*path)
            plt.plot(p_c, p_r, color='#ff3399', linewidth=4)

        # Start and Target styling
        plt.text(self.start[1], self.start[0], 'S', 
                 color='white', weight='bold',
                 ha='center', va='center',
                 bbox=dict(facecolor='#ff66b2', boxstyle='round'))

        plt.text(self.target[1], self.target[0], 'T', 
                 color='white', weight='bold',
                 ha='center', va='center',
                 bbox=dict(facecolor='#9966ff', boxstyle='round'))
        
        plt.title(f"{algorithm_name}  24F-0652_24F-0573", color='#cc0066')
        plt.pause(0.01)

    def get_path(self, parent_map, target_node):
        path = []
        curr = target_node
        while curr is not None:
            path.append(curr)
            curr = parent_map.get(curr)
        return path[::-1]

    # --- ALGORITHMS  ---

    def bfs(self):
        queue = collections.deque([self.start])
        parent_map = {self.start: None}
        explored = []
        plt.figure(figsize=(7,7))
        while queue:
            current = queue.popleft()
            if current == self.target:
                self.visualize(current, queue, explored, "BFS", self.get_path(parent_map, self.target))
                plt.show(); return
            if current not in explored:
                explored.append(current)
                for dr, dc in self.moves:
                    neighbor = (current[0]+dr, current[1]+dc)
                    if self.is_valid(neighbor) and neighbor not in parent_map:
                        parent_map[neighbor] = current
                        queue.append(neighbor)
                self.visualize(current, queue, explored, "BFS")

    def dfs(self, limit=None):
        stack = [(self.start, 0)]
        parent_map = {self.start: None}
        explored = []
        plt.figure(figsize=(7,7))
        while stack:
            current, depth = stack.pop()
            if current == self.target:
                self.visualize(current, stack, explored, "DFS/DLS", self.get_path(parent_map, self.target))
                plt.show(); return True
            if current not in explored:
                if limit is None or depth < limit:
                    explored.append(current)
                    for dr, dc in reversed(self.moves):
                        neighbor = (current[0]+dr, current[1]+dc)
                        if self.is_valid(neighbor) and neighbor not in parent_map:
                            parent_map[neighbor] = current
                            stack.append((neighbor, depth + 1))
                    self.visualize(current, stack, explored, "DFS/DLS")
        plt.close(); return False

    def ucs(self):
        pq = [(0, self.start)]
        parent_map = {self.start: None}
        cost_map = {self.start: 0}
        explored = []
        plt.figure(figsize=(7,7))
        while pq:
            cost, current = heapq.heappop(pq)
            if current == self.target:
                self.visualize(current, [n[1] for n in pq], explored, "UCS", self.get_path(parent_map, self.target))
                plt.show(); return
            if current not in explored:
                explored.append(current)
                for dr, dc in self.moves:
                    neighbor = (current[0]+dr, current[1]+dc)
                    if self.is_valid(neighbor) and (neighbor not in cost_map or cost+1 < cost_map[neighbor]):
                        cost_map[neighbor] = cost + 1
                        parent_map[neighbor] = current
                        heapq.heappush(pq, (cost+1, neighbor))
                self.visualize(current, [n[1] for n in pq], explored, "UCS")

    def iddfs(self):
        for depth in range(self.grid_size * self.grid_size):
            print(f"Searching at depth limit: {depth}")
            if self.dfs(limit=depth): return

    def bidirectional(self):
        f_q, b_q = collections.deque([self.start]), collections.deque([self.target])
        f_parent, b_parent = {self.start: None}, {self.target: None}
        f_explored, b_explored = [], []
        plt.figure(figsize=(7,7))
        while f_q and b_q:
            curr_f = f_q.popleft()
            f_explored.append(curr_f)
            for dr, dc in self.moves:
                adj = (curr_f[0]+dr, curr_f[1]+dc)
                if self.is_valid(adj) and adj not in f_parent:
                    f_parent[adj] = curr_f; f_q.append(adj)
                    if adj in b_parent:
                        path = self.get_path(f_parent, adj) + self.get_path(b_parent, adj)[::-1][1:]
                        self.visualize(adj, list(f_q)+list(b_q), f_explored+b_explored, "Bidirectional", path)
                        plt.show(); return
            curr_b = b_q.popleft()
            b_explored.append(curr_b)
            for dr, dc in self.moves:
                adj = (curr_b[0]+dr, curr_b[1]+dc)
                if self.is_valid(adj) and adj not in b_parent:
                    b_parent[adj] = curr_b; b_q.append(adj)
                    if adj in f_parent:
                        path = self.get_path(f_parent, adj) + self.get_path(b_parent, adj)[::-1][1:]
                        self.visualize(adj, list(f_q)+list(b_q), f_explored+b_explored, "Bidirectional", path)
                        plt.show(); return
            self.visualize(curr_f, list(f_q)+list(b_q), f_explored+b_explored, "Bidirectional")

def menu():
    pf = AIPathfinder()
    while True:
        print("AI Pathfinder Menu\n")
        print("1. BFS  2. DFS  3. UCS  4. DLS  5. IDDFS  6. Bidirectional  7. Exit")
        choice = input("Select Algorithm: ")
        if choice == '1': pf.bfs()
        elif choice == '2': pf.dfs()
        elif choice == '3': pf.ucs()
        elif choice == '4': pf.dfs(limit=5)
        elif choice == '5': pf.iddfs()
        elif choice == '6': pf.bidirectional()
        elif choice == '7': break

if __name__ == "__main__":
    menu()

