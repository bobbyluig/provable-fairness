#include <algorithm>
#include <fstream>
#include <iostream>
#include <random>
#include <vector>

int main() {
  static const unsigned int kIndices = 52;

  std::mt19937 initial_mt(42);
  std::vector<uint32_t> initial_indices(kIndices);
  std::iota(initial_indices.begin(), initial_indices.end(), 0);
  std::shuffle(initial_indices.begin(), initial_indices.end(), initial_mt);

  for (unsigned int &x : initial_indices)
    std::cout << x << ',';
  std::cout << std::endl;

  std::vector<uint32_t> indices(kIndices);
  std::iota(indices.begin(), indices.end(), 0);;

  for (uint32_t i = 0;; i++) {
    std::vector<uint32_t> indices_copy = indices;
    std::mt19937 generator(i);
    std::shuffle(indices_copy.begin(), indices_copy.end(), generator);

    if (std::equal(initial_indices.begin(), initial_indices.begin() + 4, indices_copy.begin())) {
      std::cout << i << ":";
      for (unsigned int &x : indices_copy)
        std::cout << x << ',';
      std::cout << std::endl;
    }

    if (i == std::numeric_limits<uint32_t>::max()) {
      break;
    }
  }
}