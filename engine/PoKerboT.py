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
import pickle
import baseline
import discard


def run(input_socket):
    """NLHE Hold'em with discards"""
    f_in = input_socket.makefile()
    name = ''
    ev = {}
    board, hole, lastactions, legalactions, keys = [], [], [], [], []
    while True:
        data = f_in.readline().strip()
        if not data:
            print('Gameover, engine disconnected')
            break

        packet = data.split()
        if packet[0] == 'NEWGAME':
            name = packet[1]
            with open(name + '.pickle', 'rb') as handle:
                ev = pickle.load(handle)
        elif packet[0] == 'NEWHAND':
            hole, keys = [baseline.totuple(packet[3]), baseline.totuple(packet[4])], []
        elif packet[0] == 'GETACTION':
            board, numboardcards = [], int(packet[2])
            for ind in range(numboardcards):
                board.append(baseline.totuple(packet[3 + ind]))
            lastactions, numlastactions = [], int(packet[3 + numboardcards])
            for ind in range(numlastactions):
                lastactions.append(packet[4 + numboardcards + ind])
            legalactions, numlegalactions = [], int(packet[4 + numboardcards + numlastactions])
            for ind in range(numlegalactions):
                legalactions.append(packet[5 + numboardcards + numlastactions + ind])
            for action in lastactions:  # process each action
                if action[:7] == 'DISCARD' and name in action:
                    hole[hole.index(baseline.totuple(action[8:10]))] = baseline.totuple(action[11:13])
            if 'DEAL:FLOP' in lastactions or 'DEAL:TURN' in lastactions or 'DEAL:RIVER' in lastactions:
                keys.append((tuple(sorted([c[1] for c in board])), tuple(sorted([c[1] for c in hole])), baseline.flushcode(board, hole)))
            if 'DISCARD:' + baseline.tostr(hole[0]) in legalactions:
                decision = None
                if 'DEAL:FLOP' in lastactions:
                    decision = discard.flop(board, hole, 1)
                elif 'DEAL:TURN' in lastactions:
                    decision = discard.turn(board, hole, 1)
                if decision is not None:
                    s.send(('DISCARD:' + baseline.tostr(decision) + '\n').encode())
                else:
                    s.send(b'CHECK\n')
            elif 'CALL' in legalactions:
                s.send(b'CALL\n')
            else:
                s.send(b'CHECK\n')
        elif packet[0] == 'HANDOVER':
            board, numboardcards = [], int(packet[3])
            for ind in range(numboardcards):
                board.append(baseline.totuple(packet[4 + ind]))
            lastactions, numlastactions = [], int(packet[4 + numboardcards])
            for ind in range(numlastactions):
                lastactions.append(packet[5 + numboardcards + ind])
            for action in lastactions:
                if action[:3] == 'WIN':
                    for key in keys:
                        if name in action:
                            ev[key][0] += 1
                        ev[key][1] += 1
                    break
                elif action[:3] == 'TIE':
                    for key in keys:
                        ev[key][0] += 1
                        ev[key][1] += 2
                    break
        elif packet[0] == 'REQUESTKEYVALUES':
            with open(name + '.pickle', 'wb') as handle:
                pickle.dump(ev, handle, protocol=pickle.HIGHEST_PROTOCOL)
            s.send(b'FINISH\n')
    s.close()

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
