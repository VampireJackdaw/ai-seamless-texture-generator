// Optional C++ acceleration kernel for seam blending and torus noise.
// Build with:  python setup.py build_ext --inplace  (pybind11)
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <algorithm>

namespace py = pybind11;

// Blend a horizontal band between top/bottom rows to force wrap-safety.
py::array_t<float> blend_edges(py::array_t<float> tile, int band) {
    auto buf = tile.request();
    float* ptr = static_cast<float*>(buf.ptr);
    const auto h = static_cast<int>(buf.shape[0]);
    const auto w = static_cast<int>(buf.shape[1]);
    const auto c = static_cast<int>(buf.shape[2]);
    band = std::min({band, h / 4, w / 4});
    for (int i = 0; i < band; ++i) {
        const float t = static_cast<float>(i + 1) / (band + 1);
        for (int x = 0; x < w; ++x) {
            for (int k = 0; k < c; ++k) {
                float& top = ptr[(i * w + x) * c + k];
                float& bot = ptr[((h - 1 - i) * w + x) * c + k];
                const float blended = top * (1 - t) + bot * t;
                bot = bot * (1 - t) + top * t;
                top = blended;
            }
        }
    }
    return tile;
}

PYBIND11_MODULE(texturegen_kernel, m) {
    m.doc() = "Native acceleration kernels for ai-seamless-texture-generator";
    m.def("blend_edges", &blend_edges, "Blend tile edges for seamlessness",
          py::arg("tile"), py::arg("band") = 8);
}