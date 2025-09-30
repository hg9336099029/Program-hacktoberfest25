class Solution {
public:
    int myAtoi(string s) {
        int i = 0;
        int n = s.length();
        int sign = 1;
        long result = 0;

        // Step 1: Skip leading whitespace
        while (i < n && s[i] == ' ') {
            i++;
        }

        // Step 2: Check for optional sign
        if (i < n && (s[i] == '+' || s[i] == '-')) {
            sign = (s[i] == '-') ? -1 : 1;
            i++;
        }

        // Step 3: Convert digits until non-digit
        while (i < n && isdigit(s[i])) {
            int digit = s[i] - '0';

            // Step 4: Check overflow
            if (result > (INT_MAX - digit) / 10) {
                return (sign == 1) ? INT_MAX : INT_MIN;
            }

            result = result * 10 + digit;
            i++;
        }

        return static_cast<int>(sign * result);
    }
};
