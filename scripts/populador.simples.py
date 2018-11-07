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
DEFAULT_BATCH_SIZE = 10000

FILE_NAME = 'acidentes2017'

TIPO_VEICULO = {
    'csv_file_name': FILE_NAME,
    'csv_columns_indexes': [19],
    'table_name': 'tipo_veiculo',
    'columns_to_insert': ['tipo_veiculocol'],
    'insert_value_format': "({})",
    'row_formatters': [FORMAT_CLEAN],
    'insert_command': "INSERT"
}

MARCA = {
    'csv_file_name': FILE_NAME,
    'csv_columns_indexes': [20],
    'table_name': 'marca',
    'columns_to_insert': ['marca'],
    'insert_value_format': "({})",
    'row_formatters': [FORMAT_CLEAN],
    'insert_command': "INSERT"
}
def format_foreing_key(id_tabela,nome_tabela,nome_coluna_tabela):
    return '(SELECT '+ id_tabela + ' FROM ' + nome_tabela + ' WHERE ' + nome_coluna_tabela +' = '

VEICULO = {
    'csv_file_name': FILE_NAME,
    'csv_columns_indexes': [19,20,21],
    'table_name': 'veiculo',
    'columns_to_insert': ['id_tipo_veiculo','id_marca', 'ano_fabricacao_veiculo'],
    'insert_value_format': "("+ format_foreing_key('id_tipo_veiculo','tipo_veiculo','tipo_veiculocol') +" {}),"+format_foreing_key('id_marca','marca','marca') +" {}),{})",
    'row_formatters': [FORMAT_CLEAN, FORMAT_CLEAN, FORMAT_CLEAN],
    'insert_command': "INSERT"
}

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
    #print("Linha atual no CSV:", csv_row)   
    
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

def inserirValoresBD(row_formatters, insert_value_format, csv_columns_indexes, allow_null_columns, csv_require_not_null_indexes, csv_preprocess_row, insert_values, csv_row):
    if csv_preprocess_row != None:
        try:
            csv_row = csv_preprocess_row(csv_row)
        except ValueError as error:
            print(str(error))
    if csv_require_not_null_indexes != None:
        try:
            require_not_null(csv_row, csv_require_not_null_indexes)
        except:
            print("erro: csv_require_not_null_indexes")
    if csv_row != []:
        csv_row = filter_csv_row(csv_row, csv_columns_indexes)
        if not allow_null_columns and '' in csv_row:
            print("erro: filter_csv_row")
        #if allow_null_columns or '' not in csv_row:
        else:
            insert_values.append(build_insert_value(csv_row, row_formatters, insert_value_format))   
    
    return insert_values

def mapInserirValoresBD(row_formatters, insert_value_format, csv_columns_indexes, allow_null_columns, csv_require_not_null_indexes, csv_preprocess_row, insert_values, reader):
    list(map(lambda z: inserirValoresBD(row_formatters, insert_value_format, csv_columns_indexes, allow_null_columns, csv_require_not_null_indexes, csv_preprocess_row, insert_values,z), reader))
    return insert_values

# converte csv para strings contendo um VALUE do sql
def convert_csv_to_sql_insert_values(config):
    file_name = config['csv_file_name']
    row_formatters = config['row_formatters']
    insert_value_format = config['insert_value_format']
    csv_columns_indexes = config['csv_columns_indexes']
    allow_null_columns = config.get('allow_null_columns', True)
    csv_require_not_null_indexes = config.get('csv_require_not_null_indexes', None)
    csv_preprocess_row = config.get('csv_preprocess_row', None)
    ifile = open('../docs/' + file_name + '.csv', 'r', encoding="ISO-8859-1")
    reader = csv.reader(ifile, delimiter=';')
    reader = list(reader)

    reader = reader[1:]

    insert_values = list()
    insert_values = mapInserirValoresBD(row_formatters, insert_value_format, csv_columns_indexes, allow_null_columns, csv_require_not_null_indexes, csv_preprocess_row, insert_values, reader)

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

db = None

if __name__ == '__main__':
    db = my.connect(
        host="127.0.0.1",
        user="root",
        passwd="",
        db="mydb",  # Nome da Base de dados gerado pelo diagrama logico
        use_unicode=True,
        charset="utf8"
    )
    db_cursor = db.cursor()
    
    startTotal = timeit.default_timer()
    
    process(db_cursor, TIPO_VEICULO)
    # process(db_cursor, MARCA)
    # process(db_cursor, VEICULO)
    
    stopTotal = timeit.default_timer()
    timeSpentTotal = stopTotal - startTotal
    minutesTotal = int(timeSpentTotal // 60) # Parte inteira
    secondsTotal = int( (timeSpentTotal/60 - minutesTotal) * 60 )
    print('\nTempo total do processo: ' + color.ENDC + str(minutesTotal) + ' min : ' + str(secondsTotal) + ' s')
    print(color.OKGREEN + '** Inserção finalizada com sucesso **' + color.ENDC)
