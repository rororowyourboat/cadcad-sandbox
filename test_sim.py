from model.experiment import run_simple_sim

# Run a small simulation and get the DataFrame
df = run_simple_sim(
    timesteps=5,    # Small number of timesteps for clarity
    samples=2,      # Run 2 simulations to see how runs are organized
    beta=0.3,
    gamma=0.1,
    population=1000
)

# Additional analysis of the DataFrame structure
print("\nUnique values in each column:")
for col in df.columns:
    print(f"\n{col}:")
    print(df[col].unique())

print("\nLast few rows:")
print(df.tail())

print("\nShape of DataFrame:")
print(df.shape)
