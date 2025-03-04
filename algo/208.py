class Trie:

    def __init__(self):
        self.children = dict()
        self.end = False

    def insert(self, word: str) -> None:
        node = self
        for w in word:
            if w not in node.children:
                node.children[w] = Trie()
            node = node.children[w]
        node.end = True
        
    def search(self, word: str) -> bool:
        node = self
        for w in word:
            if w not in node.children:
                return False
            node = node.children[w]
        return node.end

    def startsWith(self, prefix: str) -> bool:
        node = self
        for w in prefix:
            if w not in node.children:
                return False
            node = node.children[w]
        return True
        
trie = Trie()
trie.insert("apple")
print(trie.search("apple"))
print(trie.search("app"))
print(trie.startsWith("app"))
trie.insert("app")
print(trie.search("app"))
