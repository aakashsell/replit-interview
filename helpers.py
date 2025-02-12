def execute_code(code, global_vars, local_vars):
    #try using eval
    output = ""
    try:
        output = eval(code, global_vars, local_vars)
    except Exception as e1:
        #try using exec
        print("eval didn't work, trying exec ")
        try:
           output = exec(code, global_vars, local_vars) 
        except Exception as e2:
            print("exec didn't work, retuning 0 ")
            return 0
        
    if isinstance(output, object): 
        output = handle_objects(output)

    print("output = " + str(output))
  
    return str(output)

def handle_objects(obj):
    output = {}
    visited = set()
    objects = traverse_graph(obj, visited)
    return objects
    
def traverse_graph(obj, visited):
    object_id = id(obj)
    if object_id in visited:
        return []
    
    visited.add(object_id)

    collected = [obj]

    if isinstance(obj, dict):
        for value in obj.values():
            collected.extend(traverse_graph(value, visited))
            
    elif isinstance(obj, (list, tuple, set)):
        for item in obj:
            collected.extend(traverse_graph(item, visited))
    
    return collected
    

