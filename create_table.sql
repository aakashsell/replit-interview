drop session_data if exists

create table session_data (
    session_id INTEGER, 
    global_vars JSON, 
    local_vars JSON    
);