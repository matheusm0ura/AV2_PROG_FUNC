import mysql.connector

# Função para conectar ao banco de dados
def connect_to_database(host, user, password, database):
    return mysql.connector.connect(host=host, user=user, password=password, database=database)

# Função para executar comandos SQL
def execute_sql(cursor, command):
    cursor.execute(command)

# Função para gerar INNER JOIN entre tabelas
def generate_inner_join(table1, table2, join_condition):
    return f"INNER JOIN {table2} ON {join_condition}"

# Função para gerar comando SELECT
def generate_select_query(attributes, tables, conditions=None):
    query = f"SELECT {attributes} FROM {tables}"
    if conditions:
        query += f" WHERE {conditions}"
    return query

# Exemplo de uso:
# Conectar ao banco de dados
mydb = connect_to_database("localhost", "root", "admin", "mydatabase")

# Criar cursor
crs = mydb.cursor(buffered=True)

# Gerar INNER JOIN entre as tabelas games, videogames e company
inner_join = generate_inner_join("games", "videogames", "games.id_console = videogames.id_console")
inner_join += generate_inner_join("videogames", "company", "videogames.id_company = company.id_company")

# Gerar comando SELECT para consultar jogos lançados por mais de uma empresa diferente
select_query = generate_select_query("games.*", "games", "games.id_game IN (SELECT id_game FROM games GROUP BY id_game HAVING COUNT(DISTINCT id_company) > 1)")

# Executar consulta
execute_sql(crs, select_query)

# Obter resultados
results = crs.fetchall()

# Exibir resultados
for row in results:
    print(row)

# Fechar cursor e conexão com o banco de dados
crs.close()
mydb.close()
