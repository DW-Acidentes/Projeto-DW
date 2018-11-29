# -*- coding: utf-8 -*-
import pymysql as my
import csv
from unicodedata import normalize
import timeit

FORMAT_NUMBER = lambda x: x.replace(",", ".").replace("\u200b", "")
FORMAT_CLEAN = lambda x: "'" + x.strip().replace("'", "") + "'"
FORMAT_CLEAN_LIST = lambda x: x.replace(" ", "")
FORMAT_ESCAPE_SINGLE_QUOTE = lambda x: x.replace("\\", "").replace("'", "''")
FORMAT_REMOVE_ACCENTS = lambda x: FORMAT_ESCAPE_SINGLE_QUOTE(normalize('NFKD', x).encode('ASCII', 'ignore').decode('ASCII').upper())
FORMAT_DATE = lambda x: '{}-{}-{}'.format(*x.split("/")[::-1])
DEFAULT_BATCH_SIZE = 2000

#FILE_NAME = 'acidentes2017'
#ILE_NAME = 'acidentes2017_teste_not_Null'
FILE_NAME = 'acidentes2017_reduzido_not_Null'


def create_dic_table_simple(csv_columns_indexes, table_name):
    DIC_TABLE = {
        'csv_file_name': FILE_NAME,
        'csv_columns_indexes': [csv_columns_indexes],
        'table_name': table_name,
        'columns_to_insert': [table_name],
        'insert_value_format': "({})",
        'row_formatters': [FORMAT_CLEAN],
        'insert_command': "INSERT"
    }
    return DIC_TABLE


def create_dic_table(csv_columns_indexes, table_name, columns_to_insert):
    len_col = len(columns_to_insert)
    value_format = "{}," * len_col
    DIC_TABLE = {
        'csv_file_name': FILE_NAME,
        'csv_columns_indexes': csv_columns_indexes,
        'table_name': table_name,
        'columns_to_insert': columns_to_insert,
        'insert_value_format': "(" + value_format[:-1] + ")",
        'row_formatters': [FORMAT_CLEAN] * len_col,
        'insert_command': "INSERT"
    }
    return DIC_TABLE

def format_foreing_key(id_tabela,nome_tabela,nome_coluna_tabela):
    return '(SELECT '+ id_tabela + ' FROM ' + nome_tabela + ' WHERE ' + nome_coluna_tabela +' = '

def format_foreing_key_2(id_tabela,nome_tabela,nome_coluna_tabela1,nome_coluna_tabela2):
    return '(SELECT '+ id_tabela + ' FROM ' + nome_tabela + ' WHERE ' + nome_coluna_tabela1 +' = {} AND ' + nome_coluna_tabela2 +' = '

def execute_one_query(query):
    if query == 'NA':
    
        return "IS NULL"
    try:
        query = int(query)
    except:
        if query[0:6] == 'SELECT':
            db_cursor.execute(query)
            return '= '+str(db_cursor.fetchone()[0])
        else:
            return "= '"+query+"'"
    if isinstance(query, int):
        return '= '+str(query)
    # print(query)
    

def get_id_veiculo(db_cursor, csv_row):
    colunas = ['id_tipo_veiculo','id_marca','ano_fabricacao_veiculo']
    lista_ids = ["SELECT id_tipo_veiculo FROM tipo_veiculo WHERE tipo_veiculo = " + FORMAT_CLEAN(csv_row[19]),
    "SELECT id_marca FROM marca WHERE marca = " + FORMAT_CLEAN(csv_row[20]),
    int(float(csv_row[21].strip())) ]
    ands = ['AND']*2 + ['']

    try:
        db_cursor.execute("SELECT id_veiculo FROM veiculo WHERE " + ' '.join([response for ab in zip(colunas, list(map(lambda x:execute_one_query(x),lista_ids)), ands) for response in ab]))
    except:
        print(csv_row[19:22])
         
    return str(db_cursor.fetchone()[0])

