import mysql.connector

connect_to_database = lambda host, user, password: mysql.connector.connect(
    host=host,
    user=user,
    password=password
)
mydb = connect_to_database("localhost", "root", "admin")

create_cursor = lambda db: db.cursor(buffered=True)

crs = create_cursor(mydb)

exec_sql_cmd = lambda cmd, crs: crs.execute(cmd)

exec_create_table = lambda table, attrs, crs: exec_sql_cmd("CREATE TABLE " + table + " (" + attrs + ");\n", crs)
exec_create_database = lambda dbname, crs: exec_sql_cmd("CREATE DATABASE " + dbname + ";\n", crs)
exec_drop_database = lambda dbname, crs: exec_sql_cmd("DROP DATABASE " + dbname + ":\n", crs)
exec_drop_table = lambda dbname, crs: exec_sql_cmd("DROP TABLE " + dbname + ":\n", crs)
exec_use_database = lambda dbname, crs: exec_sql_cmd("USE " + dbname + ";\n", crs)
exec_select_from_where = lambda attrs, table, wherecond, crs: exec_sql_cmd("SELECT " + attrs + " FROM " + table +
                                                                           " WHERE " + wherecond, crs)
exec_select = lambda attrs, table, crs: exec_sql_cmd("SELECT " + attrs + " FROM " + table + ";\n", crs)
exec_insert = lambda table, attrs, values, crs: exec_sql_cmd("INSERT INTO "
                                                             + table + " (" + attrs + ")" +
                                                             " VALUES (" + values + ");\n", crs)
# exec_create_database("mydatabase", crs)

# exec_create_table("company", "id_company INT PRIMARY KEY, name VARCHAR (255), country VARCHAR (255)", crs)

# exec_create_table("videogames", "id_console INT PRIMARY KEY, name VARCHAR (255), release_date DATE, "
#                                "id_company INT, FOREIGN KEY (id_company) REFERENCES company(id_company)", crs)

# exec_create_table("games", "id_game INT PRIMARY KEY, title VARCHAR (255), genre VARCHAR (255), release_date DATE, "
#                           "id_console INT, FOREIGN KEY (id_console) REFERENCES videogames(id_console)", crs)

# exec_create_table("users", "id INT PRIMARY KEY, name VARCHAR (255), country VARCHAR (255), "
#                           "id_console INT, FOREIGN KEY (id_console) REFERENCES videogames(id_console)", crs)

# exec_insert("company", "id_company,name,country", "'3', 'teste', 'teste'", crs)

exec_use_database("mydatabase", crs)
exec_select_from_where("*", "users", "true", crs)
results = crs.fetchall()
mydb.commit()
show_query = lambda: [x for x in results]
print(show_query())