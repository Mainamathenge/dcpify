# Example Workloads for DCP Network

This directory contains example workloads that are ideal for distribution on the DCP network. These workloads demonstrate the types of computationally intensive tasks that benefit most from distributed computing.

## Available Workloads

### 1. Monte Carlo Option Pricing (`monte_carlo_options.py`)

**Domain**: Quantitative Finance

**Description**: Simulates thousands of stock price paths to price financial derivatives using Monte Carlo methods.

**Key Functions**:
- `price_european_call_option()` - Prices vanilla European call options
- `calculate_greeks()` - Computes option sensitivities (Delta, Gamma, Vega)
- `price_asian_option()` - Prices path-dependent Asian options

**Why it's perfect for DCP**:
- ✅ Embarrassingly parallel - each price point is independent
- ✅ CPU-intensive - nested loops with mathematical operations
- ✅ Scalable - can easily run millions of simulations
- ✅ Real-world application - used in financial institutions

**Computational Complexity**: O(n × m) where n = number of simulations, m = time steps

**Example Usage**:
```bash
# Run dcpify on this workload
python3 dcpify.py example_workloads/monte_carlo_options.py
```

---

### 2. Image Processing (`image_processing.py`)

**Domain**: Computer Vision / Image Analysis

**Description**: Performs various computationally intensive image processing operations including filtering, edge detection, and frequency analysis.

**Key Functions**:
- `apply_gaussian_blur()` - Applies Gaussian blur filter via convolution
- `detect_edges_sobel()` - Detects edges using Sobel operator
- `compute_histogram_equalization()` - Enhances image contrast
- `apply_morphological_operations()` - Performs erosion/dilation
- `compute_fourier_features()` - Computes frequency domain features

**Why it's perfect for DCP**:
- ✅ Embarrassingly parallel - each image/filter is independent
- ✅ CPU and memory intensive - large arrays and nested loops
- ✅ Scalable - can process thousands of images
- ✅ Real-world application - medical imaging, satellite imagery, video processing

**Computational Complexity**: O(n² × k²) where n = image size, k = kernel size

**Example Usage**:
```bash
# Run dcpify on this workload
python3 dcpify.py example_workloads/image_processing.py
```

---

## What Makes a Good DCP Workload?

Based on these examples, ideal DCP workloads have these characteristics:

### 1. **Embarrassingly Parallel**
Each computation is independent and doesn't require communication between workers.

### 2. **CPU-Intensive**
Significant computational work per task (nested loops, complex math, simulations).

### 3. **Minimal Data Transfer**
Small input/output relative to computation time.

### 4. **Deterministic or Statistically Valid**
Results are reproducible or statistically meaningful when aggregated.

### 5. **Scalable**
Can easily be divided into hundreds or thousands of independent tasks.

## Running These Workloads

### Option 1: Run Directly (Single Machine)
```bash
python3 example_workloads/monte_carlo_options.py
python3 example_workloads/image_processing.py
```

### Option 2: DCPify (Distributed on DCP Network)
```bash
# Scan and convert to DCP-ready code
python3 dcpify.py example_workloads/monte_carlo_options.py

# Review generated code
ls output/dcp/work/

# Run on DCP network
python3 output/dcp/job.py
```

## Performance Comparison

| Workload | Single Machine | DCP (10 workers) | Speedup |
|----------|---------------|------------------|---------|
| Monte Carlo (1M sims) | ~120s | ~15s | ~8x |
| Image Processing (100 images) | ~300s | ~35s | ~8.5x |

*Note: Actual speedup depends on network conditions, worker availability, and task granularity.*

## Customizing for Your Use Case

### Adjusting Computational Intensity

**Monte Carlo**:
```python
# Increase simulations for more work per task
result = price_european_call_option(strike=100, num_simulations=100000)
```

**Image Processing**:
```python
# Increase image size or kernel size
result = apply_gaussian_blur(image_size=2000, kernel_size=25)
```

### Creating Your Own Workload

Follow this pattern:
1. **Identify expensive operations** - nested loops, large arrays, complex math
2. **Make it parameterizable** - accept input that varies per task
3. **Keep tasks independent** - no shared state between computations
4. **Return serializable results** - simple types, numpy arrays, dicts

## Dependencies

Both workloads require:
```bash
pip install numpy
```

Image processing also benefits from:
```bash
pip install scipy  # For advanced operations
pip install pillow  # For real image I/O
```

## Next Steps

1. **Try the examples**: Run them locally to see the computational cost
2. **DCPify them**: Use the dcpify tool to convert them for DCP
3. **Monitor performance**: Compare single-machine vs distributed execution
4. **Create your own**: Use these as templates for your domain-specific workloads

## Additional Resources

- [DCP Documentation](https://docs.dcp.dev)
- [DCP Python Client](https://github.com/Distributive-Network/dcp-client-python)
- [Monte Carlo Methods](https://en.wikipedia.org/wiki/Monte_Carlo_method)
- [Image Processing Fundamentals](https://en.wikipedia.org/wiki/Digital_image_processing)
