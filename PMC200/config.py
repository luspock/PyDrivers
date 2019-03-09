
class Config:
    ACTTYP = ["850", "850"]   # 850A: range 25 mm?
    UNIT = ["mm", "mm"]
    # distance, vel, acc on both axis  (unit mm mm/s mm/s2)
    PROCESS = [
                [1, 0.1, 0.1],
                [2, 0.2, 0.2],
                [3, 0.3, 0.3]
    ]