def get_id_pessoa(db_cursor, csv_row):
    colunas = ['id_tipo_envolvido','idade','id_sexo','id_estado_fisico']
    [22,24,25,23]
    lista_ids = ["SELECT id_tipo_envolvido FROM tipo_envolvido WHERE tipo_envolvido = '" + csv_row[22].strip() + "'",
    int(float(csv_row[24].strip())),
    "SELECT id_sexo FROM sexo WHERE sexo = '" + csv_row[25].strip() + "'",
    "SELECT id_estado_fisico FROM estado_fisico WHERE estado_fisico = '" + csv_row[23].strip() + "'"]
    ands = ['AND']*3 + ['']

    db_cursor.execute("SELECT pes_id FROM pessoa WHERE " + ' '.join([response for ab in zip(colunas, list(map(lambda x:execute_one_query(x),lista_ids)), ands) for response in ab]))
    return str(db_cursor.fetchone()[0])

'''
def get_id_pista(db_cursor, csv_row):
    colunas = ['id_fase_dia','id_sentido_via','id_condicao_metereologica','id_tipo_pista','id_tracado_via','id_uso_solo']
    lista_ids = ["SELECT id_fase_dia FROM fase_dia WHERE fase_dia = '" + csv_row[12].strip() + "'",
    "SELECT id_sentido_via FROM sentido_via WHERE sentido_via = '" + csv_row[13].strip() + "'",
    "SELECT id_condicao_metereologica FROM condicao_metereologica WHERE condicao_metereologica = '" + csv_row[14].strip() + "'",
    "SELECT id_tipo_pista FROM tipo_pista WHERE tipo_pista = '" + csv_row[15].strip() + "'",
    "SELECT id_tracado_via FROM tracado_via WHERE tracado_via = '" + csv_row[16].strip() + "'",
    "SELECT id_uso_solo FROM uso_solo WHERE uso_solo = '" + csv_row[17].strip() + "'"]
    ands = ['AND']*5 + ['']

    db_cursor.execute("SELECT id_pista FROM pista WHERE " + ' '.join([response for ab in zip(colunas, list(map(lambda x:execute_one_query(x),lista_ids)), ands) for response in ab]))

    return str(db_cursor.fetchone()[0])'''

def get_id_pista(db_cursor, csv_row):
    colunas = ['id_condicao_metereologica','id_tipo_pista','id_uso_solo']
    lista_ids = ["SELECT id_condicao_metereologica FROM condicao_metereologica WHERE condicao_metereologica = '" + csv_row[14].strip() + "'",
    "SELECT id_tipo_pista FROM tipo_pista WHERE tipo_pista = '" + csv_row[15].strip() + "'",
    "SELECT id_uso_solo FROM uso_solo WHERE uso_solo = '" + csv_row[17].strip() + "'"]
    ands = ['AND']*2 + ['']
    db_cursor.execute("SELECT id_pista FROM pista WHERE " + ' '.join([response for ab in zip(colunas, list(map(lambda x:execute_one_query(x),lista_ids)), ands) for response in ab]))
    return str(db_cursor.fetchone()[0])
'''
def get_id_acidente(db_cursor, csv_row, id_pista):
    colunas = ['id_causa_acidente','id_tipo_acidente','id_classificacao_acidente','id_data','id_pista','id_endereco']
    lista_ids = ["SELECT id_causa_acidente FROM causa_acidente WHERE causa_acidente = '" + csv_row[9].strip() + "'",
    "SELECT id_tipo_acidente FROM tipo_acidente WHERE tipo_acidente = '" + csv_row[10].strip() + "'",
    "SELECT id_classificacao_acidente FROM classificacao_acidente WHERE classificacao_acidente = '" + csv_row[11].strip() + "'",
    "SELECT id_data FROM data WHERE data_inversa = '" + csv_row[2].strip() + "' AND horario = '"+csv_row[4].strip() +"'",
    int(id_pista),
    "SELECT id_endereco FROM endereco WHERE latitude = '" + csv_row[30].strip() + "' AND longitude = '"+csv_row[31].strip() +"'"]
    ands = ['AND']*5 + ['']

    db_cursor.execute("SELECT id_acidente FROM acidente WHERE " + ' '.join([response for ab in zip(colunas, list(map(lambda x:execute_one_query(x),lista_ids)), ands) for response in ab]))
    return str(db_cursor.fetchone()[0])'''

