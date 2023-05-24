import csv

# Configuración del perceptrón
threshold = 0.5
learning_rate = 0.1
trained_perceptrons = {}

def is_row_empty(row):
    for i in row:
        if i != '':
            return False
    return True

# La estructura del archivo .csv es:
# 'class_name', input_1, input_2, ..., 
#           '', input_1, input_2, ...,

def process_data(file = 'training_data.csv'):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        data = {}
        currentClass = ''
        for row in reader:
            if is_row_empty(row):
                pass
            else:
                if row[0] != '': #new class
                    currentClass = row[0]
                    data[currentClass] = []
                elements = map(lambda x: int(x), row[1:])    
                data[currentClass].extend(elements)
                list(elements)
    return data

# Producto punto con los pesos
def dot_product(values, weights):
    return sum(value * weight for value, weight in zip(values, weights))

# Entrenamiento del perceptrón con el dataset.
def train(training_set):
    weights = [0] * len(training_set[0][0])
    while True:
        error_count = 0
        for input_vector, desired_output in training_set:
            result = dot_product(input_vector, weights) > threshold
            error = desired_output - result
            if error != 0:
                error_count += 1
                for index, value in enumerate(input_vector):
                    weights[index] += learning_rate * error * value
        if error_count == 0:
            break
    return weights

# Creación del training set
def create_training_set(tag, training_data):
    training_set = []
    for key, data in iter(training_data.items()):
        training_set.append((tuple(data),1 if key == tag else 0))
    return training_set

# Corre recognize() en cada perceptrón entrenado
def classify(sensor_data, perceptrons):
    ratings = []
    for key, value in iter(perceptrons.items()):
        print("Probando {0}".format(key))
        ratings.append((key,recognize(sensor_data,value)))
    print("-"*10)
    return max(ratings, key = lambda i: i[1])[0]

# Trata de reconocer sensor_data a través de cada perceptrón, usando el umbral
def recognize(sensor_data, weights):
    result = dot_product(sensor_data, weights)
    print("Salida: {0} Umbral: {1}".format(result, threshold))
    return result 

# Crea y empieza el entrenamiento de los perceptrones
def create_perceptrons():
    data = process_data()
    for tag in iter(data.keys()):
        trained_perceptrons[tag] = train(create_training_set(tag, data))

def init():
    print("Entrenando perceptrones...")
    create_perceptrons()
    print("Perceptones entrenados.")


def main():
    init()
    while True:
        sensor_data = input("Ingrese los datos del sensor: ").split()
        sensor_data = [int(x) for x in sensor_data]
        result = classify(sensor_data, trained_perceptrons)
        print(f"Resultado: {result}")

if __name__ == "__main__":
    main()
