#include "string_utils.h"
#include <cctype>     // Required for tolower()

std::string colorString(const std::string& str, const bool printRed)
{
    const std::string BOLD_RED = "\033[1;31m";
    const std::string GREEN = "\033[32m";
    const std::string RESET_COLOR = "\033[0m";
    const std::string TEXT_COLOR = (printRed) ? BOLD_RED : GREEN;
    return TEXT_COLOR + str + RESET_COLOR;
}

std::string join(const std::vector<std::string>& vec, const std::string& delimiter)
{
    std::string result;
    
    for(size_t n = 0; n < vec.size(); n++) {
        result += vec[n];

        if (n < vec.size() - 1) {
            result += delimiter;
        }
    }

    return result;
}

std::string lower(std::string str)
{
    for (char& c : str) {
        c = std::tolower(static_cast<unsigned char>(c));
    }
    return str;
}