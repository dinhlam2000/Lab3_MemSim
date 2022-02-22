#CREATE A PT AND SET ALL FRAMES TO BE NONE AND ALL INVALID BITS --> 2D Array 256*[ [FN] [Valid] ]
#CREATE AN EMPTY TLB ARRAY 16*[ [PN] [FN] ] BUT SET EVERYTHING TO NONE INITIALLY
#PHYSICAL MEMORY IS 1D ARRAY OF SIZE FRAME_NUMBER

tlb = [[None] * 2] * 16
pt = [[None] * 2] * 256
physical_memory = [None] * 256
fn = 0
tlb_counter = 0


#NOW START POPULATING
#FN goes from 0 -> 256
#PN is Entry // 256




def map_virtual_memory(value):
    global tlb_counter
    global pt
    global tlb
    global physical_memory
    global fn

    #START POPULATING HERE

    pn = value // 256
    for tlb_val in tlb:
        #hit in TLB
        if tlb_val[0] == pn:
            return False, False, tlb_val[1]


    tlb[tlb_counter] = [pn,fn]
    tlb_counter = (tlb_counter + 1) % 16


    #misses in tlb so now goes into pt
    if pt[pn][1] == 1: #soft_miss only but found in PT
        return True, False, pt[pn][0]
    else: #hard misses
        physical_memory[fn] = pn

    #populate pt now
    pt[pn] = [fn,1]
    fn = (fn + 1) % 256

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


    output = ""

    import pdb; pdb.set_trace()
    with open("output.txt", 'w') as file3:
        for value in entries:
            soft_miss , hard_miss, found_frame = map_virtual_memory(int(value))
            if soft_miss:
                tlb_fault += 1
            if hard_miss:
                page_fault += 1

            output = output + "{0}, {1}, {2}\n".format(value,fileContent[int(value)], str(found_frame))
            file3.write("{0}, {1}, {2}\n".format(value,fileContent[int(value)], str(found_frame)))
            page_number = int(value) // 256

            content = fileContent[page_number * 256 : (page_number + 1) * 256]
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