def get_id_acidente(db_cursor, csv_row, id_pista):
    colunas = ['id_causa_acidente','id_tipo_acidente','id_classificacao_acidente','id_pista','id_endereco','id_tipo_veiculo','data_inversa','horario']
    lista_ids = ["SELECT id_causa_acidente FROM causa_acidente WHERE causa_acidente = '" + csv_row[9].strip() + "'",
    "SELECT id_tipo_acidente FROM tipo_acidente WHERE tipo_acidente = '" + csv_row[10].strip() + "'",
    "SELECT id_classificacao_acidente FROM classificacao_acidente WHERE classificacao_acidente = '" + csv_row[11].strip() + "'",
    int(id_pista),
    "SELECT id_endereco FROM endereco WHERE latitude = '" + csv_row[30].strip() + "' AND longitude = '"+csv_row[31].strip() +"'",
    "SELECT id_tipo_veiculo FROM tipo_veiculo WHERE tipo_veiculo = '" + csv_row[19].strip() + "'",
    csv_row[2].strip(),
    csv_row[4].strip()]
    ands = ['AND']*7 + ['']
    db_cursor.execute("SELECT id_acidente FROM acidente WHERE " + ' '.join([response for ab in zip(colunas, list(map(lambda x:execute_one_query(x),lista_ids)), ands) for response in ab]))
    return str(db_cursor.fetchone()[0])


TIPO_VEICULO = create_dic_table_simple(19,'tipo_veiculo')
MARCA = create_dic_table_simple(20,'marca')
SEXO = create_dic_table_simple(25,'sexo')
ESTADO_FISICO = create_dic_table_simple(23,'estado_fisico')
BR = create_dic_table_simple(6,'br')
UF = create_dic_table_simple(5,'uf')
TIPO_ENVOLVIDO = create_dic_table_simple(22,'tipo_envolvido')
CAUSA_ACIDENTE = create_dic_table_simple(9,'causa_acidente')
TIPO_ACIDENTE = create_dic_table_simple(10,'tipo_acidente')
CLASSIFICACAO_ACIDENTE = create_dic_table_simple(11,'classificacao_acidente')
FASE_DIA = create_dic_table_simple(12,'fase_dia')
SENTIDO_VIA = create_dic_table_simple(13,'sentido_via')
CONDICAO_METEREOLOGICA = create_dic_table_simple(14,'condicao_metereologica')
TIPO_PISTA = create_dic_table_simple(15,'tipo_pista')
TRACADO_VIA = create_dic_table_simple(16,'tracado_via')
USO_SOLO = create_dic_table_simple(17,'uso_solo')

DATA = create_dic_table([2,3,4], 'data', ['data_inversa', 'dia_semana', 'horario'])

VEICULO = {
    'csv_file_name': FILE_NAME,
    'csv_columns_indexes': [19,20,21],
    'table_name': 'veiculo',
    'columns_to_insert': ['id_tipo_veiculo','id_marca','ano_fabricacao_veiculo'],
    'insert_value_format': "("+ format_foreing_key('id_tipo_veiculo','tipo_veiculo','tipo_veiculo') + " {})," +
                        format_foreing_key('id_marca','marca','marca') +" {}),{})",
    'row_formatters': [FORMAT_CLEAN] * 3,
    'insert_command': "INSERT"
}

PESSOA = {
    'csv_file_name': FILE_NAME,
    'csv_columns_indexes': [22,24,25,23],
    'table_name': 'pessoa',
    'columns_to_insert': ['id_tipo_envolvido','idade','id_sexo','id_estado_fisico'],
    'insert_value_format': "("+ format_foreing_key('id_tipo_envolvido','tipo_envolvido','tipo_envolvido') + " {})," +
                        "{}," +
                        format_foreing_key('id_sexo','sexo','sexo') +" {})," +
                        format_foreing_key('id_estado_fisico','estado_fisico','estado_fisico') +" {}))",
    'row_formatters': [FORMAT_CLEAN] * 4,
    'insert_command': "INSERT"
}

