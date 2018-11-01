# -*- coding: utf-8 -*-
import pymysql as my
import csv
from unicodedata import normalize
import timeit

FORMAT_NUMBER = lambda x: x.replace(",", ".").replace("\u200b", "")
FORMAT_CLEAN = lambda x: "'" + x.replace(" ", "") + "'"
FORMAT_IDENTITY = lambda x: x
FORMAT_ESCAPE_SINGLE_QUOTE = lambda x: x.replace("\\", "").replace("'", "''")
FORMAT_REMOVE_ACCENTS = lambda x: FORMAT_ESCAPE_SINGLE_QUOTE(normalize('NFKD', x).encode('ASCII', 'ignore').decode('ASCII').upper())
FORMAT_DATE = lambda x: '{}-{}-{}'.format(*x.split("/")[::-1])
DEFAULT_BATCH_SIZE = 500

def preprocess_proposta_csv_row(csv_rows):
    desc_orgao_sup = FORMAT_REMOVE_ACCENTS(csv_rows[5])
    if desc_orgao_sup != "MINISTERIO DA EDUCACAO":
        csv_rows = []
    return csv_rows

TIPO_VEICULO = {
    'csv_file_name': 'acidentes2017_teste',
    'csv_columns_indexes': [19],
    'table_name': 'tipo_veiculo',
    'columns_to_insert': ['tipo_veiculocol'],
    'insert_value_format': "({})",
    'row_formatters': [FORMAT_CLEAN],
    'insert_command': "INSERT"
}

MARCA = {
    'csv_file_name': 'acidentes2017_teste',
    'csv_columns_indexes': [20],
    'table_name': 'tipo_veiculo',
    'columns_to_insert': ['marca'],
    'insert_value_format': "({})",
    'row_formatters': [FORMAT_CLEAN],
    'insert_command': "INSERT"


}

def columns_name_statement(columns_to_insert):
    insert_columns_name_statement = '(' + ','.join(list(map(lambda x: '`' + x + '`', columns_to_insert))) + ')'
    return insert_columns_name_statement

def rangesBat(num):
    return [num * DEFAULT_BATCH_SIZE, num * DEFAULT_BATCH_SIZE + DEFAULT_BATCH_SIZE]

def mapInsertDB(db_cursor, table_name, insert_command, insert_values, insert_columns_name_statement, total_rows, ranges, columns_to_insert):
    batch_start = timeit.default_timer()
    insert_values_batch = insert_values[ranges[0]:ranges[1]]
    insert_sql_command = (insert_command + ' INTO ' + table_name + ' ' + insert_columns_name_statement + 
        ' VALUES ' + ', '.join(insert_values_batch) + ' ON DUPLICATE KEY UPDATE ' +
        columns_to_insert[0] + ' = ' +  columns_to_insert[0])


    db_cursor.execute(insert_sql_command)
    db.commit()
    batch_stop = timeit.default_timer()
    batch_time = batch_stop - batch_start
    print("Linhas inseridas/atualizadas em " + table_name + ": " + str(ranges[1]) + "/" + str(total_rows) + ' (' + str(batch_time) + 's)')

def format_csv_column(row, row_formatter):
    if row == '':
        return 'NULL'
    else:
        return row_formatter(row)

def build_insert_value(csv_row, row_formatters, insert_value_format):
    csv_row = list(map(lambda x,y: format_csv_column(x,y), csv_row, row_formatters))
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
    ifile = open('dados/' + file_name + '.csv', 'r', encoding="utf-8")
    reader = csv.reader(ifile, delimiter=';')
    reader = list(reader)
    #print("####### 111 - ",reader)
    reader = reader[1:]
    #print("####### 222 - ",reader)
    insert_values = list()
    insert_values = mapInserirValoresBD(row_formatters, insert_value_format, csv_columns_indexes, allow_null_columns, csv_require_not_null_indexes, csv_preprocess_row, insert_values, reader)
    #print("####### 333 - ",insert_values)
    return insert_values

def insert_values_on_database(db_cursor, table_name, insert_command, columns_to_insert, insert_values):
    start = timeit.default_timer()
    insert_columns_name_statement = columns_name_statement(columns_to_insert)
    total_rows = len(insert_values)
    print('total_rows: ',total_rows)
    numBatchs = total_rows // DEFAULT_BATCH_SIZE
    lastRangeLow = total_rows - (total_rows % DEFAULT_BATCH_SIZE) 
    listSequenceBatchs = list(range(numBatchs))
    listRangesBatchs = list(map(lambda x: rangesBat(x) , listSequenceBatchs))
    listRangesBatchs.append([lastRangeLow, total_rows])
    print(listRangesBatchs)
    list(map(lambda x: mapInsertDB(db_cursor, table_name, insert_command, insert_values, insert_columns_name_statement, total_rows, x, columns_to_insert) , listRangesBatchs))
    stop = timeit.default_timer()
    time_spent = stop - start
    print('Tempo inserindo na tabela ' + table_name + ': ' + str(time_spent) + 's')

def process(db_cursor, config):
    start_build_insert = timeit.default_timer()
    insert_values_sql_part = convert_csv_to_sql_insert_values(config)
    stop_build_insert = timeit.default_timer()
    print('Entrada processada para tabela ' + config['table_name'] + ' em: ' + str(stop_build_insert - start_build_insert) + 's')
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
    
    stopTotal = timeit.default_timer()
    timeSpentTotal = stopTotal - startTotal
    minutesTotal = int(timeSpentTotal // 60) # Parte inteira
    secondsTotal = int( (timeSpentTotal/60 - minutesTotal) * 60 )
    print('Tempo total do processo: ' + str(minutesTotal) + ' min : ' + str(secondsTotal) + ' s')
