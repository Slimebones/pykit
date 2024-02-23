from typing import Callable, Generic, Self

from pykit.types import T


class TreeNode(Generic[T]):
    def __init__(self, val: T, childs: list[Self]):
        self.val = val
        self.childs = childs

    def __str__(self) -> str:
        return f"<TreeNode val = {self.val}, childs = {self.childs}>"

class ReversedTreeNode(Generic[T]):
    def __init__(self, val: T, parent: Self | None = None):
        self.val = val
        self.parent = parent

    def __str__(self) -> str:
        return f"<ReversedTreeNode val = {self.val}, parent = {self.parent}>"

class TreeUtils:
    @classmethod
    async def reverse(
        cls,
        root_node: TreeNode[T],
        *,
        _parent_rnode: ReversedTreeNode[T] | None = None,
    ) -> list[ReversedTreeNode[T]]:
        root_rnode = ReversedTreeNode(root_node.val, _parent_rnode)
        if not root_node.childs:
            return [root_rnode]

        f = []
        for child in root_node.childs:
            f.extend(await cls.reverse(child, _parent_rnode=root_rnode))

        return f

    @classmethod
    async def print(
        cls,
        root_node: TreeNode,
        print_action: Callable[[str], None] = print,
    ):
        def uncover(node: TreeNode, depth: int) -> str:
            msg = ""
            tabs = "\t" * depth

            for c in node.childs:
                msg += f"{tabs} - {c}\n"
                msg += uncover(c, depth + 1)

            return msg

        msg = f"x {root_node}\n"
        depth = 1

        msg += uncover(root_node, depth)
        print_action(msg.strip())

