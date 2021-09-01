class Dummy{
    public:
    int *num;
    Dummy() {
        num = new int{0};
    }
    Dummy(const Dummy&);

    ~Dummy() {
        delete num;
    }
    Dummy& operator=(Dummy);
};

void dummyTest();


