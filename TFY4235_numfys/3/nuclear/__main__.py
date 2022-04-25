from nuclear.utils import plot, rng

def main():
    d = []
    for _ in range(10000):
        d.append(rng.linear_congruential())
    
    plot.hist(d)

if __name__ == "__main__":
    main()
