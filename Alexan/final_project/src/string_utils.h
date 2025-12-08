#ifndef STRING_UTILS_H
#define STRING_UTILS_H

#include <string>
#include <vector>

std::string colorString(const std::string& str, const bool printRed=false);
std::string join(const std::vector<std::string>& vec, const std::string& delimiter);
std::string lower(std::string str);

#endif