MUNICIPIO = {
    'csv_file_name': FILE_NAME,
    'csv_columns_indexes': [8,5],
    'table_name': 'municipio',
    'columns_to_insert': ['municipio','id_uf'],
    'insert_value_format': "({}," +
                        format_foreing_key('id_uf','uf','uf') +" {}))",
    'row_formatters': [FORMAT_CLEAN] * 2,
    'insert_command': "INSERT"
}

ENDERECO = {
    'csv_file_name': FILE_NAME,
    'csv_columns_indexes': [6,7,8,30,31],
    'table_name': 'endereco',
    'columns_to_insert': ['id_br','km','id_municipio','latitude','longitude'],
    'insert_value_format': "("+ format_foreing_key('id_br','br','br') + " {})," +
                        "{}," +
                        format_foreing_key('id_municipio','municipio','municipio') +" {})," +
                        "{}," +
                        "{})",
    'row_formatters': [FORMAT_CLEAN] * 5,
    'insert_command': "INSERT"
}
'''
PISTA = {
    'csv_file_name': FILE_NAME,
    'csv_columns_indexes': [12,13,14,15,16,17],
    'table_name': 'pista',
    'columns_to_insert': ['id_fase_dia','id_sentido_via','id_condicao_metereologica','id_tipo_pista','id_tracado_via','id_uso_solo'],
    'insert_value_format': "("+ format_foreing_key('id_fase_dia','fase_dia','fase_dia') + " {})," +
                        format_foreing_key('id_sentido_via','sentido_via','sentido_via') +" {})," +
                        format_foreing_key('id_condicao_metereologica','condicao_metereologica','condicao_metereologica') +" {})," +
                        format_foreing_key('id_tipo_pista','tipo_pista','tipo_pista') +" {})," +
                        format_foreing_key('id_tracado_via','tracado_via','tracado_via') +" {})," +
                        format_foreing_key('id_uso_solo','uso_solo','uso_solo') +" {}))",
    'row_formatters': [FORMAT_CLEAN] * 6,
    'insert_command': "INSERT"
}'''

PISTA = {
    'csv_file_name': FILE_NAME,
    'csv_columns_indexes': [14,15,17],
    'table_name': 'pista',
    'columns_to_insert': ['id_condicao_metereologica','id_tipo_pista','id_uso_solo'],
    'insert_value_format': "("+ format_foreing_key('id_condicao_metereologica','condicao_metereologica','condicao_metereologica') +" {})," +
                        format_foreing_key('id_tipo_pista','tipo_pista','tipo_pista') +" {})," +
                        format_foreing_key('id_uso_solo','uso_solo','uso_solo') +" {}))",
    'row_formatters': [FORMAT_CLEAN] * 3,
    'insert_command': "INSERT"
}
'''
ACIDENTE = {
    'csv_file_name': FILE_NAME,
    'csv_columns_indexes': [9,10,11,2,4,30,31],  # 9,10,11,2,4,0,30,31
    'table_name': 'acidente',
    'columns_to_insert': ['id_causa_acidente','id_tipo_acidente','id_classificacao_acidente','id_data','id_pista','id_endereco'],
    'insert_value_format': "("+ format_foreing_key('id_causa_acidente','causa_acidente','causa_acidente') + " {})," +
                        format_foreing_key('id_tipo_acidente','tipo_acidente','tipo_acidente') +" {})," +
                        format_foreing_key('id_classificacao_acidente','classificacao_acidente','classificacao_acidente') +" {})," +
                        format_foreing_key_2('id_data','data','data_inversa','horario') +" {})," +
                        " {}," +
                        format_foreing_key_2('id_endereco','endereco','latitude','longitude') +" {}))",
    'row_formatters': [FORMAT_CLEAN] * 8,
    'insert_command': "INSERT",
    'csv_special_filttering': "ACIDENTE"
}'''

