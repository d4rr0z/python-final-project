'''
Program na podstawie danych wczytywanych z pliku w formacie .csv
(moze to byc plik tekstowy lub plik arkusza kalkulacyjnego) tworzy tablice input-output,
ktora wypisuje w konsoli lub zapisuje do osobnego pliku tekstowego.

Do projektu dolaczono kilka przykladowych plikow tekstowych z danymi. Te z 'x' w nazwie
zawieraja macierz przeplywow oraz wektor produkcji globalnej, natomiast te z 'y' macierz
nakladow i wektor produkcji finalnej. PLiki z tymi samymi cyframi w nazwie powinny dac
dokladnie ten sam wynik. Macierze sa wymiarow 2x2 i 3x3, ale program dziala dla dowolnie
duzych (odwracalnych) macierzy.

Do odwracania macierzy wykorzystano biblioteke NumPy.
'''

from numpy.linalg import inv
from sys import argv

def read_file(filename):
    ##
    # Funkcja czyta plik i zapisuje jego zawartosc do zmiennych pomocniczych.
    # @param filename Nazwa pliku z danymi
    # @return matrix Macierz przeplywow albo nakladow
    # @return vector Wektor produkcji finalnej albo globalnej
    # @return total Prawda, jezeli plik zawieral wektor produkcji globalnej
    #
    matrix = []
    vector = []
    total = False
    with open(filename) as new_file:
        for line in new_file:
            if 'x' in line:
                total = True
                continue
            if 'y' in line:
                continue
            parts = line.split(';')
            if total:
                int_parts = list(map(int, parts))
                matrix.append(int_parts[:-1])
                vector.append(int_parts[-1])
            else:
                help = []
                for content in parts:
                    if '/' in content:
                        numbers = content.split('/')
                        value = int(numbers[0]) / int(numbers[1])
                        help.append(value)
                    else:
                        help.append(int(content))
                matrix.append(help[:-1])
                vector.append(help[-1])
    return matrix, vector, total

def lf_matrix(matrix):
    ##
    # Funkcja modyfikuje podana macierz nakladow odejmujac ja od macierzy
    # jednostkowej (wynikiem jest macierz Leontiefa).
    # @param matrix Macierz nakladow (jej kopia)
    #
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i == j:
                matrix[i][j] = 1 - matrix[i][j]
            else:
                matrix[i][j] *= - 1

def io_matrix(matrix, vector):
    ##
    # Funkcja zamienia podana macierz nakladow na macierz przeplywow
    # @param matrix Macierz nakladow
    # @param vector Wektor produkcji globalnej
    #
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            matrix[i][j] = round(matrix[i][j] * vector[j])

def final_demand(matrix, vector):
    ##
    # Funkcja oblicza wektor produkcji finalnej
    # @param matrix Macierz przeplywow
    # @param vector Wektor produkcji globalnej
    # @return result Wektor produkcji finalnej
    #
    result = []
    for i in range(len(matrix)):
        result.append(vector[i]-sum(matrix[i]))
    return result

def total_output(matrix, vector):
    ##
    # Funkcja oblicza wektor produkcji globalnej
    # @param matrix Macierz nakladow
    # @param vector Wektor produkcji finalnej
    # @return result Wektor produkcji globalnej
    #
    result = []
    copy_matrix = []
    for row in matrix:
        copy_matrix.append(row[:])
    lf_matrix(copy_matrix)
    for row in inv(copy_matrix):
        value = 0
        for i in range(len(matrix)):
            value += row[i]*vector[i]
        result.append(round(value))
    io_matrix(matrix, result)
    return result

def to_console(matrix, vector, result, total):
    ##
    # Funkcja wypisuje w konsoli tablice input-output
    # @param matrix Macierz przeplywow
    # @param vector Wektor produkcji finalnej/globalnej
    # @param result Wektor produkcji finalnej/globalnej
    # @param total Zawiera informacje o tym, ktory wektor jest ktory
    #
    header = ' ' * 9 + '|'
    for i in range(len(matrix)):
        header += f' Sektor {i+1} '
    header += ' Produkcja finalna  Produkcja globalna '
    print('\n' + header)
    print('-' * 9 + '|' + '-' * (len(header)-10))
    for i in range(len(matrix)):
        print(f'Sektor {i+1} |', end='')
        for j in range(len(matrix)):
            print(f'{matrix[i][j]:^10}', end='')
        if total:
            print(f'{result[i]:^20}{vector[i]:^20}')
        else:
            print(f'{vector[i]:^20}{result[i]:^20}')

def to_file(matrix, vector, result, total):
    ##
    # Funkcja zapisuje do pliku tekstowego tablice input-output
    # @param matrix Macierz przeplywow
    # @param vector Wektor produkcji finalnej/globalnej
    # @param result Wektor produkcji finalnej/globalnej
    # @param total Zawiera informacje o tym, ktory wektor jest ktory
    #
    with open('results.txt', 'w') as new_file:
        header = ' ' * 9 + '|'
        for i in range(len(matrix)):
            header += f' Sektor {i+1} '
        header += ' Produkcja finalna  Produkcja globalna '
        new_file.write(header + '\n')
        new_file.write('-' * 9 + '|' + '-' * (len(header)-10) + '\n')
        for i in range(len(matrix)):
            new_file.write(f'Sektor {i+1} |')
            for j in range(len(matrix)):
                new_file.write(f'{matrix[i][j]:^10}')
            if total:
                new_file.write(f'{result[i]:^20}{vector[i]:^20}\n')
            else:
                new_file.write(f'{vector[i]:^20}{result[i]:^20}\n')
    print('\n' + 'Tablica input-output zostala zapisana do pliku results.txt.' + '\n')

def main():
    ##
    # Funkcja glowna. Nazwe pliku mozna podac od razu przy wywolywaniu programu w konsoli.
    #
    try:
        if len(argv) > 1:
            matrix, vector, total = read_file(argv[1])
        else:
            print()
            filename = input('Podaj nazwe pliku: ')
            matrix, vector, total = read_file(filename)
        if total:
            result = final_demand(matrix, vector)
        else:
            result = total_output(matrix, vector)
        to_console(matrix, vector, result, total)
        to_file(matrix, vector, result, total)
    except:
        print('\n' + 'Cos poszlo nie tak. Sprobuj ponownie.' + '\n')

if __name__ == "__main__":
    main()
