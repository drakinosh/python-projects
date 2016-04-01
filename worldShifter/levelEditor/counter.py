import sys

def main(): 
    
    file_list = sys.argv[1:] # all except prog name
    summ = 0

    for filename in file_list:
        
        with open(filename, 'r') as fname:
            
            dat = fname.read()
            summ += dat.count('\n')

    print("TOTAL no. of lines: {}".format(summ))


if __name__ == '__main__':
    
    main()
