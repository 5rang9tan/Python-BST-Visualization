import warnings
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# 한글 폰트 설정 (맥OS)
plt.rcParams['font.family'] = 'AppleGothic'  # MacOS에서 한글 지원 폰트

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            print(f"루트 노드 {value} 추가")
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                print(f"{value}를 {node.value}의 왼쪽에 추가")
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:  # value >= node.value
            if node.right is None:
                print(f"{value}를 {node.value}의 오른쪽에 추가")
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)

    def delete(self, value):
        print(f"\n삭제할 노드: {value}")
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        if node is None:
            print(f"{value}는 트리에 존재하지 않습니다.")
            return node
        
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # 노드가 삭제될 때의 처리
            if node.left and node.right:  # 차수가 2인 경우
                print(f"{value}를 삭제합니다: 두 자식을 가진 경우")
                print("삭제할 노드가 두 자식을 가지고 있으므로, 대치할 노드로 오른쪽 서브트리의 최소값을 사용합니다.")
                # 오른쪽 서브트리의 최소값으로 대치
                min_larger_node = self._find_min(node.right)
                node.value = min_larger_node.value
                node.right = self._delete_recursive(node.right, min_larger_node.value)
                print(f"{value}의 값을 {min_larger_node.value}로 대치합니다.")
            elif node.left or node.right:  # 단일 자식 노드인 경우
                print(f"{value}를 삭제합니다: 단일 자식 노드 삭제")
                if node.left:
                    print(f"{value}는 왼쪽 자식 {node.left.value}로 대치됩니다.")
                else:
                    print(f"{value}는 오른쪽 자식 {node.right.value}로 대치됩니다.")
                return node.left if node.left else node.right
            else:  # 단일 노드인 경우
                print(f"{value}를 삭제합니다: 단순 삭제")
                print("삭제할 노드가 자식을 가지지 않으므로, 해당 노드를 단순히 삭제합니다.")
                return None
        
        return node

    def _find_min(self, node):
        while node.left is not None:
            node = node.left
        return node

    def in_order_traversal(self, node):
        if node is not None:
            self.in_order_traversal(node.left)
            print(f"[{node.value}] ", end="")
            self.in_order_traversal(node.right)

    def visualize(self, title):
        G = nx.DiGraph()
        self._add_edges(G, self.root)
        pos = self._get_positions(self.root, 0, 0, 1)

        plt.figure(figsize=(10, 6))
        colors = plt.cm.rainbow(np.linspace(0, 1, 10))[::-1]
        node_colors = [colors[i % len(colors)] for i in range(len(self._get_all_values()))]

        nx.draw(G, pos, with_labels=True, arrows=True, node_size=2000, node_color=node_colors, font_size=10, font_weight='bold')
        plt.axis('off')
        plt.title(title)
        plt.show()  # 각 시각화 후 새로운 창 열기

    def _add_edges(self, G, node):
        if node is not None:
            if node.left is not None:
                G.add_edge(node.value, node.left.value)
                self._add_edges(G, node.left)
            if node.right is not None:
                G.add_edge(node.value, node.right.value)
                self._add_edges(G, node.right)

    def _get_positions(self, node, x, y, layer):
        pos = {}
        if node is not None:
            pos[node.value] = (x, y)
            pos.update(self._get_positions(node.left, x - 1 / (2 ** layer), y - 1, layer + 1))
            pos.update(self._get_positions(node.right, x + 1 / (2 ** layer), y - 1, layer + 1))
        return pos

    def _get_all_values(self):
        values = []
        self._in_order_collect(self.root, values)
        return values

    def _in_order_collect(self, node, values):
        if node:
            self._in_order_collect(node.left, values)
            values.append(node.value)
            self._in_order_collect(node.right, values)

# 메인 함수
if __name__ == "__main__":
    bst = BinarySearchTree()
    
    # 시각화하기 좋은 배열
    values = [30, 20, 40, 10, 25, 35, 50]  # 균형 잡힌 배열
    print("배열:", values)

    # 노드 추가
    for value in values:
        print(f"{value}을 추가합니다.")
        bst.insert(value)
        # 추가 후 중위 순회 결과 출력
        print(f"{value} 추가 후 중위 순회 결과: ", end="")
        bst.in_order_traversal(bst.root)
        print("\n")
        # 시각화 창을 보여주기 전에 로그 출력
        bst.visualize(f"이진 탐색 트리 ({value} 추가 후)")

    # 삭제할 노드 선택 (30, 25, 20, 10)
    values_to_delete = [30, 25, 20, 10]  # 예시로 삭제할 노드
    print("삭제할 노드:", values_to_delete)

    for value in values_to_delete:
        # 삭제 로그 출력
        print(f"{value}을 삭제합니다.")
        bst.delete(value)
        # 삭제 후 중위 순회 결과 출력
        print(f"{value} 삭제 후 중위 순회 결과: ", end="")
        bst.in_order_traversal(bst.root)
        print("\n")
        # 시각화 창을 보여주기 전에 로그 출력
        bst.visualize(f"이진 탐색 트리 ({value} 삭제 후)")
