import visa

def find_instrument(id_answer, id_query = '*?IDN', read_termination='\r'):
    rm = visa.ResourceManager()
    rs = rm.list_resources()
    for r in rs:
        inst = rm.open_resource(r, read_termination=read_termination)
        ans = inst.query(id_query)
        if id_answer in ans:
            return r
    else:
        return None
    
    