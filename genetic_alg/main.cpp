//Se creará un algoritmo genético para resolver el problema del agente viajero
#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <time.h>
#include <math.h>

using namespace std;

//Se crea la estructura ciudad
struct City{
    int x;
    int y;
    City(int x, int y): x(x), y(y){}
    City operator-(const City &c){
        return City(x - c.x, y - c.y);
    }
    double distance(const City &c){
        City d = *this - c;
        return sqrt(d.x * d.x + d.y * d.y);
    }
    friend ostream& operator<<(ostream &os, const City &c){
        os << "(" << c.x << ", " << c.y << ")";
        return os;
    }
};

struct Individual{
    vector<int> genes;
    vector<City> cities;
    double fitness = 0;
    int n_cities;
    Individual(vector<City> &cities): cities(cities){
        n_cities = cities.size();
        create_genes();
        calc_fitness();
    }
    
    void create_genes(){
        for(int i = 0; i < n_cities; i++){
            genes.push_back(i);
        }
        shuffle(genes.begin() + 1, genes.end(), default_random_engine(rand()));
        genes.push_back(0);
    }

    void calc_fitness(){
        for(int i = 0; i < n_cities; i++){
            fitness += cities[genes[i]].distance(cities[genes[i+1]]);
        }
    }

    friend ostream& operator<<(ostream &os, const Individual &ind){
        for(int i = 0; i <= ind.n_cities; i++){
            os << ind.genes[i] << " ";
        }
        return os;
    }

    double get_fitness(){
        return fitness;
    }
};

class DNA{
    vector<City> cities;
    vector<Individual> population;
    int n_cities;
    int n_generations;
    int n_population;
public:
    DNA(int n_cities, int n_generations, int n_population): n_cities(n_cities), n_generations(n_generations), n_population(n_population){
        create_cities();
        create_population();
    }
    void create_cities(){
        for (int i = 0; i < n_cities; i++){
            cities.push_back(City(rand() % 100, rand() % 100));
        }
    }
    void create_population(){
        for(int i = 0; i < n_population; i++){
            population.push_back(Individual(cities));
        }
    }
    void order_by_best(){
        sort(population.begin(), population.end(), [](Individual &a, Individual &b){
            return a.fitness < b.fitness;
        });
    }
    void simulate(){
        for(int i = 0; i < n_generations; i++){
            order_by_best();
            print();
            vector<Individual> new_population;
            for(int j = 0; j < n_population; j++){
                Individual parent1 = select_parent();
                Individual parent2 = select_parent();
                Individual child = crossover(parent1, parent2);
                mutate(child);
                new_population.push_back(child);
            }
            population = new_population;
        }
    }
    void mutate(Individual &child){
        int index1 = rand() % n_cities;
        int index2 = rand() % n_cities;
        int temp = child.genes[index1];
        child.genes[index1] = child.genes[index2];
        child.genes[index2] = temp;
    }
    Individual select_parent(){
        int index = rand() % n_population;
        return population[index];
    }
    Individual crossover(Individual &parent1, Individual &parent2){
        Individual child(cities);
        int start = rand() % n_cities;
        int end = rand() % n_cities;
        for(int i = 0; i < n_cities; i++){
            if(start < end && i > start && i < end){
                child.genes[i] = parent1.genes[i];
            }else if(start > end){
                if(!(i < start && i > end)){
                    child.genes[i] = parent1.genes[i];
                }
            }
        }
        for(int i = 0; i < n_cities; i++){
            if(child.genes[i] == -1){
                for(int j = 0; j < n_cities; j++){
                    if(!contains(child.genes, parent2.genes[j])){
                        child.genes[i] = parent2.genes[j];
                        break;
                    }
                }
            }
        }
        return child;
    }
    bool contains(vector<int> &v, int n){
        for(int i = 0; i < v.size(); i++){
            if(v[i] == n){
                return true;
            }
        }
        return false;
    }
    void print(){
        cout << "Cities: " << endl;
        for(int i = 0; i < n_cities; i++){
            cout << cities[i] << " ";
        }
        cout << endl << "Population: " << endl;
        for(int i = 0; i < n_population; i++){
            cout << population[i] << "-> " << population[i].fitness << endl;
        }
    }

};

int main(){
    srand(time(0));
    DNA dna(10, 100, 10);
    dna.simulate();
    return 0;
}