#include "argparse/argparse.hpp"
#include "BBSRandom.h"
#include "Cipher.h"
#include "ElGamal.h"
#include "RSA.h"
#include "string_utils.h"
#include <cstdlib>
#include <exception>
#include <functional>
#include <gmpxx.h>
#include <iostream>
#include <map>
#include <regex>
#include <string>
#include <vector>

using namespace std;

const vector<string> VALID_ALGORITHMS = { "elgamal", "rsa" };
const string VALID_ALGOS = join(VALID_ALGORITHMS, ", ");

const vector<string> VALID_OPERATIONS = { "attack", "decrypt", "encrypt" };
const string VALID_OPS = join(VALID_OPERATIONS, ", ");

struct MyArgs : public argparse::Args {
    string &algorithm = kwarg("a,algorithm", "Valid options: (" + VALID_ALGOS + ")");
    string &operation = kwarg("o,operation", "Valid options: (" + VALID_OPS + ")");
    string &inputFile = kwarg("i,inputfile", "File path to an encrypted message or clear-text message");
    string &keyFile   = kwarg("k,keyfile",   "Use this name for the generated key files.  Otherwise, use the defaults.").set_default("");
    string &recipientPubKey = kwarg("p,pubKey", "The public key of the recipient").set_default("");
};

void printAndExit(const string msg, const int code = 0)
{
    cerr << colorString(msg, code == EXIT_FAILURE) << '\n';
    exit(code);
}

void run(const MyArgs& args)
{
    map<string, function<unique_ptr<Cipher>()>> factory;

    if (args.keyFile.empty()) {
        factory["elgamal"] = []() { return make_unique<ElGamal>(); };
        factory["rsa"] = []() { return make_unique<RSA>(); };
    } else {
        const string keyFile = args.keyFile;

        factory["elgamal"] = [keyFile]() {
            return make_unique<ElGamal>(keyFile + ".pub", keyFile);
        };
        factory["rsa"] = [keyFile]() {
            return make_unique<RSA>(keyFile + ".pub", keyFile);
        };
    }

    auto algorithm = factory[args.algorithm]();

    try {
        if (args.operation != "encrypt") {
            algorithm->run(args.operation, args.inputFile);
        } else {
            const int BASE = 10;
            const mpz_class pubKey(args.recipientPubKey, BASE);
            algorithm->run(args.operation, args.inputFile, pubKey);
        }
    } catch (const exception& err) {
        printAndExit(err.what(), EXIT_FAILURE);
    }
}

bool isPositiveInteger(const std::string& s) {
    const regex positiveIntegerRegex("^[1-9][0-9]*$");
    return regex_match(s, positiveIntegerRegex);
}

bool validateStringChoice(const string choice, const vector<string>& options)
{
    for (const string& option : options) {
        if (choice == option) return true;
    }

    return false;
}

int main(int argc, char* argv[])
{
    auto args = argparse::parse<MyArgs>(argc, argv);
    const string algorithm = lower(args.algorithm);
    const string operation = lower(args.operation);

    if (!validateStringChoice(algorithm, VALID_ALGORITHMS)) {
        string msg = "ERROR: Invalid algorithm.  Valid options: " + VALID_ALGOS;
        printAndExit(msg, EXIT_FAILURE);
    }

    if (!validateStringChoice(operation, VALID_OPERATIONS)) {
        string msg = "ERROR: Invalid operation.  Valid options: " + VALID_OPS;
        printAndExit(msg, EXIT_FAILURE);
    }

    if (operation == "encrypt" && !isPositiveInteger(args.recipientPubKey)) {
        string msg = "ERROR: Invalid recipient public key.  Must be a positive integer.";
        printAndExit(msg, EXIT_FAILURE);
    }

    args.algorithm = algorithm;
    args.operation = operation;
    run(args);

    return 0;
}