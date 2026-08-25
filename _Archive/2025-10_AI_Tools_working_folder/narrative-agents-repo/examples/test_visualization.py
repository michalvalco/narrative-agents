"""
Quick Test Script - Verify Visualization System

Run this to test your visualization setup before running the full benchmark.
Creates a small demo with dummy data to verify matplotlib is working.
"""

import sys
import os

# Add parent directory to path (for imports)
sys.path.insert(0, os.path.abspath('..'))

print("=" * 70)
print("VISUALIZATION SYSTEM TEST")
print("=" * 70)

# Test 1: Import dependencies
print("\n📦 Testing dependencies...")
try:
    import matplotlib.pyplot as plt
    print("  ✅ matplotlib imported successfully")
except ImportError as e:
    print(f"  ❌ matplotlib not found: {e}")
    print("  → Run: pip install matplotlib")
    sys.exit(1)

try:
    import numpy as np
    print("  ✅ numpy imported successfully")
except ImportError as e:
    print(f"  ❌ numpy not found: {e}")
    print("  → Run: pip install numpy")
    sys.exit(1)

try:
    import seaborn as sns
    print("  ✅ seaborn imported successfully (optional)")
except ImportError:
    print("  ⚠️  seaborn not found (optional but recommended)")
    print("  → Run: pip install seaborn")

# Test 2: Import visualization module
print("\n📊 Testing visualization module...")
try:
    from visualizations import create_full_benchmark_figure
    print("  ✅ visualizations.py imported successfully")
except ImportError as e:
    print(f"  ❌ visualizations.py not found: {e}")
    print("  → Make sure visualizations.py is in the examples/ directory")
    sys.exit(1)

# Test 3: Create dummy data
print("\n🎲 Creating test data...")
dummy_data = {
    'agent_names': ['Test-Agent-1', 'Test-Agent-2', 'Test-Agent-3'],
    'storage_pct': [30.0, 25.0, 100.0],
    'trait_counts': [3, 2, 0],
    'timeline_data': {
        'Test-Agent-1': [(10, 0), (20, 1), (30, 2), (40, 3)],
        'Test-Agent-2': [(10, 0), (20, 1), (30, 2), (40, 2)],
        'Test-Agent-3': [(10, 0), (20, 0), (30, 0), (40, 0)],
    },
    'efficiency': [30.0, 25.0, 100.0],
    'coherence': [75.0, 68.0, 35.0],
    'decision_matrix': np.array([
        [1.0, 0.8, 0.5, 0.3, 0.9],  # Agent 1: Mostly engaging
        [0.8, 0.6, 0.4, 0.2, 0.7],  # Agent 2: Moderately engaging
        [0.3, 0.3, 0.5, 0.3, 0.4]   # Agent 3: Mostly cautious
    ]),
    'situations': ['Challenge', 'Risk', 'Routine', 'Unknown', 'Creative']
}
print("  ✅ Test data created")

# Test 4: Generate visualization
print("\n🎨 Generating test visualization...")
output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'test_visualization.png')

try:
    fig = create_full_benchmark_figure(dummy_data, output_path)
    print(f"  ✅ Visualization created successfully!")
    print(f"  📁 Saved to: {output_path}")
except Exception as e:
    print(f"  ❌ Visualization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Verify file exists
print("\n📁 Verifying output file...")
if os.path.exists(output_path):
    file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
    print(f"  ✅ File exists: {output_path}")
    print(f"  📊 File size: {file_size:.2f} MB")
else:
    print(f"  ❌ File not created: {output_path}")
    sys.exit(1)

# Success!
print("\n" + "=" * 70)
print("✅ ALL TESTS PASSED!")
print("=" * 70)
print("\nYour visualization system is working correctly!")
print("\nNext steps:")
print("  1. Run the full benchmark: python memory_efficiency_viz.py")
print("  2. Or view the test output: open", output_path)
print("\n" + "=" * 70)
