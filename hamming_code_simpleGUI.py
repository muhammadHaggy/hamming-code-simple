import PySimpleGUI as sg

def hammingDecode(biner:str, parity):
    nParity = 1
    while pow(2, nParity) < len(biner):
        nParity += 1
    pangkat2 = [pow(2, v) for v in range(nParity)]
    def hitung1(kar):
        if kar == '1':
            return 1
        return 0
    biner = list(biner)
    err = set()

    for p in pangkat2:
        result = 0
        awal = p-1
        
        while awal < len(biner):
            akhir = awal + p
            for i in range(awal, akhir):
                if i >= len(biner): break
                result += hitung1(biner[i])
            awal += 2 * p
        if parity == PARITY[0]:
            if result % 2 == 1:
                err.add(p)
        elif parity == PARITY[1]:
            if result % 2 == 0:
                err.add(p)
    
    pangkat2.reverse()
    for p in pangkat2:
        del biner[p-1]

    bitError = 0
    for r in err:
        bitError += r
    if not err:
        bitError = None
    return ''.join(biner), bitError


MODE = ('encode', 'decode')
PARITY = ('even', 'odd')
LSB = ('right', 'left')
layout = [
    [sg.Text('Mode:'),sg.OptionMenu(MODE, default_value=MODE[1], key='mode'),sg.Text('Posisi LSB:'), sg.OptionMenu(LSB, default_value=LSB[0], key='lsb'), sg.Text('Parity:'), sg.OptionMenu(PARITY, default_value=PARITY[0], key='parity')],
    [sg.Text('masukkan biner'),sg.InputText(key='biner'), sg.Submit()]
]

window = sg.Window('Hamming Encoder/Decoder', layout)
event, values = window.read()

window.close()

mode = MODE.index(values['mode']) + 1
bits = values['biner']
first_parity_in_left = LSB.index(values['lsb'])
par = PARITY.index(values['parity'])

layout = []
if int(mode) == 1:
    # hasil hamming code
    hamming = ""
    # index hamming code
    hamming_idx = 1

    tmp = bits
    if first_parity_in_left:
        tmp = tmp[::-1]

    while len(tmp) > 0:
        if (
            hamming_idx & (hamming_idx - 1)
        ) == 0:  # cek kalau hamming_idx itu pangkat 2
            # tambahi karakter 'p' yang menandai bahwa itu adalah suatu parity bit
            hamming = "p" + hamming
        else:
            hamming = tmp[-1] + hamming
            tmp = tmp[:-1]

        hamming_idx += 1

    idx = 1
    # tambahi dummy char agar menjadi 1-based index
    hamming += "-"
    hamming = hamming[::-1]

    # proses perubahan 'p' menjadi parity bit
    while idx < len(hamming):
        parity = par
        for j in range(1, len(hamming)):
            if j & idx and j != idx:
                parity ^= int(hamming[j])

        hamming = hamming[:idx] + str(parity) + hamming[idx + 1 :]
        idx <<= 1

    if first_parity_in_left:
        layout.append([sg.Text(f'The hamming code of {bits} is:'),sg.InputText(f"{hamming[1:]}", disabled=True)])
    else:
        layout.append([sg.Text(f'The hamming code of {bits} is:'),sg.InputText(f"{hamming[:0:-1]}", disabled=True)])

else:
    idx = 1

    if first_parity_in_left:
        bits = bits[::-1]

    # tambahkan dummy char agar 1-based index
    bits += "-"
    bits = bits[::-1]

    error_loc = 0

    while idx < len(bits):
        parity = 0
        for j in range(1, len(bits)):
            if j & idx:
                parity ^= int(bits[j])

        if parity != par:
            error_loc += idx

        layout.append([sg.Text(f"The parity bit at position {idx} is {'Even' if parity == 0 else 'Odd'}")])
        idx <<= 1

    bits = bits[1:] if first_parity_in_left else bits[:0:-1]

    if error_loc:
        layout.append([sg.Text(f"The error location of {bits} is: {error_loc}")])
    else:
        layout.append([sg.Text(f"There are no errors in {bits}")])


    # Tambahan Buat nyari hasil decode
    bits = list(values['biner'])
    if not first_parity_in_left:
        bits = ''.join(bits[::-1])
    else:
        bits = ''.join(bits)

    hasil, biterror = hammingDecode(bits, values['parity'])
    layout.append([sg.Text('Hasil decode:'),sg.InputText(hasil, disabled=True)])


window = sg.Window('Hasil', layout)
window.read()
window.close()
