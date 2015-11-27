def main():
    collectfilelist = [
        "R1-cmd.txt",
        "R2-cmd.txt",
        "R3-cmd.txt",
        "R4-cmd.txt",
        "R5-cmd.txt"
        ]

    caselist = [
        {'case': 'Case1 -Everything OK', 'casefile': 'case1'},
        {'case': 'Case2 -IOU3 e0/0 DOWN', 'casefile': 'case2'},
        {'case': 'Case3 -IOU5 e0/0 DOWN', 'casefile': 'case3'}
    ]

    testruns = 1
    iterations = 1

########## __name__ == '__main__' sentinel checks whether your program is being
########## run standalone
if __name__ == "__main__":
    main()
