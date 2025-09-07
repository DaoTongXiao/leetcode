class TrieNode:
    def __init__(self):
        self.children: dict[str, "TrieNode"] = {}  # 子节点映射：字符 -> TrieNode
        self.word: str | None = None  # 如果是单词结尾，存储完整单词，否则 None


class Solution:
    def findWords(self, board: list[list[str]], words: list[str]) -> list[str]:
        # 处理空 board
        if not board or not board[0]:
            return []

        # 1️⃣ 构建 Trie
        root = TrieNode()
        for word in words:
            node = root
            for c in word:
                if c not in node.children:
                    node.children[c] = TrieNode()  # 创建新节点
                node = node.children[c]  # 移动到子节点
            node.word = word  # 标记：从根到此节点构成 word

        m, n = len(board), len(board[0])
        res = set()  # 用 set 避免重复添加同一个单词

        # 2️⃣ DFS 回溯函数
        def dfs(i, j, node):
            # 越界 或 已访问过（用 '#' 标记）
            if i < 0 or i >= m or j < 0 or j >= n or board[i][j] == "#":
                return

            c = board[i][j]  # 当前字符

            # Trie 中没有以当前字符开头的路径 → 剪枝！
            if c not in node.children:
                return

            # 同步移动到 Trie 的下一个节点
            node = node.children[c]

            # ✅ 如果当前节点是一个完整单词，加入结果
            if node.word:
                res.add(node.word)
                # 注意：不要 return！因为可能有更长的单词，比如 "eat" 和 "eats"

            # 3️⃣ 回溯标记：防止重复使用当前格子
            temp = board[i][j]
            board[i][j] = "#"

            # 4️⃣ 递归四个方向
            dfs(i + 1, j, node)
            dfs(i - 1, j, node)
            dfs(i, j + 1, node)
            dfs(i, j - 1, node)

            # 5️⃣ 回溯恢复
            board[i][j] = temp

        # 6️⃣ 从每个格子作为起点开始搜索
        for i in range(m):
            for j in range(n):
                dfs(i, j, root)

        return list(res)


if __name__ == "__main__":
    board = [
        ["o", "a", "a", "n"],
        ["e", "t", "a", "e"],
        ["i", "h", "k", "r"],
        ["i", "f", "l", "v"],
    ]
    words = ["oath", "pea", "eat", "rain"]
    print(Solution().findWords(board, words))
