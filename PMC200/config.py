
class Config:
    ACTTYP = ["850", "850"]   # 850A: range 25 mm?
    UNIT = ["mm", "mm"]
    CENTER_POS = 12.5
    # distance, vel, acc on both axis  (unit mm mm/s mm/s2)
    PROCESS = [
                [1, 2, 0.5],
                [2, 2, 0.5],
                [3, 2, 0.5]
    ]



