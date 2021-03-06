#CREATE A PT AND SET ALL FRAMES TO BE NONE AND ALL INVALID BITS --> 2D Array 256*[ [FN] [Valid] ]
#CREATE AN EMPTY TLB ARRAY 16*[ [PN] [FN] ] BUT SET EVERYTHING TO NONE INITIALLY
#PHYSICAL MEMORY IS 1D ARRAY OF SIZE FRAME_NUMBER


import sys

frame_number = int(sys.argv[1])
tlb = [[None] * 2] * 16
pt = [[None] * 2] * 256
physical_memory = [None] * frame_number
fn = 0
physical_memory_size = 0
tlb_counter = 0


#NOW START POPULATING
#FN goes from 0 -> 256
#PN is Entry // 256


import codecs



def map_virtual_memory(value, alg):
    global tlb_counter
    global pt
    global tlb
    global physical_memory
    global fn
    global physical_memory_size
    global frame_number

    #START POPULATING HERE

    pn = value // 256
    for index, tlb_val in enumerate(tlb):
        #hit in TLB
        if tlb_val[0] == pn:
            evicted_value = tlb.pop(index)
            tlb.append(evicted_value)
            return False, False, tlb_val[1]


    #FIFO/LRU hybrid to maintain TLB
    if tlb_counter < 16:
        tlb[tlb_counter] = [pn,fn]
    else:
        tlb.pop(0)
        tlb.append([pn,fn])

    tlb_counter = tlb_counter + 1


    #misses in tlb so now goes into pt
    if pt[pn][1] == 1: #soft_miss only but found in PT
        return True, False, pt[pn][0]
    else: #hard misses
        if physical_memory_size < frame_number:
            physical_memory[fn] = pn
        else:
            #pick an evicting victim
            if alg == "FIFO":
                pn_evicted = physical_memory.pop(0)
                pt[pn_evicted][1] = 0
                physical_memory.append(pn)
            elif alg == "LRU":
                #Looks for least recently used and replace that one
                pass
            elif alg == "OPT":
                #Looks into the future starting from the miss and see which ones will be least used farthest from now and evict that one
                pass
        physical_memory_size += 1


    #populate pt now
    pt[pn] = [fn,1]
    fn = (fn % frame_number)
    fn = fn + 1

    return True, True, fn - 1








if __name__ == '__main__':
    with open("BACKING_STORE.bin", mode='rb') as file:
        fileContent = file.read()

    #Full Address is the entry
    #Value references = fileContent[fullAddress]
    #Physical Memory FrameNumber = FN
    #Content = fileContent[FullAddress // 256 * 256 : (FullAddress // 256 + 1) * 256]
    #IS TLB MISSES >= PAGE FAULT


    with open("addresses.txt", "r") as file2:
        entries = file2.read()
        entries = entries.split('\n')


    page_fault = 0
    tlb_fault = 0

    replacement_algorithm = sys.argv[2]
    output = ""

    import pdb; pdb.set_trace()
    with open("output.txt", 'w') as file3:
        for value in entries:
            soft_miss , hard_miss, found_frame = map_virtual_memory(int(value), replacement_algorithm)
            if soft_miss:
                tlb_fault += 1
            if hard_miss:
                page_fault += 1

            output = output + "{0}, {1}, {2}\n".format(value,fileContent[int(value)], str(found_frame))
            byte = fileContent[int(value)]
            if byte > 127:
                byte = byte - 256
            file3.write("{0}, {1}, {2}\n".format(value,byte, str(found_frame)))
            page_number = int(value) // 256

            content = fileContent[page_number * 256 : (page_number + 1) * 256]
            content = content.hex()
            # content = "".join(list(map(lambda x: x if x != "\\" else "", content)))
            # content = content.replace('x', '')
            # content = content.replace('\\', '')
            # content = content.replace()
            file3.write(str(content) + "\n")
            output = output + str(fileContent[page_number * 256 : (page_number + 1) * 256])
        file3.write("Number of Translated Addresses = {0}".format(str(len(entries))))
        file3.write("\n")
        file3.write("Page Faults = {0}".format(str(page_fault)))
        file3.write("\n")
        file3.write("Page Fault Rate = {0}".format(str(page_fault / len(entries))))
        file3.write("\n")
        file3.write("TLB Hits = {0}".format(str(len(entries) - tlb_fault)))
        file3.write("\n")
        file3.write("TLB Misses = {0}".format(str(tlb_fault)))
        file3.write("\n")
        file3.write("TLB Hit Rate = {0}".format(str(1 - tlb_fault / len(entries))))








