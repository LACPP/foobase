"""Example for Testing the MapReduce intersection
"""
import fbserver

def main():
    fbserver.clear_log()
    print "Running 'main' in test_fbsmapreduce.py ..."
    print "Running a FooBaseServer with the MapReduce version of intersections..."
    bserv = fbserver.FooBaseServerMapReduce('localhost', 11111)
    print bserv
    bserv.start()
    
if __name__=="__main__":
    main()      