ACIDENTE = {
    'csv_file_name': FILE_NAME,
    'csv_columns_indexes': [9,10,11,30,31,19,2,4], #  [9,10,11,0,30,31,19,2,4]
    'table_name': 'acidente',
    'columns_to_insert': ['id_causa_acidente','id_tipo_acidente','id_classificacao_acidente','id_pista','id_endereco','id_tipo_veiculo','data_inversa','horario'],
    'insert_value_format': "("+ format_foreing_key('id_causa_acidente','causa_acidente','causa_acidente') + " {})," +
                        format_foreing_key('id_tipo_acidente','tipo_acidente','tipo_acidente') +" {})," +
                        format_foreing_key('id_classificacao_acidente','classificacao_acidente','classificacao_acidente') +" {})," +
                        " {}," +
                        format_foreing_key_2('id_endereco','endereco','latitude','longitude') +" {})," +
                        format_foreing_key('id_tipo_veiculo','tipo_veiculo','tipo_veiculo') +" {})," +
                        "{}," +
                        "{})",
    'row_formatters': [FORMAT_CLEAN] * 9,
    'insert_command': "INSERT",
    'csv_special_filttering': "ACIDENTE"
}

MUNICIPIO = {
    'csv_file_name': FILE_NAME,
    'csv_columns_indexes': [8,5],
    'table_name': 'municipio',
    'columns_to_insert': ['municipio','id_uf'],
    'insert_value_format': "({}," +
                        format_foreing_key('id_uf','uf','uf') +" {}))",
    'row_formatters': [FORMAT_CLEAN] * 2,
    'insert_command': "INSERT"
}

'''ACIDENTE_VEICULO = {
    'csv_file_name': FILE_NAME,
    'csv_columns_indexes': [],
    'table_name': 'acidente_veiculo',
    'columns_to_insert': ['id_veiculo','id_acidente'],
    'insert_value_format': "({}, {})",
    'row_formatters': [FORMAT_CLEAN] * 2,
    'insert_command': "INSERT",
    'csv_special_filttering': "ACIDENTE_VEICULO"
}'''

ACIDENTE_PESSOA = {
    'csv_file_name': FILE_NAME,
    'csv_columns_indexes': [],
    'table_name': 'acidente_pessoa',
    'columns_to_insert': ['id_pessoa','id_acidente'],
    'insert_value_format': "({}, {})",
    'row_formatters': [FORMAT_CLEAN] * 2,
    'insert_command': "INSERT",
    'csv_special_filttering': "ACIDENTE_PESSOA"
}

#SELECT `id_data` FROM `data` WHERE `data_inversa` = '2017-01-01' AND `horario` = '00:40:00'

class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Funções para estilizar prints no terminal
NEGRITO = lambda x: color.BOLD + x + color.ENDC
SUCESSO = lambda x: color.OKGREEN + x + color.ENDC
ERRO = lambda x: color.FAIL + x + color.ENDC
INFO = lambda x: color.OKBLUE + x + color.ENDC
HEADER = lambda x: color.HEADER + x + color.ENDC


def columns_name_statement(columns_to_insert):
    insert_columns_name_statement = '(' + ','.join(list(map(lambda x: '`' + x + '`', columns_to_insert))) + ')'
    return insert_columns_name_statement

def rangesBat(num):
    return [num * DEFAULT_BATCH_SIZE, num * DEFAULT_BATCH_SIZE + DEFAULT_BATCH_SIZE]

def mapInsertDB(db_cursor, table_name, insert_command, insert_values, insert_columns_name_statement, total_rows, ranges, columns_to_insert):
    batch_start = timeit.default_timer()
    insert_values_batch = insert_values[ranges[0]:ranges[1]]

    #print("Valores do batch", insert_values_batch)
    # print(insert_values_batch)
    insert_sql_command = (insert_command + ' INTO ' + table_name + ' ' + insert_columns_name_statement + ' VALUES ' + ', '.join(insert_values_batch) + ' ON DUPLICATE KEY UPDATE ' + str(columns_to_insert[0]) + ' = ' +  str(columns_to_insert[0]) )
    # print("insert_sql_command === ",insert_sql_command)
    db_cursor.execute(insert_sql_command)
    # db.commit()
    # print(db_cursor.mogrify(insert_sql_command))
    # db_cursor = db.cursor()

    batch_stop = timeit.default_timer()
    batch_time = batch_stop - batch_start
    print("Linhas inseridas/atualizadas em " + INFO(table_name) + ": " + str(ranges[1]) + "/" + str(total_rows) + ' (' + str(batch_time) + 's)')

