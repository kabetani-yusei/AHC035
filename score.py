import subprocess
import sys
import datetime

# テストケースの範囲（0から99まで）
start_case = 0
end_case = 99

total_cost = 0
min_score = 100000000000000000
max_score = 0

#時間を書き込む
with open("result.txt", "a") as f:
    now = datetime.datetime.now()
    filename = now.strftime("%m月%d日 %H時%M分%S秒")
    f.write(f"{filename}\n")

for i in range(start_case, end_case):
    input_file = f"./in/{i:04d}.txt"
    output_file = f"./out/{i:04d}.txt"

    # main.rbの実行
    result = subprocess.run(["python", "main.py", "vismode"], stdin=open(input_file, "r"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # 結果の出力
    if result.returncode == 0:
        # 各ケースのスコアを取得し合計に加える
        try:
            cost_line = result.stdout.strip().split('\n')[-1]
            cost = int(cost_line.split(':')[-1])
            min_score = min(min_score, cost)
            max_score = max(max_score, cost)
            total_cost += cost
            #print(f"Test case {i:04d}: cost = {cost}")
        except (ValueError, IndexError):
            print(f"Failed to process {input_file}")
            sys.exit(1)
    else:
        print(f"Failed to process {input_file}")
        sys.exit(1)

    # 結果をファイルに書き込む
    with open(output_file, "w") as f:
        f.write(result.stdout)

#結果をresult fileに出力する
with open("result.txt", "a") as f:
    f.write(f"Total cost      : {total_cost}\n")
    f.write(f"Total cost / num: {total_cost // 100}\n")
    f.write(f"Min score       : {min_score}\n")
    f.write(f"Max score       : {max_score}\n\n")

print("Finished processing all test cases.")
print(f"Total cost: {total_cost}")
print(f"Total cost: {total_cost}", file=sys.stderr)
print(f"Total cost / num: {total_cost // 100}", file=sys.stderr)
print(f"Min score       : {min_score}", file=sys.stderr)
print(f"Max score       : {max_score}", file=sys.stderr)