#include <vector>
#include <algorithm>
#include <numeric>
#include <iterator>
#include <time.h>
#include <random>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

namespace py = pybind11;


// See src/python/funcs for python version
float photon_propagation (
    py::array_t<float> mu,    //  (np.array)  - Array with attenuation coefficient
    const float& thickness,   //  (float)     - Thickness of material
    const int& N              //  (int)       - Number of photons to simulate
) {
    py::buffer_info mu_buff = mu.request();

    float *mu_ptr = static_cast<float *>(mu_buff.ptr);

    // Stepsize
    float dx = thickness / static_cast<float>(mu_buff.size - 1);

    // Probability of scattering or absorption
    std::vector<float> p(mu_buff.size);
    for (int i = 0; i < mu_buff.size; i++) p[i] = mu_ptr[i] * dx;

    // Photons per discretization step
    int photons_cont = N;

    // Random generator for uniform floating point distribution [0, 1)
    std::random_device dev;
    std::mt19937 rng(dev());

    std::uniform_real_distribution<double> ureal_dist(0.0, 1.0);

    std::vector<float> z(photons_cont);

    for (int i = 0; i < mu_buff.size; i++) {
        std::generate(
            z.begin(), z.begin() + photons_cont, 
            [&p, &i, &ureal_dist, &rng]() -> float { return static_cast<float>(ureal_dist(rng)) > p[i]; }
        );
        
        photons_cont = std::accumulate(z.begin(), z.begin() + photons_cont, 0);
    }

    return static_cast<float>(photons_cont) / N;
}

PYBIND11_MODULE(cpp_funcs, m) {
    m.doc() = "Monte Carlo Simulation of X-ray imaging functions";

    m.def("photon_propagation", &photon_propagation);
}