def format_csv_column(row, row_formatter):
    if row == '' or row == 'NA':
        return 'NULL'
    else:
        return row_formatter(row)

def build_insert_value(csv_row, row_formatters, insert_value_format):

    csv_row = list(map(lambda x,y: format_csv_column(x,y), csv_row, row_formatters))
    # print("Linha atual no CSV:", csv_row)

    #csv_row = selectIds(csv_row)

    return insert_value_format.format(*csv_row).replace("'NULL'", 'NULL')

# Remove colunas que nao serao utilizadas
def filter_csv_row(csv_row, csv_columns_indexes):
    filtered_csv_row = list(map(lambda x: csv_row[x], csv_columns_indexes))
    return filtered_csv_row

def require_not_null_condition(csv_row, index):
    if csv_row[index] == '':
        raise (Exception('Erro - condicao csv_require_not_null_indexes nao satisfeita'))

def require_not_null(csv_row, csv_require_not_null_indexes):
    filtered_csv_row = list(map(lambda x: require_not_null_condition(csv_row, x), csv_require_not_null_indexes))
    return filtered_csv_row

def inserirValoresBD(row_formatters, insert_value_format, csv_columns_indexes, allow_null_columns, csv_require_not_null_indexes, csv_special_filttering, insert_values, csv_row):
    skip_normal_filter = False
    if csv_special_filttering != None:
        skip_normal_filter = True
        if csv_special_filttering == 'ACIDENTE':
            id_pista = get_id_pista(db_cursor,csv_row)
            csv_row = list(map(lambda x: csv_row[x], [9,10,11,0,30,31,19,2,4]))
            csv_row[3] = id_pista
        if csv_special_filttering == 'ACIDENTE_PESSOA':
            id_pista = get_id_pista(db_cursor,csv_row)
            id_acidente = get_id_acidente(db_cursor, csv_row, id_pista)
            id_pessoa = get_id_pessoa(db_cursor,csv_row)
            csv_row = [id_pessoa,id_acidente]

    if csv_require_not_null_indexes != None:
        try:
            require_not_null(csv_row, csv_require_not_null_indexes)
        except:
            print("erro: csv_require_not_null_indexes")
    if csv_row != []:
        if skip_normal_filter == False:
            csv_row = filter_csv_row(csv_row, csv_columns_indexes)
        if not allow_null_columns and '' in csv_row:
            print("erro: filter_csv_row")
        #if allow_null_columns or '' not in csv_row:
        else:
            insert_values.append(build_insert_value(csv_row, row_formatters, insert_value_format))

    return insert_values

def mapInserirValoresBD(row_formatters, insert_value_format, csv_columns_indexes, allow_null_columns, csv_require_not_null_indexes, csv_special_filttering, insert_values, reader):
    list(map(lambda z: inserirValoresBD(row_formatters, insert_value_format, csv_columns_indexes, allow_null_columns, csv_require_not_null_indexes, csv_special_filttering, insert_values,z), reader))
    return insert_values

# converte csv para strings contendo um VALUE do sql
def convert_csv_to_sql_insert_values(config):
    file_name = config['csv_file_name']
    row_formatters = config['row_formatters']
    insert_value_format = config['insert_value_format']
    csv_columns_indexes = config['csv_columns_indexes']
    allow_null_columns = config.get('allow_null_columns', True)
    csv_require_not_null_indexes = config.get('csv_require_not_null_indexes', None)
    csv_special_filttering = config.get('csv_special_filttering', None)
    #ifile = open('../docs/' + file_name + '.csv', 'r', encoding="ISO-8859-1")
    ifile = open('../docs/' + file_name + '.csv', 'r', encoding="ISO-8859-1")
    reader = csv.reader(ifile, delimiter=';')
    reader = list(reader)

    reader = reader[1:]

    insert_values = list()
    insert_values = mapInserirValoresBD(row_formatters, insert_value_format, csv_columns_indexes, allow_null_columns, csv_require_not_null_indexes, csv_special_filttering, insert_values, reader)

    return insert_values

