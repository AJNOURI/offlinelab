collectfilelist = [
    "R1-cmd.txt",
    "R2-cmd.txt",
    "R3-cmd.txt",
    "R4-cmd.txt",
    "R5-cmd.txt"
    ]

caselist = [
    {'case': 'Case1 -Traffic between R1 10.10.0.1 (area 123) to R5 50.10.0.5 (area0): Default interface ospf costs', 'casefile': 'case1'},
    {'case': 'Case2 -Traffic from R1 10.10.0.1 (area123) to R5 50.20.0.5 (backbone) : R1 fa1/0 cost = 10, R2 fa1/2 cost = 10', 'casefile': 'case2'},
    {'case': 'Case3 -Traffic from R1 10.10.0.1 (area 123) to R5 50.10.0.2 (backbone): R1 fa1/0 cost = 10, R3 fa1/2 cost = 100', 'casefile': 'case3'},
    {'case': 'Case4 -Traffic from R1 10.10.0.1 (area 123) to R5 50.10.0.2 (backbone): R1 fa1/0 cost = 10, R3 fa1/2 cost = 10', 'casefile': 'case4'},
    {'case': 'Case5 -Traffic from R5 50.10.0.5 (backbone) to R1 10.10.0.1 (area 123): R3 fa1/1 cost = 10', 'casefile': 'case5'},
    {'case': 'Case6 -Traffic from R5 50.10.0.5 (backbone) to R1 10.10.0.1 (area 123): R3 fa1/1 cost = 10, R4 fa1/1 cost = 5', 'casefile': 'case6'},
    {'case': 'Case7 -Traffic from R1 10.10.0.1 (area123) to R2 20.10.0.2 (area 123): R1 fa1/0 cost = 100', 'casefile': 'case7'},
    {'case': 'Case8 -Traffic from R1 10.10.0.1 (area123) to R2 20.10.0.2 (area 123): R1-R2 link down (no inter-area route to 20.10.0.2)', 'casefile': 'case8'},
    {'case': 'Case9 -Intra-area traffic from R4 40.10.0.4 (backbone) to R2 20.10.0.2 (backbone): R4 f1/1 cost = 100', 'casefile': 'case9'},
    {'case': 'Case10 -Traffic from R1 10.10.0.2 (area123) to R2 20.20.0.2 (backbone): R4-R2 link down (no inter-area route to 20.20.0.2)', 'casefile': 'case10'},
    {'case': 'Case11 -Traffic between two non-backbone areas. From area123 to area25: Default interface costs', 'casefile': 'case11'},
    {'case': 'Case12 -Traffic generated from R2: 20.10.0.2 (area 123) to R5 50.20.0.5 (area 25): R2 fa1/2 cost = 100', 'casefile': 'case12'},
    {'case': 'Case13 -R2 fa1/1 Down', 'casefile': 'case13'},
    {'case': 'Case14 -R2 fa1/1 Down, R1 fa1/1 Down', 'casefile': 'case14'}
]

testruns = 1
iterations = 1

########## __name__ == '__main__' sentinel checks whether your program is being
########## run standalone
if __name__ == "__main__":
    main()