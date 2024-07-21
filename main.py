import sys
sys.setrecursionlimit(10000000)
import math

class EmbedSeed:
    def __init__(self, n: int, m: int, t: int, seeds: 'list[list[int]]'):
        self.n = n
        self.seeds_count = 2 * n * (n - 1)
        self.m = m
        self.t = t
        self.turn = 0
        self.seeds = seeds
        self.embed_seeds = [[-1] * self.n for _ in range(self.n)]
        self.ranking_seeds = [[-1] * self.m for _ in range(self.seeds_count)]
        self.dist = set()
        self.dir = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        self.dir2 = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
    
    def calculate_embed_seed(self, seeds: 'list[list[int]]', turn: int) -> 'list[list[int]]':
        self.seeds = [[j for j in seeds[i]] for i in range(self.seeds_count)]
        self.turn = turn
        self._pre_process(seeds)
        now = [self.n // 2, self.n // 2]
        self.embed_seeds[self.n // 2][self.n // 2] = self._best_seed_first()
        self.dfs(now, 1)
        return self.embed_seeds

    def dfs(self, now: 'list[int]', mode: int) -> None:
        x, y = now
        for i in range(4):
            nx, ny = x + self.dir[i][0], y + self.dir[i][1]
            if 0 <= nx < self.n and 0 <= ny < self.n and self.embed_seeds[nx][ny] == -1:
                self.embed_seeds[nx][ny] = self._best_seed(self.embed_seeds[x][y])
                self.dfs([nx, ny], 0)
        if mode == 1:
            self.embed_seeds[x-1][y-1] = self._best_seed(self.embed_seeds[x][y])
            self.dfs([x-1, y-1], 0)
        #todo 4方向から埋める種を選ぶように変える -> 斜め方向のときに変わるようになるから
        for i in range(4):
            nx, ny = x + self.dir[i][0], y + self.dir[i][1]
            if 0 <= nx < self.n and 0 <= ny < self.n and self.embed_seeds[nx][ny] == -1:
                self.embed_seeds[nx][ny] = self._best_seed(self.embed_seeds[x][y])
                self.dfs([nx, ny], 0)
                
    def _best_seed(self, seed_num:int) -> int:
        if self.t - self.turn >= 10:
            # 1位の数が多くなるようにする->0のcount
            # minを取った順位が高くなるようにする
            score = [0, 0, -1]#1位の数、minの順位の合計、そのseedの番号
            now_val = self.ranking_seeds[seed_num]
            for i in range(self.seeds_count):
                if i in self.dist or i == seed_num: continue
                temp_val = [min(now_val[j], self.ranking_seeds[i][j]) for j in range(self.m)]
                temp_score = [temp_val.count(0), sum(temp_val), i]
                if score[2] == -1:
                    score = temp_score
                elif temp_score[0] > score[0]:
                    score = temp_score
                elif temp_score[0] == score[0] and temp_score[1] < score[1]:
                    score = temp_score
            self.dist.add(score[2])
            return score[2]
        else:
            # 1位の数が多くなるようにする->0のcount
            # minを取った順位が高くなるようにする
            score = [0, 0, -1]#1位の数、minの順位の合計、そのseedの番号
            now_val2 = self.seeds[seed_num]
            for i in range(self.seeds_count):
                if i in self.dist or i == seed_num: continue
                temp_val2 = [max(now_val2[j], self.seeds[i][j]) for j in range(self.m)]
                temp_score = [0, sum(temp_val2), i]
                if score[2] == -1:
                    score = temp_score
                elif temp_score[0] > score[0]:
                    score = temp_score
                elif temp_score[0] == score[0] and temp_score[1] > score[1]:
                    score = temp_score
            self.dist.add(score[2])
            return score[2]
            
    
    def _best_seed_first(self) -> int:
        # 1位の数が多くなるようにする->0のcount
        # 合計が大きくなるようにする
        score = [0, 0, -1]#1位の数、総合値、そのseedの番号
        for i in range(self.seeds_count):
            if i in self.dist: continue
            temp_val = self.ranking_seeds[i]
            temp_val2 = self.seeds[i]
            temp_score = [temp_val.count(0), sum(temp_val2), i]
            if score[2] == -1:
                score = temp_score
            elif temp_score[0] > score[0]:
                score = temp_score
            elif temp_score[0] == score[0] and temp_score[1] > score[1]:
                score = temp_score
        self.dist.add(score[2])
        return score[2]
    
    def _pre_process(self, seeds: 'list[list[int]]') -> None:
        # 初期化する
        self.embed_seeds = [[-1] * self.n for _ in range(self.n)]
        self.ranking_seeds = [[-1] * self.m for _ in range(self.seeds_count)]
        self.dist = set()
        # 番号を追加する
        for i in range(self.seeds_count):
            seeds[i].append(i)
            
        # ランキングを付ける
        ranking_set = [set() for _ in range(self.m)]
        for i in range(self.m):
            for j in range(self.seeds_count):
                ranking_set[i].add(seeds[j][i])
        ranking_list = [sorted(list(ranking_set[i]), reverse=True) for i in range(self.m)]
        
        for i in range(self.seeds_count):
            for j in range(self.m):
                self.ranking_seeds[i][j] = ranking_list[j].index(seeds[i][j])
    
class Judge:
    def __init__(self, n: int, m: int, t: int, seeds: 'list[list[int]]'):
        self.n = n
        self.seeds_count = 2 * n * (n - 1)
        self.m = m
        self.t = t
        self.seeds = seeds
    
    def output_query(self, embed_seeds: 'list[list[int]]') -> None:
        for i in range(self.n):
            print(" ".join(map(str, embed_seeds[i])), flush=True)
            
    def input_query(self) -> 'list[list[int]]':
        created_seeds = []
        for i in range(self.seeds_count):
            created_seeds.append(list(map(int, input().split())))
        return created_seeds


class Visualizer():
    def __init__(self, n: int, m: int, t: int, seeds: 'list[list[int]]'):
        print("# Visualizer mode", flush=True)
        self.n = n
        self.seeds_count = 2 * n * (n - 1)
        self.m = m
        self.t = t
        self.seeds = seeds
        
    def output_query(self, embed_seeds: 'list[list[int]]') -> None:
        self.embed_seeds = embed_seeds
        for i in range(self.n):
            print(" ".join(map(str, embed_seeds[i])), flush=True)
            
    def input_query(self) -> 'list[list[int]]':
        created_seeds = []
        #横との比較によって生まれるやつ
        created_seeds_yoko = [list(map(str, input().split())) for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n-1):
                seeds = [0 for _ in range(self.m)]
                for k in range(self.m):
                    if int(created_seeds_yoko[i][j][k]) == 0:
                        seeds[k] = self.seeds[self.embed_seeds[i][j]][k]
                    elif int(created_seeds_yoko[i][j][k]) == 1:
                        seeds[k] = self.seeds[self.embed_seeds[i][j+1]][k]
                created_seeds.append(seeds)
        #縦との比較によって生まれるやつ
        created_seeds_tate = [list(map(str, input().split())) for _ in range(self.n-1)]
        for i in range(self.n-1):
            for j in range(self.n):
                seeds = [0 for _ in range(self.m)]
                for k in range(self.m):
                    if int(created_seeds_tate[i][j][k]) == 0:
                        seeds[k] = self.seeds[self.embed_seeds[i][j]][k]
                    elif int(created_seeds_tate[i][j][k]) == 1:
                        seeds[k] = self.seeds[self.embed_seeds[i+1][j]][k]
                created_seeds.append(seeds)
        self.seeds = created_seeds
        return created_seeds
           
        
          
class Solver:
    def __init__(self, n: int, m: int, t: int, seeds: 'list[list[int]]', mode: int):
        print(f"n:{n}, m:{m}, t:{t}", file=sys.stderr)
        self.n = n
        self.seeds_count = 2 * n * (n - 1)
        self.m = m
        self.t = t
        self.seeds = seeds
        self.first_seeds = [[j for j in seeds[i]] for i in range(self.seeds_count)]
        self.mode = mode
        self.embed_seeds_class = EmbedSeed(n, m, t, seeds)
        if mode == 0:
            self.judge = Judge(n, m, t, seeds)
        else:
            self.judge = Visualizer(n, m, t, seeds)

    
    def solve(self) -> int:
        seeds = [[j for j in self.first_seeds[i]] for i in range(self.seeds_count)]
        for turn in range(self.t):
            embed_seeds = self.embed_seeds_class.calculate_embed_seed(seeds, turn)
            self.judge.output_query(embed_seeds)
            seeds = self.judge.input_query()
        return self.score(self.first_seeds, seeds)
    
    def score(self, first_seeds: 'list[list[int]]', last_seeds: 'list[list[int]]') -> int:
        x_list = [0 for _ in range(self.m)]
        for i in range(self.seeds_count):
            for j in range(self.m):
                x_list[j] = max(x_list[j], first_seeds[i][j])
        x = sum(x_list)
        w = 0
        w_list = [0 for _ in range(self.m)]
        for i in range(self.seeds_count):
            if w < sum(last_seeds[i]):
                w = sum(last_seeds[i])
                w_list = [j for j in last_seeds[i]]
        score = round((10 ** 6) * w / x)
        x_list = " ".join(map(str, x_list))
        w_list = " ".join(map(str, w_list))
        print(f'x sum: {x}', file=sys.stderr)
        print(f'x list: {x_list}', file=sys.stderr)
        print(f'w sum: {w}', file=sys.stderr)
        print(f'w list: {w_list}', file=sys.stderr)
        return score        
             
                    
                    
def main():
    #コマンドライン引数がある場合はビジュアライザー用として処理する
    # mode  0: 通常, 1: ビジュアライザー用
    mode = 0
    if len(sys.argv) == 2:
        mode = 1
    n, m, t = map(int, input().split())
    seeds_count = 2 * n * (n - 1)
    seeds = [list(map(int, input().split())) for _ in range(seeds_count)]
    solver = Solver(n, m, t, seeds, mode)
    score = solver.solve()
    print(f"{score}", file=sys.stderr)
    print(f"#total_cost:{score}", flush=True)


if __name__ == "__main__":
    main()
