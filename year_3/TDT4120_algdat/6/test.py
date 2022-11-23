# stavkutting

P = [1,4, 3, 6, 8, 5, 9]
def cut(n):
    if n == 0:
        return 0
    m = -1
    for i in range(n):
        m = max(m, P[i] + cut(n-i-1))
    return m

def main():
    print(cut(7))

if __name__ == "__main__":
    main()