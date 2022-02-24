#CREATE A PT AND SET ALL FRAMES TO BE NONE AND ALL INVALID BITS --> 2D Array 256*[ [FN] [Valid] ]
#CREATE AN EMPTY TLB ARRAY 16*[ [PN] [FN] ] BUT SET EVERYTHING TO NONE INITIALLY
#PHYSICAL MEMORY IS 1D ARRAY OF SIZE FRAME_NUMBER


import sys
from fifo import FifoMem
from lru import LRUMem
from opt import OPTMem

# frame_number = int(sys.argv[1])
# tlb = [[None] * 2] * 16
# pt = [[None] * 2] * 256
# physical_memory = [None] * frame_number
# fn = 0
# physical_memory_size = 0
# tlb_counter = 0


#NOW START POPULATING
#FN goes from 0 -> 256
#PN is Entry // 256


import codecs


import math
def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


# def map_virtual_memory(value, alg):
#     global tlb_counter
#     global pt
#     global tlb
#     global physical_memory
#     global fn
#     global physical_memory_size
#     global frame_number
#
#     #START POPULATING HERE
#
#     pn = value // 256
#     for index, tlb_val in enumerate(tlb):
#         #hit in TLB
#         if tlb_val[0] == pn:
#             evicted_value = tlb.pop(index)
#             tlb.append(evicted_value)
#             return False, False, tlb_val[1]
#
#
#     #FIFO/LRU hybrid to maintain TLB
#     if tlb_counter < 16:
#         tlb[tlb_counter] = [pn,fn]
#     else:
#         tlb.pop(0)
#         tlb.append([pn,fn])
#
#     tlb_counter = tlb_counter + 1
#
#
#     #misses in tlb so now goes into pt
#     if pt[pn][1] == 1: #soft_miss only but found in PT
#         return True, False, pt[pn][0]
#     else: #hard misses
#         if physical_memory_size < frame_number:
#             physical_memory[fn] = pn
#         else:
#             #pick an evicting victim
#             if alg == "FIFO":
#                 pn_evicted = physical_memory.pop(0)
#                 pt[pn_evicted][1] = 0
#                 physical_memory.append(pn)
#             elif alg == "LRU":
#                 #Looks for least recently used and replace that one
#                 pass
#             elif alg == "OPT":
#                 #Looks into the future starting from the miss and see which ones will be least used farthest from now and evict that one
#                 pass
#         physical_memory_size += 1
#
#
#     #populate pt now
#     pt[pn] = [fn,1]
#     fn = (fn % frame_number)
#     fn = fn + 1
#
#     return True, True, fn - 1








if __name__ == '__main__':
    with open("BACKING_STORE.bin", mode='rb') as file:
        fileContent = file.read()

    #Full Address is the entry
    #Value references = fileContent[fullAddress]
    #Physical Memory FrameNumber = FN
    #Content = fileContent[FullAddress // 256 * 256 : (FullAddress // 256 + 1) * 256]
    #IS TLB MISSES >= PAGE FAULT

    # test = {1 : -1, 2: -1, 3: 0, 4 : 1}
    # import pdb; pdb.set_trace()
    address_file = sys.argv[3]
    with open(address_file, "r") as file2:
        entries = file2.read()
        entries = entries.split('\n')


    frame_number = int(sys.argv[1])
    replacement_algorithm = sys.argv[2]

    virtual_mem = FifoMem(frame_number, entries, fileContent)

    with open("output.txt", 'w') as file3:
        if replacement_algorithm == 'FIFO':
            virtual_mem = FifoMem(frame_number,entries, fileContent)
        elif replacement_algorithm == 'LRU':
            virtual_mem = LRUMem(frame_number, entries, fileContent)
        elif replacement_algorithm == 'OPT':
            virtual_mem = OPTMem(frame_number, entries, fileContent)


        output = virtual_mem.map_virtual_memory()

        for value in output:



            file3.write("{0}, {1}, {2}\n".format(value[0],value[1], value[2]))

            file3.write(value[3] + "\n")
        file3.write("Number of Translated Addresses = {0}".format(str(len(entries))))
        file3.write("\n")
        file3.write("Page Faults = {0}".format(str(virtual_mem.page_fault)))
        file3.write("\n")
        file3.write("Page Fault Rate = {0}".format(str(truncate(virtual_mem.page_fault / len(entries),3))))
        file3.write("\n")
        file3.write("TLB Hits = {0}".format(str(len(entries) - virtual_mem.tlb_fault)))
        file3.write("\n")
        file3.write("TLB Misses = {0}".format(str(virtual_mem.tlb_fault)))
        file3.write("\n")
        file3.write("TLB Hit Rate = {0}".format(str(truncate(1 - virtual_mem.tlb_fault / len(entries),3))))








