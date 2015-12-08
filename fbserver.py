"""FOOBASE Server

"""
import json
import socket
import foosettings

#    =================== Logging Management =====================
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=foosettings.LOG_FILE,
                    filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s'))
logging.getLogger('').addHandler(console)
logging.debug("\n\n   =====  ===== STARTED :"+__file__+"   =====  =====")
def clear_log():
    open(foosettings.LOG_FILE, 'w').close()
    
#    ===================   FooBase Server   =====================    
class SERVER_STATES(object):
    """Server States
    """
    class BEGIN(object):
        pass
    class STARTED(object):
        pass
    class CLOSED(object):
        pass

class FooBaseServer(object):
    """FooBase Server
    """
    def __init__(self, host = foosettings.default_host, port = foosettings.default_port, storage_file = foosettings.default_storage_file, backlog = foosettings.default_backlog):
        logging.info("FooBase Server is being instanciated...")
        self.host = host
        self.port = port
        self.storage_file = storage_file
        self.backlog = backlog
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.state = SERVER_STATES.BEGIN
        self.data_buffer = {}
        self.query_stats = foosettings.init_query_stats
        pass
        
    def __str__(self):
        s = "== FooBaseServer Instance =="
        s+= "\n== Host : "+str(self.host)
        s+= "\n== Port : "+str(self.port)
        s+= "\n== Data is stored in file : "+str(self.storage_file)
        s+= "\n== == == == = == == == == =="
        return s
    
    ## Decoding a message
    def decode_query(self, query_string):
        query_value = None
        try:
            query_command, query_key, query_value = query_string.strip().split(' ')
        except:
            query_command, query_key = query_string.strip().split(' ')
        return query_command, query_key, query_value
    def handle_query(self, query):
        response_code = '1110'
        response_value = None
        if(self.state == SERVER_STATES.STARTED):
            command, key, value = self.decode_query(query)
            logging.info("- Received query (command = "+str(command)+", key = "+str(value)+")...")
            if command == 'CREATE':
                response_code, response_value = self.handle_create_query(key, value)
            elif command == 'READ':
                response_code, response_value = self.handle_read_query(key)
            elif command == 'UPDATE':
                response_code, response_value = self.handle_update_query(key, value)
            elif command == 'DELETE':
                response_code, response_value = self.handle_delete_query(key)   
        return response_code, response_value                     
    ## Handling a query    
    # Create key/value pair
    def handle_create_query(self, key, value):
        logging.info("- Processing command CREATE on (key = "+str(key)+", value = "+str(value)+")...")
        response_code = '1110'
        response_value = None
        try:
            self.create_query(key, value)
        except Exception, e:
            print "- ERROR on CREATE : " + str(e)
            response_code = '1111'
        return response_code, response_value
    # Store key/value pair
    def create_query(self, key, value):
        logging.info("- The following data is being stored in the storage file (key = "+str(key)+", value = "+str(value)+")...")
        data_store_file = open( (self.storage_file), "r")
        try:
            self.data_buffer = json.load(data_store_file)
        except ValueError: 
            self.data_buffer = {}
        data_store_file.close()
        if key in self.data_buffer.keys():
            logging.warning(" > Key : "+str(key)+" is already present."
                         +"\n To replace its content please use the UPDATE command"
                         +"\n To delete the key please use the DELETE command  TACK :)")
        else:
            self.data_buffer[key] = value
            data_store_file = open((self.storage_file), "w+")
            json.dump(self.data_buffer, data_store_file)
            data_store_file.close()
            logging.info("      > Data was stored successfully :)")
        
    # Read value from key 
    def handle_read_query(self, key):
        logging.info("- Processing command READ on (key = "+str(key)+")...")
        response_code = '1110'
        response_value = None
        try:
            value = self.read_query(key)
            if(value is None):
                logging.info("- Oh oh, returned value is None")
            else:
                logging.info("- Returned value is : " + str(value))
            response_value = value
        except Exception, e:
            print "- ERROR on READ : " + str(e)
            response_code = '1111'
        return response_code, response_value
    # Read value from key using the storage file
    def read_query(self, key):
        logging.info("- The following key is being read from the storage file: key = "+str(key)+"...")
        value = None
        data_store_file = open( (self.storage_file), "r")
        try:
            self.data_buffer = json.load(data_store_file)
            if not(key in self.data_buffer.keys()):
                logging.warning(" > Key : "+str(key)+" is not present.  TACK :)")
            else:
                value = self.data_buffer[key]
                logging.info("      > Data was read successfully :)")
        except ValueError: 
            logging.warning(" > Data file seems to be empty! :'(")
        data_store_file.close()
        return value
        
    # Update key with new value
    def handle_update_query(self, key, value):
        logging.info("- Processing command UPDATE on (key = "+str(key)+", value = "+str(value)+")...")
        response_code = '1110'
        response_value = None
        try:
            self.update_query(key, value)
        except Exception, e:
            print "- ERROR on UPDATE : " + str(e)
            response_code = '1111'
        return response_code, response_value
    # Update key/value pair in storage file
    def update_query(self, key, value):
        logging.info("- The following data is being stored in the storage file (key = "+str(key)+", value = "+str(value)+")...")
        data_store_file = open( (self.storage_file), "r")
        try:
            self.data_buffer = json.load(data_store_file)
        except ValueError: 
            self.data_buffer = {}
        data_store_file.close()
        if not(key in self.data_buffer.keys()):
            logging.warning(" > Key : "+str(key)+" is not present."
                         +"\n To create it please use the CREATE command instead  TACK :)")
        else:
            self.data_buffer[key] = value
            data_store_file = open((self.storage_file), "w+")
            json.dump(self.data_buffer, data_store_file)
            data_store_file.close()
            logging.info("      > Data was updated successfully :)")
    # Delete key
    def handle_delete_query(self, key):
        logging.info("- Processing command DELETE on (key = "+str(key)+")...")
        response_code = '1110'
        response_value = None
        try:
            self.delete_query(key)
        except Exception, e:
            print "- ERROR on DELETE : " + str(e)
            response_code = '1111'
        return response_code, response_value
    # Delete key from storage file
    def delete_query(self, key):
        logging.info("- The following data is being deleted from the storage file (key = "+str(key)+")...")
        data_store_file = open((self.storage_file), "r")
        try:
            self.data_buffer = json.load(data_store_file)
            if not(key in self.data_buffer.keys()):
                logging.warning(" > Key : "+str(key)+" is not present."
                             +"\n Things that do not exist cannot be deleted  TACK :)")
            else:
                del self.data_buffer[key]
                data_store_file = open((self.storage_file), "w+")
                json.dump(self.data_buffer, data_store_file)
                data_store_file.close()
                logging.info("      > Data was deleted successfully :)")
        except ValueError: 
            self.data_buffer = {}
        data_store_file.close()
        
        
        
    ## Launching the server
    def start(self):
        if self.state == SERVER_STATES.BEGIN:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(self.backlog)
            self.state = SERVER_STATES.STARTED
            while self.state == SERVER_STATES.STARTED:
                client_con, client_adr = self.server_socket.accept()
                print 'New connection from [{}]'.format(client_adr)
                client_qry = client_con.recv(4096).decode()
                response_code, response_value = self.handle_query(client_qry)
                client_con.sendall('-Response Code: {}\n-Response Message: {}\n-Response Value: {}\n'.format(response_code, foosettings.decode_response[response_code], response_value))
                client_con.close()
                
        else:
            logging.error("Tried to start FooBase Server without being in state BEGIN. Current state: " + str(self.state))
            
def main():
    print "Running 'main' in fbserver.py ..."
    clear_log()
    server = FooBaseServer()
#    server.state = SERVER_STATES.STARTED
    print "------- PERFORMING CREATE -------------"
    server.handle_query("CREATE store 0")
    print "------- PERFORMING READ -------------"
    server.handle_query("READ store")
    print "------- PERFORMING UPDATE -------------"
    server.handle_query("UPDATE store 1")
    print "------- PERFORMING READ -------------"
    server.handle_query("READ store")
    print "------- PERFORMING DELETE -------------"
    server.handle_query("DELETE store")
    print "------- PERFORMING READ -------------"
    server.handle_query("READ store")
    print server
    server.start()
    
if __name__=="__main__":
    main()            
        
            
        
     
