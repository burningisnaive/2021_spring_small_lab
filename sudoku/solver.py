from __future__ import annotations

from typing import List, Optional, Set

# You may remove this import if you don't use it in your code.
from adts import Queue

from puzzle import Puzzle


class Solver:
    """"
    A solver for full-information puzzles. This is an abstract class
    and purely provides the interface for our solve method.
    """

    # You may NOT change the interface to the solve method.
    # Note the optional parameter seen and its type.
    # Your implementations of this method in the two subclasses should use seen
    # to keep track of all puzzle states that you encounter during the
    # solution process.
    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        raise NotImplementedError

class DfsSolver(Solver):
    """"
    A solver for full-information puzzles that uses
    a depth first search strategy.
    """

    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        stack = []
        stack.append(puzzle)
        child2parent = {}
        child2parent[str(puzzle)] = [None]

        while(len(stack)>0):
            parent = stack.pop(-1)
            if parent.is_solved() == True:
                solved = parent 
                break

            next_states = parent.extensions()
            if seen is not None:
                next_unseen = [s for s in next_states if str(s) not in seen]
            else:
                next_unseen = next_states

            for child in next_unseen:
                str_child = str(child)
                if str_child not in child2parent:
                    child2parent[str_child] = []
                child2parent[str_child].append(parent)
                stack.append(child)
        else:
            return []

        child = solved
        path = [child]
        parent = child2parent[str(child)][0]
        while(parent is not None):
            child = parent
            path.insert(0, child)
            parent = child2parent[str(child)][0]

        return path      


class BfsSolver(Solver):
    """"
    A solver for full-information puzzles that uses
    a breadth first search strategy.
    """

    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        queue = Queue()
        queue.enqueue(puzzle)
        child2parent = {}
        child2parent[str(puzzle)] = [None]

        while(not queue.is_empty()):
            parent = queue.dequeue()
            if parent.is_solved() == True:
                solved = parent 
                break

            next_states = parent.extensions()
            if seen is not None:
                next_unseen = [s for s in next_states if str(s) not in seen]
            else:
                next_unseen = next_states

            for child in next_unseen:
                str_child = str(child)
                if str_child not in child2parent:
                    child2parent[str_child] = []
                child2parent[str_child].append(parent)
                queue.enqueue(child)
        else:
            return []
        
        child = solved
        path = [child]
        parent = child2parent[str(child)][0]
        while(parent is not None):
            child = parent
            path.insert(0, child)
            parent = child2parent[str(child)][0]

        return path    
