#include <iostream>
using namespace std;

// This program calculates the factorial of a number using an iterative approach
int main() {
    int n;
    long long factorial = 1;

    cout << "Enter a number: ";
    cin >> n;

    // Loop from 1 to n and multiply to get factorial
    for (int i = 1; i <= n; i++) {
        factorial *= i;
    }

    cout << "Factorial of " << n << " is " << factorial << endl;
    return 0;
}