def insert_values_on_database(db_cursor, table_name, insert_command, columns_to_insert, insert_values):
    start = timeit.default_timer()
    insert_columns_name_statement = columns_name_statement(columns_to_insert)
    total_rows = len(insert_values)
    # print('Total de linhas: ',total_rows)

    numBatchs = total_rows // DEFAULT_BATCH_SIZE
    lastRangeLow = total_rows - (total_rows % DEFAULT_BATCH_SIZE)
    listSequenceBatchs = list(range(numBatchs))
    listRangesBatchs = list(map(lambda x: rangesBat(x) , listSequenceBatchs))
    listRangesBatchs.append([lastRangeLow, total_rows])

    list(map(lambda x: mapInsertDB(db_cursor, table_name, insert_command, insert_values, insert_columns_name_statement, total_rows, x, columns_to_insert) , listRangesBatchs))
    db.commit()
    stop = timeit.default_timer()
    time_spent = stop - start
    print('Tempo inserindo na tabela ' + table_name + ': ' + str(time_spent) + 's\n')

def process(db_cursor, config):
    print(HEADER('Iniciando extração da tabela ' + NEGRITO(config['table_name']) + '\n'))
    start_build_insert = timeit.default_timer()
    insert_values_sql_part = convert_csv_to_sql_insert_values(config)

    stop_build_insert = timeit.default_timer()
    print('Entrada processada para tabela ' + INFO(config['table_name']) + ' em: ' + str(stop_build_insert - start_build_insert) + 's')
    insert_values_on_database(db_cursor, config['table_name'], config['insert_command'], config['columns_to_insert'], insert_values_sql_part)

def process_tables(list_tables):
    list(map(lambda x: process(db_cursor, x), list_tables))


db = None
db_cursor = None

if __name__ == '__main__':
    db = my.connect(
        host="127.0.0.1",
        user="root",
        passwd="",
        db="acidentesdb",  # Nome da Base de dados gerado pelo diagrama logico
        use_unicode=True,
        charset="utf8"
    )
    db_cursor = db.cursor()
    '''db_cursor.execute("SET GLOBAL max_allowed_packet=268435456")
    db_cursor.execute("SET @@GLOBAL.wait_timeout=300")
    db_cursor.execute("SET profiling = 1")
    db.commit()'''

    startTotal = timeit.default_timer()

    list_tables_inserts = []

    # Extraindo as tabela simples
    list_tables_inserts = [TIPO_VEICULO,SEXO,ESTADO_FISICO,BR,UF,TIPO_ENVOLVIDO,
                                CAUSA_ACIDENTE,TIPO_ACIDENTE,CLASSIFICACAO_ACIDENTE,
                                CONDICAO_METEREOLOGICA,TIPO_PISTA,USO_SOLO]
    # Para a fase de testes
    #list_tables_inserts.append(VEICULO)
    list_tables_inserts.append(PESSOA)
    list_tables_inserts.append(MUNICIPIO)
    list_tables_inserts.append(ENDERECO)
    list_tables_inserts.append(PISTA)
    list_tables_inserts.append(ACIDENTE)
    # list_tables_inserts.append(ACIDENTE_VEICULO)
    list_tables_inserts.append(ACIDENTE_PESSOA)


    process_tables(list_tables_inserts)


    stopTotal = timeit.default_timer()
    timeSpentTotal = stopTotal - startTotal
    minutesTotal = int(timeSpentTotal // 60) # Parte inteira
    secondsTotal = int( (timeSpentTotal/60 - minutesTotal) * 60 )
    print('\nTempo total do processo: ' + color.ENDC + str(minutesTotal) + ' min : ' + str(secondsTotal) + ' s')
    print(color.OKGREEN + '** Inserção finalizada com sucesso **' + color.ENDC)
