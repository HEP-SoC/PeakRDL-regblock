from typing import TYPE_CHECKING, Optional, List
import textwrap

from systemrdl.walker import RDLListener, RDLWalker

if TYPE_CHECKING:
    from systemrdl.node import AddressableNode, Node

class Body:

    def __init__(self) -> None:
        self.children = []

    def __str__(self) -> str:
        s = '\n'.join((str(x) for x in self.children))
        return s

class LoopBody(Body):
    def __init__(self, dim: int, iterator: str, i_type: str) -> None:
        super().__init__()
        self.dim = dim
        self.iterator = iterator
        self.i_type = i_type

    def __str__(self) -> str:
        s = super().__str__()
        return (
            f"for({self.i_type} {self.iterator}=0; {self.iterator}<{self.dim}; {self.iterator}++) begin\n"
            + textwrap.indent(s, "    ")
            + "\nend"
        )



class ForLoopGenerator:
    i_type = "int"

    def __init__(self) -> None:
        self._loop_level = 0
        self._stack = []

    @property
    def current_loop(self) -> Body:
        return self._stack[-1]

    def push_loop(self, dim: int) -> None:
        i = f"i{self._loop_level}"
        b = LoopBody(dim, i, self.i_type)
        self._stack.append(b)
        self._loop_level += 1

    def add_content(self, s: str) -> None:
        self.current_loop.children.append(s)

    def pop_loop(self) -> None:
        b = self._stack.pop()

        if b.children:
            # Loop body is not empty. Attach it to the parent
            self.current_loop.children.append(b)
        self._loop_level -= 1

    def start(self):
        assert not self._stack
        b = Body()
        self._stack.append(b)

    def finish(self) -> Optional[str]:
        b = self._stack.pop()
        assert not self._stack

        if not b.children:
            return None
        return str(b)

class RDLForLoopGenerator(ForLoopGenerator, RDLListener):

    def get_content(self, node: 'Node') -> Optional[str]:
        self.start()
        walker = RDLWalker()
        walker.walk(node, self, skip_top=True)
        return self.finish()

    def enter_AddressableComponent(self, node: 'AddressableNode') -> None:
        if not node.is_array:
            return

        for dim in node.array_dimensions:
            self.push_loop(dim)

    def exit_AddressableComponent(self, node: 'AddressableNode') -> None:
        if not node.is_array:
            return

        for _ in node.array_dimensions:
            self.pop_loop()
