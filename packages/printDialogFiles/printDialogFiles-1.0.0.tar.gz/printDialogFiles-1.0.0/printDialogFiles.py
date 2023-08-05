def printFiles (fileName):
    try:
        data = open(fileName)
        for each_line in data:
            try:
                (role, spoken) = each_line.split(':', 1)
                print(role, end = '')
                print(' said: ', end = '')
                print(spoken, end = '')
            except  ValueError:
                pass
            
    except IOError:
        print('File Missing')
