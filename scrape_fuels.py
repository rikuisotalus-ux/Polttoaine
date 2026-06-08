import csv
import requests
from datetime import datetime


# =========================
# ✅ STOOQ (oikea endpoint)
# =========================
def get_stooq(symbol):
    try:
        url = f"https://stooq.com/q/d/l/?s={symbol}&i=d"

        r = requests.get(url, timeout=10)

        lines = r.text.splitlines()

        if len(lines) < 2:
            return None

        last = lines[-1].split(",")

        # Close price (index 4)
        return float(last[4])

    except Exception as e:
        print(f"{symbol} error:", e)
        return None


# =========================
# ✅ MAIN
# =========================
def run():

    today = datetime.utcnow().strftime("%Y-%m-%d")

    rows = []

    # ✅ Oil
    rows.append(["WTI", "cl.f", get_stooq("cl.f"), today])
    rows.append(["BRENT", "bz.f", get_stooq("bz.f"), today])

    # ✅ TTF (ICE gas)
    rows.append(["TTF", "tg.f", get_stooq("tg.f"), today])

    # ✅ CO2 (EUA futures)
    rows.append(["CO2_EUA", "ck.f", get_stooq("ck.f"), today])

    # ✅ COAL → ei oikeaa ilmaista → jätetään None
    rows.append(["COAL_API2", "api2", None, today])

    # =========================
    # ✅ WRITE CSV
    # =========================
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
