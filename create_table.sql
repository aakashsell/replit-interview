drop table if exists session_data;

create table session_data (
    session_id INTEGER UNIQUE, 
    global_vars JSON, 
    local_vars JSON    
);