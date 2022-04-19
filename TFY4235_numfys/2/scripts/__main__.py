from . import plot, data, drift
import numpy as np

def main():
    plot.trajectories()#all = True, legend = False)
    #plot.hist(block=True)

    d = data.get("particles")
    t = data.get("time")
    #v_d = drift.drift(d, t[1]-t[0])
    v_a = drift.average(d, t[-1]-t[0])
    del d
    del t
    #print(f"Drift velocity mean: {np.mean(v_d)}")
    #print(f"Drift velocity std:  {np.std(v_d)}")

    print(f"Drift velocity mean: {np.mean(v_a)}")
    print(f"Drift velocity std:  {np.std(v_a)}")

    #plot.plt.plot(np.linspace(0,1,v_a.shape[0]), v_a)
    #plot.plt.show()
    #plot.drift_velocities(v_d, title="Drift", block=False)
    plot.drift_velocities(v_a, title="Average")
    if input("Save? "):
        print("Saving data...")
        data.save()
        print("Saving complete.")

if __name__ == "__main__":
    main()
