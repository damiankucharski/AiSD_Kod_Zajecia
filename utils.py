import numpy as np
import matplotlib.pyplot as plt
from functools import partial
from matplotlib.patches import Rectangle
from IPython.display import display
from graphviz import Digraph
from IPython.display import clear_output


class InteractiveArray:
    def __init__(self, arr, stats=False, xticks=None, yticks=None):
        self.arr = np.array(arr)
        self.stats = stats
        self.highlight_rects = []
        self.ax = None
        self.shape = arr.shape

        if xticks is not None:
            self.xticks = xticks
        else:
            self.xticks = np.arange(arr.shape[0])
        if len(arr.shape) > 1:
            if yticks is not None:
                self.yticks = yticks
            else:
                self.yticks = np.arange(arr.shape[1])

    def sum(self, axis=None):
        return InteractiveArray(np.sum(self.arr, axis=axis))

    def update_stats(self):
        """Calculate and update statistics for the highlighted portion of the array."""
        highlighted_elements = []
        for rect in self.highlight_rects:
            row, col = int(rect.xy[1] + 0.5), int(rect.xy[0] + 0.5)
            if len(self.arr.shape) == 1:
                highlighted_elements.append(self.arr[col])
            else:
                highlighted_elements.append(self.arr[row, col])

        if not highlighted_elements:
            plt.title("")
            plt.draw()
            return

        min_val = np.min(highlighted_elements)
        max_val = np.max(highlighted_elements)
        median_val = np.median(highlighted_elements)
        mean_val = np.mean(highlighted_elements)
        std_val = np.std(highlighted_elements)
        sum = np.sum(highlighted_elements)

        title = f"Min: {min_val}, Max: {max_val}, Median: {median_val}, Mean: {mean_val:.2f}, Std: {std_val:.2f}, Sum: {sum:.2f}"
        plt.title(title)
        plt.draw()

    def onclick(self, event):
        """Handle click events and highlight or unhighlight the selected cell."""
        col = int(np.floor(event.xdata + 0.5))
        row = int(np.floor(event.ydata + 0.5))

        for rect in self.highlight_rects:
            if rect.xy == (col - 0.5, row - 0.5):
                rect.remove()
                self.highlight_rects.remove(rect)
                self.update_stats()
                plt.draw()
                return

        rect = Rectangle((col - 0.5, row - 0.5), 1, 1, linewidth=2, edgecolor="r", facecolor="none")
        self.highlight_rects.append(rect)
        self.ax.add_patch(rect)
        self.update_stats()
        plt.draw()

    def display(self, clear=True):
        """Display the array with interactivity."""
        if clear:
            clear_output(wait=True)
        if len(self.arr.shape) == 1:
            fig, self.ax = plt.subplots()
            self.ax.matshow(self.arr[np.newaxis, :], cmap="coolwarm", aspect="auto")
            self.ax.set_yticklabels([])
            self.ax.set_xticks(np.arange(len(self.arr)))
            self.ax.set_xticklabels(self.xticks)
            self.ax.set_yticks([])
            for i, v in enumerate(self.arr):
                self.ax.text(i, 0, str(v), va="center", ha="center")
        elif len(self.arr.shape) == 2:
            fig, self.ax = plt.subplots()
            self.ax.matshow(self.arr, cmap="Blues")
            for i in range(self.arr.shape[0]):
                for j in range(self.arr.shape[1]):
                    self.ax.text(j, i, str(self.arr[i, j]), va="center", ha="center")

            self.ax.set_xticks(np.arange(len(self.arr)))
            self.ax.set_xticklabels(self.xticks)

            self.ax.set_yticks(np.arange(len(self.arr[0])))
            self.ax.set_yticklabels(self.yticks)

        else:
            print("Array dimensions not supported.")
            return

        fig.canvas.mpl_connect("button_press_event", partial(self.onclick))
        if self.stats:
            self.update_stats()
        plt.show()

    def __add__(self, other):
        if isinstance(other, InteractiveArray):
            return InteractiveArray(self.arr + other.arr)

        return InteractiveArray(self.arr + other)

    def __sub__(self, other):
        if isinstance(other, InteractiveArray):
            return InteractiveArray(self.arr - other.arr)

        return InteractiveArray(self.arr - other)

    def __mul__(self, other):
        if isinstance(other, InteractiveArray):
            return InteractiveArray(self.arr * other.arr)

        return InteractiveArray(self.arr * other)

    def __truediv__(self, other):
        if isinstance(other, InteractiveArray):
            return InteractiveArray(self.arr / other.arr)

        return InteractiveArray(self.arr / other)

    def __pow__(self, other):
        if isinstance(other, InteractiveArray):
            return InteractiveArray(self.arr**other.arr)

        return InteractiveArray(self.arr**other)

    def __gt__(self, other):
        if isinstance(other, InteractiveArray):
            return InteractiveArray(self.arr > other.arr)

        return InteractiveArray(self.arr > other)

    def __lt__(self, other):
        if isinstance(other, InteractiveArray):
            return InteractiveArray(self.arr < other.arr)

        return InteractiveArray(self.arr < other)

    def __ge__(self, other):
        if isinstance(other, InteractiveArray):
            return InteractiveArray(self.arr >= other.arr)

        return InteractiveArray(self.arr >= other)

    def __le__(self, other):
        if isinstance(other, InteractiveArray):
            return InteractiveArray(self.arr <= other.arr)

        return InteractiveArray(self.arr <= other)

    def __eq__(self, other):
        if isinstance(other, InteractiveArray):
            return InteractiveArray(self.arr == other.arr)

        return InteractiveArray(self.arr == other)

    def __getitem__(self, key):
        item = self.arr[key]
        if isinstance(item, np.ndarray):
            return InteractiveArray(item)
        return item

    def __setitem__(self, key, value):
        self.arr[key] = value

    def __repr__(self) -> str:
        self.display()
        return ""

    def __sizeof__(self):
        return self.arr.__sizeof__()


def draw_fib_tree(n):
    """
    Simplified function to draw Fibonacci call tree using Graphviz, displayed inline in Jupyter Notebook.

    Parameters:
        n (int): The input number for the Fibonacci sequence.
    """

    def draw_fib_tree_internal(n, parent=None, graph=None, counter=None):
        if graph is None:
            graph = Digraph("FibonacciTree")
        if counter is None:
            counter = {}

        # Create a unique identifier for this function call
        count = counter.get(n, 0)
        counter[n] = count + 1
        node = f"fib({n})_{count}"

        # Add the node to the graph
        graph.node(node, label=f"fib({n})")

        # Add an edge from the parent to this node
        if parent is not None:
            graph.edge(parent, node)

        # Base case: stop the recursion
        if n <= 1:
            return graph

        # Recursive case: create child nodes and edges
        graph = draw_fib_tree_internal(n - 1, node, graph, counter)
        graph = draw_fib_tree_internal(n - 2, node, graph, counter)

        return graph

    # Initialize Graphviz graph and draw the tree
    G = draw_fib_tree_internal(n)

    # Render the graph inline in the notebook
    display(G)
