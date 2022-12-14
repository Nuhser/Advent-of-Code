import aoc_util as aoc
import json
import utility.sorting as sorting

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.pairs: list[tuple[list, list]] = []
        for block in aoc.parse_input_with_blocks(puzzle_input):
            self.pairs.append((json.loads(block[0]), json.loads(block[1])))

    def part1(self) -> tuple[str, (int | float | str | None)]:
        correct_pairs: list[int] = []
        for pair_idx, (left, right) in enumerate(self.pairs):
            if self.compare_pairs(left, right):
                correct_pairs.append(pair_idx + 1)

        solution = sum(correct_pairs)
        return f"Correct Pairs: {correct_pairs}\nThe sum is {aoc.ANSI_UNDERLINE + str(solution) + aoc.ANSI_NOT_UNDERLINE}", solution

    def part2(self) -> tuple[str, (int | float | str | None)]:
        packets = [packet for pair in self.pairs for packet in pair] + [[[2]], [[6]]]
        sorting.merge_sort(packets, lambda a, b: self.compare_pairs(a, b))

        divider_packets = [-1, -1]
        for idx, packet in enumerate(packets):
            if packet == [[2]]:
                divider_packets[0] = idx + 1
            if packet == [[6]]:
                divider_packets[1] = idx + 1

        if divider_packets[0] == -1:
            raise RuntimeError("First divider packet '[[2]]' wasn't found in ordered packets!")
        elif divider_packets[1] == -1:
            raise RuntimeError("Second divider packet '[[6]]' wasn't found in ordered packets!")

        return f"Decoder Key: {divider_packets[0] * divider_packets[1]}", divider_packets[0] * divider_packets[1]

    def visualize(self) -> None:
        import matplotlib.pyplot as plt
        from matplotlib.animation import FuncAnimation

        sorted_packets = [packet for pair in self.pairs for packet in pair] + [[[2]], [[6]]]
        sorting.merge_sort(sorted_packets, lambda a, b: self.compare_pairs(a, b))

        # initialize plots
        figure, ((ax_bubble, ax_heap), (ax_insertion, ax_merge), (ax_quick, ax_selection)) = plt.subplots(3, 2)

        figure.set_figwidth(10)
        figure.set_figheight(10)
        figure.tight_layout(rect=[0, 0, 1, 0.9])
        figure.suptitle("Advent of Code Day 13 Part 2")

        # bubble sort
        history_bubble = sorting.bubble_sort([packet for pair in self.pairs.copy() for packet in pair] + [[[2]], [[6]]], lambda a, b: self.compare_pairs(a, b), True)
        ax_bubble.set_title(f"Bubble Sort")
        ax_bubble.set_xticklabels([])
        ax_bubble.set_yticklabels([])
        ax_bubble.set_ylim(0, len(sorted_packets))
        rects_bubble = ax_bubble.bar([i for i in range(len(history_bubble[0]))], [0] * len(history_bubble[0]), color="b")

        # heap sort
        history_heap = sorting.heap_sort([packet for pair in self.pairs.copy() for packet in pair] + [[[2]], [[6]]], lambda a, b: self.compare_pairs(a, b), True)
        ax_heap.set_title(f"Heap Sort")
        ax_heap.set_xticklabels([])
        ax_heap.set_yticklabels([])
        ax_heap.set_ylim(0, len(sorted_packets))
        rects_heap = ax_heap.bar([i for i in range(len(history_heap[0]))], [0] * len(history_heap[0]), color="g")

        # insertion sort
        history_insertion = sorting.insertion_sort([packet for pair in self.pairs.copy() for packet in pair] + [[[2]], [[6]]], lambda a, b: self.compare_pairs(a, b), True)
        ax_insertion.set_title(f"Insertion Sort")
        ax_insertion.set_xticklabels([])
        ax_insertion.set_yticklabels([])
        ax_insertion.set_ylim(0, len(sorted_packets))
        rects_insertion = ax_insertion.bar([i for i in range(len(history_insertion[0]))], [0] * len(history_insertion[0]), color="y")

        # merge sort
        history_merge = sorting.merge_sort([packet for pair in self.pairs.copy() for packet in pair] + [[[2]], [[6]]], lambda a, b: self.compare_pairs(a, b), True)
        ax_merge.set_title(f"Merge Sort")
        ax_merge.set_xticklabels([])
        ax_merge.set_yticklabels([])
        ax_merge.set_ylim(0, len(sorted_packets))
        rects_merge = ax_merge.bar([i for i in range(len(history_merge[0]))], [0] * len(history_merge[0]), color="r")

        # quick sort
        history_quick = sorting.quick_sort([packet for pair in self.pairs.copy() for packet in pair] + [[[2]], [[6]]], lambda a, b: self.compare_pairs(a, b), save_history=True)
        ax_quick.set_title(f"Quick Sort")
        ax_quick.set_xticklabels([])
        ax_quick.set_yticklabels([])
        ax_quick.set_ylim(0, len(sorted_packets))
        rects_quick = ax_quick.bar([i for i in range(len(history_quick[0]))], [0] * len(history_quick[0]), color="c")

        # selection sort
        history_selection = sorting.selection_sort([packet for pair in self.pairs.copy() for packet in pair] + [[[2]], [[6]]], lambda a, b: self.compare_pairs(a, b), True)
        ax_selection.set_title(f"Selection Sort")
        ax_selection.set_xticklabels([])
        ax_selection.set_yticklabels([])
        ax_selection.set_ylim(0, len(sorted_packets))
        rects_selection = ax_selection.bar([i for i in range(len(history_selection[0]))], [0] * len(history_selection[0]), color="m")

        frame_time = 5
        n_frames = max(len(history_bubble), len(history_heap), len(history_insertion), len(history_merge), len(history_quick), len(history_selection))
        n_frames += (5000 // frame_time)

        def init():
            print()
            return rects_bubble

        def animate(i):
            figure.suptitle(f"Advent of Code Day 13 Part 2\nFrame {i+1} of {n_frames}")

            for rect, height in zip(rects_bubble, [sorted_packets.index(packet) + 1 for packet in history_bubble[min(i, len(history_bubble) - 1)]]):
                rect.set_height(height)

            for rect, height in zip(rects_heap, [sorted_packets.index(packet) + 1 for packet in history_heap[min(i, len(history_heap) - 1)]]):
                rect.set_height(height)

            for rect, height in zip(rects_insertion, [sorted_packets.index(packet) + 1 for packet in history_insertion[min(i, len(history_insertion) - 1)]]):
                rect.set_height(height)

            for rect, height in zip(rects_merge, [sorted_packets.index(packet) + 1 for packet in history_merge[min(i, len(history_merge) - 1)]]):
                rect.set_height(height)

            for rect, height in zip(rects_quick, [sorted_packets.index(packet) + 1 for packet in history_quick[min(i, len(history_quick) - 1)]]):
                rect.set_height(height)

            for rect, height in zip(rects_selection, [sorted_packets.index(packet) + 1 for packet in history_selection[min(i, len(history_selection) - 1)]]):
                rect.set_height(height)

            return rects_bubble

        animation = FuncAnimation(figure, animate, init_func=init, frames=n_frames, interval=frame_time, blit=True)
        animation.save(
            "2022/visualization13.gif",
            progress_callback=lambda i, n: print(f"{aoc.ANSI_LINE_BEGINNING}Animating frame {i + 1} of {n_frames}..." + ("\nAnimation done. Saving GIF..." if (i+1) == n else ""))
        )

    def compare_pairs(self, left, right) -> bool | None:
        if len(left) == 0:
            return True

        for i in range(len(left)):
            if i > (len(right) - 1):
                return False

            if (type(left[i]) == int) and (type(right[i]) == int):
                if left[i] < right[i]:
                    return True
                elif left[i] > right[i]:
                    return False
                else:
                    continue
            
            elif (type(left[i]) == list) and (type(right[i]) == list):
                comparison = self.compare_pairs(left[i], right[i])
                if (comparison == None):
                    continue
                else:
                    return comparison

            else:
                comparison = self.compare_pairs(left[i] if type(left[i]) == list else [left[i]], right[i] if type(right[i]) == list else [right[i]])
                if (comparison == None):
                    continue
                else:
                    return comparison

        if len(right) > len(left):
            return True

        return None