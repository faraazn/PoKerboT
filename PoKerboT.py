"""
==================================================
    Filename:   PoKerboT.py

 Description:   MIT pokerbots competition program

     Version:   1.0
     Created:   2017-01-19
    Revision:   none
    Compiler:   python 3.5

      Author:   David Amirault,
                Faraaz Nadeem,
                Nilai Sarda,
                Arman Talkar
==================================================
"""

import argparse
import socket
import baseline
import discard


def run(input_socket):
    """NLHE Hold'em with discards"""
    f_in = input_socket.makefile()
    name = ''
    board, hole, lastactions, legalactions = [], [], [], []
    codes = [0] * 9
    while True:
        data = f_in.readline().strip()
        if not data:
            print('Gameover, engine disconnected')
            break

        print(data)

        packet = data.split()
        if packet[0] == 'NEWGAME':
            name = packet[1]
        if packet[0] == 'NEWHAND':
            hole = [baseline.totuple(packet[3]), baseline.totuple(packet[4])]
            print(hole)
        if packet[0] == 'GETACTION':
            board, numboardcards = [], int(packet[2])
            for ind in range(numboardcards):
                board.append(baseline.totuple(packet[3 + ind]))
            print(board)
            lastactions, numlastactions = [], int(packet[3 + numboardcards])
            for ind in range(numlastactions):
                lastactions.append(packet[4 + numboardcards + ind])
            print(lastactions)
            legalactions, numlegalactions = [], int(packet[4 + numboardcards + numlastactions])
            for ind in range(numlegalactions):
                legalactions.append(packet[5 + numboardcards + numlastactions + ind])
            print(legalactions)
            if lastactions[-1][14:] == name and lastactions[-1][:7] == 'DISCARD':
                hole[hole.index(baseline.totuple(lastactions[-1][8:10]))] = baseline.totuple(lastactions[-1][11:13])
                print(hole)
            if 'DISCARD' in legalactions:
                decision = None
                if 'DEAL:TURN' in lastactions:
                    decision = discard.turn(board, hole, 1)
                elif 'DEAL:FLOP' in lastactions:
                    decision = discard.flop(board, hole, 1)
                if decision is not None:
                    s.send('DISCARD:' + baseline.tostr(decision) + '\n')
                else:
                    s.send('CHECK\n')
            elif 'CALL' in legalactions:
                s.send('CALL\n')  # keep the game going
            else:
                s.send('CHECK\n')
        elif packet[0] == 'HANDOVER':
            board, numboardcards = [], int(packet[3])
            for ind in range(numboardcards):
                board.append(baseline.totuple(packet[4 + ind]))
            print(board)
            codes[discard.handcode(board + hole)] += 1
        elif packet[0] == 'REQUESTKEYVALUES':
            s.send('FINISH\n')
    s.close()
    print([c * 100 / sum(c) for c in codes])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PKT pokerbot', add_help=False, prog='pokerbot')
    parser.add_argument('-h', dest='host', type=str, default='localhost', help='Host to connect to, defaults to localhost')
    parser.add_argument('port', metavar='PORT', type=int, help='Port on host to connect to')
    args = parser.parse_args()

    print('Connecting to %s:%d' % (args.host, args.port))
    try:
        s = socket.create_connection((args.host, args.port))
    except socket.error as e:
        print('Error connecting! Aborting')
        exit()

    run(s)
