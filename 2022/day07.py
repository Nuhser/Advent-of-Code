import aoc_util as aoc
import json

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        # This parser assumes that the puzzle input valid and no files or directories on the same level in the file system share the same name.

        # init file system
        self.file_system = [{
            "name": "/",
            "size": 0,
            "parent": None,
            "children": []
        }]

        # parse puzzle input
        current_dir = self.file_system[0]
        for line in aoc.parse_input(puzzle_input[1:], ""):
            # command input ("$ ls" is ignored)
            if line[0] == "$":
                if line[1] == "cd":
                    if line[2] == "..":
                        current_dir = self.file_system[current_dir["parent"]] if current_dir["name"] != "/" else current_dir
                    else:
                        current_dir = [self.file_system[child] for child in current_dir["children"] if self.file_system[child]["name"] == line[2]][0]

                    # update current directory size
                    current_dir["size"] = sum([self.file_system[child]["size"] for child in current_dir["children"]])

            else:
                # add new directory and link to parent
                if line[0] == "dir":
                    self.file_system.append({
                        "name": line[1],
                        "size": 0,
                        "parent": self.file_system.index(current_dir),
                        "children": []
                    })
                    current_dir["children"].append(len(self.file_system) - 1)

                # add new file, link to parent and update parent's size
                else:
                    self.file_system.append({
                        "name": line[1],
                        "size": int(line[0]),
                        "parent": self.file_system.index(current_dir)
                    })
                    current_dir["children"].append(len(self.file_system) - 1)
                    current_dir["size"] += int(line[0])

        # do last size update from current directory to root
        while True:
            current_dir["size"] = sum([self.file_system[child]["size"] for child in current_dir["children"]])

            if current_dir["parent"] == None:
                break

            current_dir = self.file_system[current_dir["parent"]]

        if self.verbose:
            print(f"File System:\n{json.dumps(self.file_system)}\n")

    def part1(self) -> tuple[str, (int | str)]:
        threshold = 100000

        solution = sum([directory['size'] for directory in self.file_system if ('children' in directory) and (directory['size'] <= threshold)])
        return f"Total size of all directories with a size below {threshold}: {solution}", solution

    def part2(self) -> tuple[str, (int | str)]:
        space_used = self.file_system[0]["size"]
        space_free = 70000000 - space_used
        space_needed = 30000000 - space_free

        if self.verbose:
            print(f"Used Space: {space_used}\nFree Space: {space_free}\nNeeded Space: {space_needed}\n")

        solution = min([element['size'] for element in self.file_system if ('children' in element) and (element['size'] >= space_needed)])
        return f"Size of smalest directory that can be deleted: {solution}", solution