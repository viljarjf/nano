from scattering import plot, rng

def main():
    d = []
    p = 1
    for _ in range(10000):
        i = rng.linear_congruential(42.8, 69.1, 13370)
      
        if i/1337 in d and p:
            p = 0
            print(len(d))
        d.append(i/1337)
    
    plot.hist(d)

if __name__ == "__main__":
    main()
