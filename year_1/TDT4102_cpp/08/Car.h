#pragma once

class Car{
    int freeSeats;

    public:
        Car(int fS);

        bool hasFreeSeats() const;

        void reserveFreeSeat();
};