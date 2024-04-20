import mysql.connector

# Função lambda para conectar ao banco de dados
connect_to_database = lambda host, user, password: mysql.connector.connect(
    host=host,
    user=user,
    password=password
)
mydb = connect_to_database("localhost", "root", "admin")

# Função lambda para criar um cursor
create_cursor = lambda db: db.cursor(buffered=True)
crs = create_cursor(mydb)

# Função lambda para executar um comando SQL no cursor
exec_sql_cmd = lambda cmd, crs: crs.execute(cmd)

# Função lambda para executar o comando USE DATABASE
exec_use_database = lambda dbname, crs: exec_sql_cmd(f"USE {dbname};\n", crs)

# Função para executar uma consulta no banco de dados
execute_query = lambda query, cursor: cursor.execute(query) or cursor.fetchall()

# Função lambda para gerar o comando SELECT
generate_select_query = lambda table, attrs: f"SELECT {attrs} FROM {table};"

# Função lambda para gerar o comando INNER JOIN entre tabelas
generate_inner_join = lambda table1, table2, table3, join_condition, join_condition_2: (
    f"SELECT * FROM {table1} "
    f"INNER JOIN {table2} ON {join_condition} "
    f"INNER JOIN {table3} ON {join_condition_2};"
)


query_games_by_multiple_companies = lambda cursor: (
    execute_query(
        f"{generate_select_query('games', '*')}\n"
        f"{generate_inner_join('games', 'videogames', 'company', 'games.id_console = videogames.id_console', 'videogames.id_company = company.id_company')}",
        cursor
    )
)

# Usar o banco de dados
exec_use_database("mydatabase", crs)

# Executar a consulta e imprimir os resultados
results = query_games_by_multiple_companies(crs)
print([x for x in results])

# Fechar o cursor e a conexão
crs.close()
mydb.close()
