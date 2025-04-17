#include <cstdlib>
#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <thread>
#include <mutex>

struct LifeGame {
    int width, height;
    std::vector<std::vector<bool>> tab;
    double p0;
    
    LifeGame(int w, int h, double p) : width(w), height(h), p0(p) {
        tab.resize(width, std::vector<bool>(height, false));
        randomizeTab();
    }

    void randomizeTab() {
        for (auto &row : tab)
            for (auto &cell : row)
                cell = ((double)rand() / RAND_MAX) < p0;
    }

    int countLiveCells() {
        int liveCells = 0;
        for (auto &row : tab)
            liveCells += std::count(row.begin(), row.end(), true);
        return liveCells;
    }

    void simulate(int iterations) {
        for (int i = 0; i < iterations; i++) {
            std::vector<std::vector<bool>> newTab = tab;
            for (int x = 0; x < width; x++) {
                for (int y = 0; y < height; y++) {
                    int neighbors = countNeighbors(x, y);
                    if (tab[x][y])
                        newTab[x][y] = (neighbors == 2 || neighbors == 3);
                    else
                        newTab[x][y] = (neighbors == 3);
                }
            }
            tab = newTab;
        }
    }

    int countNeighbors(int x, int y) {
        int count = 0;
        for (int dx = -1; dx <= 1; dx++) {
            for (int dy = -1; dy <= 1; dy++) {
                if (dx == 0 && dy == 0) continue;
                int nx = (x + dx + width) % width;
                int ny = (y + dy + height) % height;
                count += tab[nx][ny];
            }
        }
        return count;
    }
};

void calculateErrorForL(int L, int iterations, double p0, int N, double &sem, std::mutex &coutMutex) {
    std::vector<double> densities;
    {
        std::lock_guard<std::mutex> lock(coutMutex);
        std::cout << "L: " << L << "\n";
    }
    
    for (int i = 0; i < N; i++) {
        {
            std::lock_guard<std::mutex> lock(coutMutex);
            std::cout << "i: " << i << " dla L=" << L << "\n";
        }
        LifeGame game(L, L, p0);
        game.simulate(iterations);
        double density = static_cast<double>(game.countLiveCells()) / (L * L);
        densities.push_back(density);
    }
    
    double sum = 0;
    for (double d : densities) sum += d;
    double mean = sum / N;
    
    double variance = 0;
    for (double d : densities) variance += (d - mean) * (d - mean);
    variance /= (N - 1);
    sem = sqrt(variance) / sqrt(N);
    
    {
        std::lock_guard<std::mutex> lock(coutMutex);
        std::cout << "L=" << L << " SEM=" << sem << "\n";
    }
}

int main() {
    std::vector<int> Ls = {10, 100, 200, 500, 1000};
    int iterations = 1000;
    double p0 = 0.5;
    int N = 100;
    
    std::vector<std::thread> threads;
    std::mutex coutMutex; // Mutex do synchronizacji wypisywania do konsoli
    std::vector<double> sems(Ls.size());
    
    // Utworzenie wątków - każdy przetwarza jedną wartość L
    for (size_t idx = 0; idx < Ls.size(); idx++) {
        threads.push_back(std::thread(calculateErrorForL, Ls[idx], iterations, p0, N,
                                      std::ref(sems[idx]), std::ref(coutMutex)));
    }
    
    // Dołączenie wszystkich wątków
    for (auto &t : threads) {
        t.join();
    }
    
    // Zapis wyników do pliku
    std::ofstream file("errors.txt");
    for (size_t i = 0; i < Ls.size(); i++) {
        file << Ls[i] << " " << sems[i] << "\n";
    }
    file.close();
    
    return 0;
}
