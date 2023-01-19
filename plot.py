import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

benchmark = pd.read_csv("benchmark.txt", sep=" ")

time_rel = np.array([i for i in benchmark['time']])
mem_rel = np.array([float(i) for i in benchmark['mem']])

for g, d in benchmark.groupby(['N', 'simplify']):
    btime = d['time'][d['method'] == 'bookmark']
    time_rel_g = d['time'].div(float(btime))
    time_rel[d.index] = time_rel_g
    bmem = d['mem'][d['method'] == 'bookmark']
    mem_rel_g = d['mem'].div(float(bmem))
    mem_rel[d.index] = mem_rel_g

benchmark["time_rel"] = time_rel
benchmark["mem_rel"] = mem_rel

g = sns.FacetGrid(benchmark, col="simplify", hue="method")
g.map(sns.scatterplot, "N", "time_rel")
g.add_legend()
g.set(ylim=(0, 1.5))

for ax in g.axes[0]:
    for y in np.arange(0.25, 1.5, 0.25):
        ax.axhline(y, ls="dashed", color="gray", alpha=0.25)

plt.savefig("benchmark_time_rel.png")

g = sns.FacetGrid(benchmark, col="simplify", hue="method")
g.map(sns.scatterplot, "N", "mem_rel")
g.add_legend()

plt.savefig("benchmark_mem_rel.png")

# Now, plot absolute timings/mem use

g = sns.FacetGrid(benchmark, col="simplify", hue="method")
time = benchmark["time"]/60.0/60.0
benchmark["hours"] = time
g.map(sns.scatterplot, "N", "hours", alpha=0.5)
g.set(ylabel="Time (hours)")
g.add_legend()
plt.savefig("benchmark_time.png")

mem = benchmark["mem"]/1024.0/1024.0
benchmark["GB"] = mem
g = sns.relplot(benchmark, x="N", y="GB",
                col="simplify", hue="method", style="method")
# g.map(sns.scatterplot, "N", "GB", alpha=0.5)
g.set(ylabel="Peak memory (GB)")
g.add_legend()
plt.savefig("benchmark_mem.png")

# GB difference from bookmark
gb = np.array([i for i in benchmark["GB"]])
for g, d in benchmark.groupby(['N', 'simplify']):
    gb_bookmark = d['GB'][d['method'] == 'bookmark']
    gb_g = d['GB'].sub(float(gb_bookmark))
    gb[d.index] = gb_g

benchmark["GBdelta"] = gb

g = sns.relplot(benchmark, x="N", y="GBdelta",
                col="simplify", hue="method", style="method")
# g.map(sns.scatterplot, "N", "GB", alpha=0.5)
g.set(ylabel="Peak memory delta from bookmark (GB)")
g.add_legend()
plt.savefig("benchmark_delta.png")
