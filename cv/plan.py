import socket
import mission 

hardware_plan = []

def surfaces_2_plan(surfaces):
    global hardware_plan
    trans_ref = 'LUFRDB'
    trans_table = {
            'U1':'FURBDL',
            'U2':'RUBLDF',
            'U3':'BULFDR',
            'L1':'LBURFD',
            'L2':'LDBRUF',
            'L3':'LFDRBU',
            'F1':'LFDRBU',
            'F2':'LFDRBU',
            'F3':'LFDRBU',
            'D1':'LUFRDB',
            'D2':'LUFRDB',
            'D3':'LUFRDB',
            'R1':'LUFRDB',
            'R2':'LUFRDB',
            'R3':'LUFRDB',
            'B1':'BULFDR',
            'B2':'BULFDR',
            'B3':'BULFDR'} 
    init_trans = 'RBDLFU'
    hardware_plan = []

    plan = []
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    s.connect(('118.24.87.139', 8080))
    s.connect(('127.0.0.1', 8080))
    socket_input_string = ''
    for i in range(6):
        for j in range(9):
            socket_input_string += surfaces[i][j]
    s.sendall((socket_input_string + '\n').encode())
    socket_receieve_str = s.recv(2048).decode().strip('\n')
    s.close()
    words = socket_receieve_str.split(' ')
    if words[-1][-2] != 'f':
        print('Server process Error...')
        print(socket_receieve_str)
        return False
    else:
        print('Server process Success!')
        print(socket_receieve_str)
        for word in words[0:-1]:
            plan.append([word[0], word[1]])
        trans = ''
        for i in range(len(plan)):
            for j in range(6):
                if plan[i][0] == trans_ref[j]:
                    plan[i][0] = init_trans[j]
                    break
        for i in range(len(plan)):
            trans = trans_table[plan[i][0] + plan[i][1]]
            for j in range(len(plan)):
                if j > i:
                    for k in range(len(trans)):
                        if plan[j][0] == trans_ref[k]:
                            plan[j][0] = trans[k]
                            break
        plan_string = []
        for item in plan:
            plan_string.append(item[0] + item[1])
        mission.add(plan_string+['Finished'])
        return True
