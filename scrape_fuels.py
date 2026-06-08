import csv
import requests
from datetime import datetime


# =========================
# ✅ STOOQ CSV FETCH
# =========================
def get_stooq(symbol):
    try:
        url = f"https://stooq.com/q/l/?s={symbol}&f=sd2t2ohlcv&h&e=csv"

        r = requests.get(url, timeout=10)

        lines = r.text.splitlines()

        if len(lines) > 1:
            last = lines[-1].split(",")

            price = float(last[6])  # close

            return price

    except Exception as e:
        print(f"{symbol} error:", e)

    return None


# =========================
# ✅ COAL (yritetään stooq commodity)
# =========================
def get_coal():
    return get_stooq("coal")  # usein None → hyväksytään


# =========================
# ✅ MAIN
# =========================
def run():

    today = datetime.utcnow().strftime("%Y-%m-%d")

    rows = []

    # ✅ OIL (Yahoo korvattu Stooqlla)
    rows.append(["WTI", "CL.F", get_stooq("cl.f"), today])
    rows.append(["BRENT", "BZ.F", get_stooq("bz.f"), today])

    # ✅ TTF (oikea)
    rows.append(["TTF", "TG.F", get_stooq("tg.f"), today])

    # ✅ CO2 (oikea)
    rows.append(["CO2_EUA", "CK.F", get_stooq("ck.f"), today])

    # ✅ COAL (voi olla None)
    rows.append(["COAL_API2", "COAL", get_coal(), today])

    # ✅ WRITE CSV
    with open("latest_fuels.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Product", "Symbol", "Price", "Date"])
        writer.writerows(rows)

    print("✅ DONE")
    for r in rows:
        print(r)


# =========================
if __name__ == "__main__":
    run()
