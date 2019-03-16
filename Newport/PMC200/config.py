
class Config:
    ACTTYP = ["850", "850"]   # 850A: range 25 mm?
    UNIT = ["mm", "mm"]
    CENTER_POS = 24.5
    # distance, vel, acc on both axis  (unit mm mm/s mm/s2)
    PROCESS = [
                [1, 4, 1],
                [2, 3, 0.5],
                [9, 2, 0.5]
    ]
    POS_PROCESS = [
        [
            [1, 1, 0.5]
        ]
    ]



