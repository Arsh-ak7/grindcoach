#ifndef LC_UTILS_H
#define LC_UTILS_H

#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
#include <map>
#include <unordered_map>
#include <set>
#include <unordered_set>
#include <queue>
#include <stack>
#include <numeric>
#include <cmath>
#include <functional>
#include <iomanip>

using namespace std;

// --- Forward Declarations for Printing ---
template <typename T> ostream& operator<<(ostream& os, const vector<T>& v);
template <typename T> ostream& operator<<(ostream& os, const set<T>& s);
template <typename T> ostream& operator<<(ostream& os, const multiset<T>& s);
template <typename T> ostream& operator<<(ostream& os, const unordered_set<T>& s);
template <typename K, typename V> ostream& operator<<(ostream& os, const map<K, V>& m);
template <typename K, typename V> ostream& operator<<(ostream& os, const unordered_map<K, V>& m);
template <typename T1, typename T2> ostream& operator<<(ostream& os, const pair<T1, T2>& p);

// --- Definitions ---

// Pair
template <typename T1, typename T2>
ostream& operator<<(ostream& os, const pair<T1, T2>& p) {
    return os << "(" << p.first << ", " << p.second << ")";
}

// Vector
template <typename T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); ++i) {
        if (i > 0) os << ", ";
        os << v[i];
    }
    return os << "]";
}

// Set
template <typename T>
ostream& operator<<(ostream& os, const set<T>& s) {
    os << "{";
    bool first = true;
    for (const auto& item : s) {
        if (!first) os << ", ";
        os << item;
        first = false;
    }
    return os << "}";
}

// Map
template <typename K, typename V>
ostream& operator<<(ostream& os, const map<K, V>& m) {
    os << "{";
    bool first = true;
    for (const auto& item : m) {
        if (!first) os << ", ";
        os << item.first << ": " << item.second;
        first = false;
    }
    return os << "}";
}

// Unordered Map
template <typename K, typename V>
ostream& operator<<(ostream& os, const unordered_map<K, V>& m) {
    os << "{";
    bool first = true;
    for (const auto& item : m) {
        if (!first) os << ", ";
        os << item.first << ": " << item.second;
        first = false;
    }
    return os << "}";
}

// --- LeetCode Structures ---

struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}

    // Helper to print linked list
    friend ostream& operator<<(ostream& os, ListNode* head) {
        vector<int> vals;
        while (head) {
            vals.push_back(head->val);
            head = head->next;
        }
        return os << vals;
    }
};

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}

    // Very simple printer (prints value only for now)
    friend ostream& operator<<(ostream& os, TreeNode* root) {
        if (!root) return os << "null";
        return os << "TreeNode(" << root->val << ")";
    }
};

// --- Debug Macro ---
#define DBG(x) cerr << "\033[34m[DEBUG] " << #x << " = " << (x) << "\033[0m" << endl;

// --- Input Parsing Helpers ---

// Helper to remove surrounding quotes if present
string strip_quotes(string s) {
    if (s.size() >= 2 && s.front() == '"' && s.back() == '"') {
        return s.substr(1, s.size() - 2);
    }
    return s;
}

// Very basic vector parser: [1,2,3] -> vector<int>
// Does NOT handle nested vectors robustly yet, designed for 1D simple cases
template <typename T>
vector<T> parse_vector(string s) {
    vector<T> res;
    if (s.empty()) return res;
    if (s.front() == '[') s = s.substr(1);
    if (s.back() == ']') s.pop_back();

    stringstream ss(s);
    string item;
    while (getline(ss, item, ',')) {
        // Trim spaces
        item.erase(0, item.find_first_not_of(" \t"));
        item.erase(item.find_last_not_of(" \t") + 1);

        stringstream item_ss(item);
        T val;
        // For strings, handle quotes
        if constexpr (is_same_v<T, string>) {
             res.push_back(strip_quotes(item));
        } else {
            item_ss >> val;
            res.push_back(val);
        }
    }
    return res;
}

// Function to read entire stdin into a string (for persistent/pipe mode)
string read_all_stdin() {
    string content, line;
    while (getline(cin, line)) {
        content += line;
    }
    return content;
}

// Helper to read a single line from stdin
string read_line() {
    string s;
    getline(cin, s);
    return s;
}

#endif
