#include <iostream>
#include <memory>
#include <queue>
#include <string>
#include <unordered_map>

struct Node {
    char ch;
    int freq;
    std::shared_ptr<Node> left;
    std::shared_ptr<Node> right;

    Node(char c, int f) : ch(c), freq(f), left(nullptr), right(nullptr) {}
    Node(std::shared_ptr<Node> l, std::shared_ptr<Node> r)
        : ch('\0'), freq(l->freq + r->freq), left(l), right(r) {}
};

struct Compare {
    bool operator()(const std::shared_ptr<Node>& a, const std::shared_ptr<Node>& b) {
        return a->freq > b->freq;
    }
};

void buildCodes(const std::shared_ptr<Node>& node, const std::string& prefix,
                std::unordered_map<char, std::string>& codes) {
    if (!node) return;
    if (!node->left && !node->right) {
        codes[node->ch] = prefix.empty() ? "0" : prefix;
        return;
    }
    buildCodes(node->left, prefix + "0", codes);
    buildCodes(node->right, prefix + "1", codes);
}

std::shared_ptr<Node> buildTree(const std::string& text) {
    std::unordered_map<char, int> freq;
    for (char ch : text) freq[ch]++;

    std::priority_queue<std::shared_ptr<Node>, std::vector<std::shared_ptr<Node>>, Compare> heap;
    for (const auto& item : freq) heap.push(std::make_shared<Node>(item.first, item.second));
    if (heap.empty()) return nullptr;

    while (heap.size() > 1) {
        auto left = heap.top(); heap.pop();
        auto right = heap.top(); heap.pop();
        heap.push(std::make_shared<Node>(left, right));
    }
    return heap.top();
}

int main() {
    std::string text = "huffman coding creates optimal prefix free codes";
    auto root = buildTree(text);
    std::unordered_map<char, std::string> codes;
    buildCodes(root, "", codes);

    std::string encoded;
    for (char ch : text) encoded += codes[ch];

    std::cout << "Original text: " << text << "\n\nCodes:\n";
    for (const auto& item : codes) {
        std::cout << item.first << ": " << item.second << "\n";
    }
    std::cout << "\nEncoded bits: " << encoded << "\n";
    return 0;
}
