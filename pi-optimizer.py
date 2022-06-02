from renko import Renko
import csv
from numpy import log as ln


RESULTS = []

def main():
    global RESULTS

    tick_data = get_tick_data()

    for i in range(1900, 1902):
        r = Renko(i, tick_data)
        r.create_renko()
        backtest(i, r.bricks, len(tick_data))

    result_string = ""
    sorted_charts = sorted(RESULTS, key=lambda i: i['score'], reverse=True)
    for _, i in enumerate(sorted_charts[:30]):
        result_string = result_string + "\n" + str(i)

    write_to_file(result_string)

def backtest(brick_size, bricks, tick_count):
    global RESULTS

    balance = 0
    sign_changes = 0
    for i, b in enumerate(bricks):
        if i != 0:
            if bricks[i]["type"] == bricks[i - 1]["type"]:
                balance = balance + 1
            else:
                balance = balance - 2
                sign_changes = sign_changes + 1

    if sign_changes == 0:
        sign_changes = 1

    price_ratio = tick_count / len(bricks)

    score = balance / sign_changes
    if score >= 0 and price_ratio >= 1:
        score = ln(score + 1) * ln(price_ratio)
    else:
        score = -1.0

    RESULTS.append({"brick_size": brick_size, "score": score})


def get_tick_data():
    # file = open("/tmp/tickrecorder.csv")
    file = open("test.csv")
    csvreader = csv.reader(file)
    tick = []
    for row in csvreader:
        tick.append(float(row[1]))
    file.close()
    return tick


def write_to_file(content):
    f = open("results.txt", "w")
    f.write(content)
    f.close()


if __name__ == "__main__":
    main()